"""Offline mixing library: asset placement, synthesized sound effects, music build-in, mastering, and loudness normalization. mix.py is the per-project cue sheet and only calls into here."""
import json
import os
import subprocess

import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, fftconvolve, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "audio-src")
SR = 48000
rng = np.random.default_rng(3)


def timing():
    return json.load(open(os.path.join(ROOT, "src", "timing.json"), encoding="utf-8"))


def src(name):
    return os.path.join(SRC, name)


def load(name):
    """Any audio -> float32 stereo 48k. name can be a file name under audio-src or an absolute path."""
    path = name if os.path.isabs(name) else src(name)
    raw = subprocess.run(
        ["ffmpeg", "-v", "quiet", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
        capture_output=True,
    ).stdout
    if not raw:
        raise FileNotFoundError(path)
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def seg(clip, a, b):
    return clip[int(a * SR) : int(b * SR)]


def lp(x, hz):
    return sosfilt(butter(4, hz, "low", fs=SR, output="sos"), x, axis=0)


def hp(x, hz):
    return sosfilt(butter(4, hz, "high", fs=SR, output="sos"), x, axis=0)


def stereo(m):
    return np.stack([m, m], axis=1).astype(np.float32)


# ---------- synthesized sound effects ----------

def sub_boom(length=3.5, f0=62, f1=28, decay=1.6):
    """Low-frequency impact (a descending sine + a noise transient), used at drops and transition downbeats."""
    t = np.arange(int(length * SR)) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 5)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay)
    click = rng.normal(0, 1, len(t)) * np.exp(-t * 60) * 0.35
    return stereo(np.tanh((body + lp(click, 2500)) * 1.6) * 0.9)


def blip(freq=1800, length=0.09, gain=0.5):
    """UI notification tone, good for cards or numbers appearing one by one."""
    t = np.arange(int(length * SR)) / SR
    return stereo(np.sin(2 * np.pi * freq * t) * np.exp(-t * 55) * gain)


def flick(length=0.05, gain=0.3):
    """Short noise burst for a card sliding."""
    t = np.arange(int(length * SR)) / SR
    n = rng.normal(0, 1, len(t)) * np.exp(-t * 90)
    return stereo(lp(hp(n, 1800), 7000) * gain)


def room_tone(length, gain=0.012):
    """Very light unpitched ambience to fill gaps in a sound-effect-only passage without clashing with any key."""
    return stereo(lp(hp(rng.normal(0, 1, int(length * SR)), 180), 1600) * gain)


def reverb(x, seconds=2.8, wet=0.35):
    n = int(seconds * SR)
    t = np.arange(n) / SR
    irs = []
    for _ in range(2):
        ir = lp(rng.normal(0, 1, n) * np.exp(-t * 6.9 / seconds), 6000)
        irs.append(ir / np.sqrt(np.sum(ir**2)))
    wl, wr = fftconvolve(x[:, 0], irs[0]), fftconvolve(x[:, 1], irs[1])
    dry = np.zeros((len(wl), 2), dtype=np.float32)
    dry[: len(x)] = x
    return (dry * (1 - wet) + np.stack([wl, wr], axis=1) * wet).astype(np.float32)


def keystrokes(name, max_hits=60):
    """Cut single key presses out of a typing recording, for aligning a typing animation character by character."""
    x = load(name)
    mono = np.abs(x.mean(axis=1))
    w = 240
    env = np.array([mono[i : i + w].mean() for i in range(0, len(mono) - w, w)])
    thr = env.max() * 0.35
    hits, last = [], -1e9
    for i in range(1, len(env)):
        if env[i] > thr and env[i - 1] <= thr and (i - last) * w > SR * 0.09:
            hits.append(i * w)
            last = i
    return [x[max(0, h - 200) : h + int(0.11 * SR)] for h in hits[:max_hits]]


def splice(track, spans, offset, duration, xfade=0.03):
    """Cut the track to the film length per timing.json's music stitch table: spans = [{at, from, to}], playing track seconds from~to starting at video second at.
    Stitch points must land on bar lines; seams get an xfade-second crossfade. Use when the track is shorter than the film or you want to repeat a few extra bars in a stretch.
    from / to are track times relative to offset (timing.json's musicOffset), not absolute track times; each span's at must join end to end (next at = previous at + to - from)."""
    xf = int(xfade * SR)
    parts = []
    for sp in spans:
        end = min(sp["to"], sp["from"] + duration - sp["at"])
        c = seg(track, offset + sp["from"], offset + end).copy()
        if parts:
            c[:xf] *= np.linspace(0, 1, xf)[:, None]
            parts[-1][-xf:] *= np.linspace(1, 0, xf)[:, None]
        parts.append(c)
    return np.concatenate(parts)[: int(duration * SR)].copy()


