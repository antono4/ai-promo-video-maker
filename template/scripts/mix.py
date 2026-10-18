"""This project's cue sheet: mix the assets in audio-src/ into public/audio/mix.wav per src/timing.json. Rewritten per storyboard for each project.

python3 scripts/mix.py            generate the mix
python3 scripts/mix.py --env      print the loudness curve after generating
python3 scripts/mix.py --no-vo    no narration and no music ducking, written to out/mix-music.wav (swap it into the finished video for a "music-only version")
"""
import os
import sys

from audiolib import ROOT, SR, Mix, build_in, duck_curve, load, room_tone, seg, splice, src, sub_boom, timing, voice_lines

TM = timing()
DUR = TM["duration"]
BEAT = TM["beat"]
SC = {k: v[0] for k, v in TM["scenes"].items()}
mix = Mix(DUR)

# ---------- narration: voice.lines in timing.json, generated into audio-src/vo/ by `elevenlabs.py vo`; duck the music by duckDb while speaking ----------
VC = TM.get("voice") or {}
NO_VO = "--no-vo" in sys.argv
VO = voice_lines(TM, VC.get("rmsDb", -13)) if VC.get("lines") and not NO_VO else []
duck = duck_curve([(ln["at"], ln["at"] + len(c) / SR, ln.get("duckDb", VC.get("duckDb", -9))) for ln, c in VO], DUR + 4) if VO else None
for ln, clip in VO:
    mix.place(clip, ln["at"], gain=VC.get("gain", 1.0), fade_out=0.03, tag="voice")

# ---------- music ----------
if os.path.exists(src("music.mp3")):
    music = load("music.mp3")
    off = TM["musicOffset"]
    if TM.get("music"):
        # the composition has its own opening mood section: use it from second 0 per the stitch table (add muffle(body, a, b) when a quiet passage is needed)
        body = splice(music, TM["music"], off, DUR)
        mix.place(body, 0.0, fade_in=0.15, fade_out=1.2, duck=duck, tag="music")
    else:
        music_in = max(0.0, TM["drop"] - 4 * BEAT)
        body = seg(music, off + music_in, off + DUR)
        body = build_in(body, TM["drop"] - music_in)
        mix.place(body, music_in, fade_in=0.3, fade_out=1.5, duck=duck, tag="music")
else:
    print("audio-src/music.mp3 does not exist; outputting the sound-effect layer only")

# ---------- sound effects ----------
mix.place(room_tone(max(1.0, TM["drop"])), 0.0, fade_in=1.0, fade_out=1.0)
mix.place(sub_boom(), TM["drop"], gain=0.9)
for name, start in SC.items():
    if start > 0:
        mix.place(sub_boom(0.6, 90, 45, 8), start, gain=0.3)

mix.vo_margin()
if NO_VO:
    os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
mix.master(os.path.join(ROOT, "out", "mix-music.wav") if NO_VO else None)

if "--env" in sys.argv:
    from audiolib import envelope

    envelope()