def muffle(clip, a, b, hz=420, gain=0.55, ramp=0.15):
    """Low-pass a~b seconds to "muffle" it (the music sounds like it is behind a wall), restoring full band immediately at b. Use it to create a quiet passage when the composition did not deliver the planned one."""
    i0, i1, k = int(max(0, a - ramp) * SR), int(b * SR), int(ramp * SR)
    out = clip.copy()
    w = np.ones(i1 - i0, dtype=np.float32)
    w[:k] = np.linspace(0, 1, k)
    w[-int(0.05 * SR):] = np.linspace(1, 0, int(0.05 * SR))
    out[i0:i1] = clip[i0:i1] * (1 - w[:, None]) + (lp(clip[i0:i1], hz) * gain).astype(np.float32) * w[:, None]
    return out


def build_in(clip, seconds, hp_hz=700, g0=0.3, g1=0.75):
    """Music build-in: keep only high frequencies at a low volume at the start and open gradually to full band within `seconds`. Feels more driving than a plain fade-in."""
    n = min(len(clip), int(seconds * SR))
    w = (np.linspace(0, 1, n) ** 1.6)[:, None]
    head = clip[:n]
    out = clip.copy()
    out[:n] = ((hp(head, hp_hz) * (1 - w) + head * w) * (g0 + (g1 - g0) * w)).astype(np.float32)
    return out


# ---------- narration ----------

def level(clip, rms_db=-18.0):
    """Normalize a voice clip to a given RMS (counting only the audible part), so every narration line has consistent loudness."""
    m = clip.mean(axis=1)
    w = int(0.05 * SR)
    r = np.sqrt((m[: len(m) // w * w].reshape(-1, w) ** 2).mean(axis=1))
    act = r[r > r.max() * 0.1]
    cur = 20 * np.log10(np.sqrt((act**2).mean()) + 1e-9)
    return (clip * 10 ** ((rms_db - cur) / 20)).astype(np.float32)


def voice_lines(tm=None, rms_db=-18.0):
    """Read voice.lines from timing.json and audio-src/vo/<id>.mp3 (generated by elevenlabs.py vo), returning [(line, clip)]."""
    tm = tm or timing()
    out = []
    for ln in (tm.get("voice") or {}).get("lines", []):
        if not os.path.exists(src(f"vo/{ln['id']}.mp3")):
            raise FileNotFoundError(f"missing narration audio-src/vo/{ln['id']}.mp3: run python3 scripts/elevenlabs.py vo first")
        clip = level(hp(load(f"vo/{ln['id']}.mp3"), 90).astype(np.float32), rms_db)
        out.append((ln, clip))
    return out


def duck_curve(spans, length, depth_db=-7.0, attack=0.08, release=0.35):
    """Generate a per-sample gain for the music from the voice time spans [(start, end[, dB for that line])]: duck by depth_db while speaking, with a smooth transition. Pass to Mix.place(duck=...)."""
    n = int(length * SR)
    db = np.zeros(n, dtype=np.float32)
    t = np.arange(n) / SR
    for sp in spans:
        a, b = sp[0], sp[1]
        d = sp[2] if len(sp) > 2 else depth_db
        up = np.clip((t - (a - attack)) / attack, 0, 1)
        down = np.clip(((b + release) - t) / release, 0, 1)
        db = np.minimum(db, d * np.minimum(up, down))
    return (10 ** (db / 20)).astype(np.float32)


# ---------- mixing console ----------

class Mix:
    def __init__(self, duration, tail=4.0):
        self.duration = duration
        self.buf = np.zeros((int((duration + tail) * SR), 2), dtype=np.float32)
        self.stems = {}
        self.spans = []

    def place(self, clip, at, gain=1.0, align=0.0, fade_in=0.0, fade_out=0.004, duck=None, tag=None):
        """Align second `align` of clip to second `at` of the timeline. duck is the result of duck_curve(), used to duck the music under the voice.
        tag="music" / "voice" also saves a separate stem, which vo_margin() uses to check whether the voice sits above the music."""
        start = int(round((at - align) * SR))
        clip = clip * gain
        if start < 0:
            clip, start = clip[-start:], 0
        clip = clip[: max(0, len(self.buf) - start)].copy()
        n = len(clip)
        if n == 0:
            return
        if fade_in > 0:
            k = min(n, int(fade_in * SR))
            clip[:k] *= np.linspace(0, 1, k)[:, None]
        if fade_out > 0:
            k = min(n, int(fade_out * SR))
            clip[-k:] *= np.linspace(1, 0, k)[:, None]
        if duck is not None:
            g = np.ones(n, dtype=np.float32)
            m = max(0, min(n, len(duck) - start))
            g[:m] = duck[start : start + m]
            clip *= g[:, None]
        self.buf[start : start + n] += clip
        if tag:
            stem = self.stems.setdefault(tag, np.zeros_like(self.buf))
            stem[start : start + n] += clip
            if tag == "voice":
                self.spans.append((start / SR, (start + n) / SR))

    def vo_margin(self, need=8.0):
        """How many dB the voice sits above the music in each narration span. Below `need` means the voice will be buried: raise voice.rmsDb or deepen duckDb."""
        if "voice" not in self.stems or "music" not in self.stems:
            return None
        db = lambda x: 20 * np.log10(np.sqrt(np.mean(x**2)) + 1e-9)
        worst = 99.0
        for a, b in self.spans:
            i, j = int(a * SR), int(b * SR)
            d = db(self.stems["voice"][i:j]) - db(self.stems["music"][i:j])
            worst = min(worst, d)
            print(f"  narration {a:6.2f}s  voice above music by {d:+5.1f} dB" + ("   <- low" if d < need else ""))
        print(f"vo_margin: lowest {worst:+.1f} dB (required >= +{need:.0f})")
        return worst

    def master(self, dest=None, lufs=-14.0, true_peak=-1.0, end_fade=0.8):
        """Soft clip + ending fade-out + ffmpeg two-pass loudnorm. Defaults to -14 LUFS (works for Bilibili / YouTube / TikTok)."""
        dest = dest or os.path.join(ROOT, "public", "audio", "mix.wav")
        out = hp(self.buf[: int(self.duration * SR)], 25)
        peak = np.abs(out).max() or 1.0
        out = np.tanh(out / peak * 1.4) / np.tanh(1.4) * 0.97
        k = int(end_fade * SR)
        out[-k:] *= np.linspace(1, 0, k)[:, None]
        raw = os.path.join(SRC, "_mix_raw.wav")
        wavfile.write(raw, SR, out.astype(np.float32))
        target = f"I={lufs}:TP={true_peak}:LRA=11"
        err = subprocess.run(
            ["ffmpeg", "-hide_banner", "-i", raw, "-af", f"loudnorm={target}:print_format=json", "-f", "null", "-"],
            capture_output=True, text=True,
        ).stderr
        s = json.loads(err[err.rindex("{") : err.rindex("}") + 1])
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-v", "error", "-y", "-i", raw, "-af",
             f"loudnorm={target}:measured_I={s['input_i']}:measured_TP={s['input_tp']}:measured_LRA={s['input_lra']}:"
             f"measured_thresh={s['input_thresh']}:offset={s['target_offset']}:linear=true",
             "-ar", str(SR), "-c:a", "pcm_s16le", dest],
            check=True,
        )
        print(f"mix: input {s['input_i']} LUFS -> {lufs} LUFS  {dest}")
        return dest


def envelope(path=None, step=0.5, until=None):
    """Print the loudness curve of the finished mix, to confirm the entry, build-up, and drop match the design (the main basis when you cannot hear the audio)."""
    path = path or os.path.join(ROOT, "public", "audio", "mix.wav")
    sr, x = wavfile.read(path)
    m = x.astype(np.float32).mean(axis=1) / 32768
    end = until or len(m) / sr
    for a in np.arange(0, end, step):
        s = m[int(a * sr) : int((a + step) * sr)]
        db = 20 * np.log10(np.sqrt(np.mean(s**2)) + 1e-9)
        print(f"{a:6.1f}s {db:6.1f} dB " + "#" * max(0, int(60 + db)))
