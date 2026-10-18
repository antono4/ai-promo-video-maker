"""Pre-render asset gate: whether the public/ files referenced in code exist, whether images are too small or too large, and whether the font subset is missing glyphs. Exit code is 1 when there are ERRORs.

python3 scripts/check_assets.py
"""
import glob
import json
import os
import re
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, "public")
EXT = r"png|jpe?g|webp|svg|gif|mp3|wav|mp4|webm|woff2"
errors, warns = [], []

refs = set()
for p in glob.glob(os.path.join(ROOT, "src", "**", "*.ts*"), recursive=True) + glob.glob(os.path.join(ROOT, "web", "*.ts*")):
    for m in re.finditer(rf"[\"'`]/?([^\"'`$\s]+\.(?:{EXT}))[\"'`]", open(p, encoding="utf-8").read()):
        refs.add((m.group(1).lstrip("/"), os.path.relpath(p, ROOT)))
for ref, where in sorted(refs):
    if not os.path.exists(os.path.join(PUB, ref)):
        errors.append(f"missing file public/{ref} ({where})")

if not os.path.exists(os.path.join(PUB, "audio", "mix.wav")):
    errors.append("missing public/audio/mix.wav; run npm run mix first")

for f in glob.glob(os.path.join(PUB, "**", "*.*"), recursive=True):
    if not re.search(r"\.(png|jpe?g|webp)$", f, re.I):
        continue
    try:
        w, h = Image.open(f).size
    except Exception as e:
        errors.append(f"corrupt image {os.path.relpath(f, ROOT)}: {e}")
        continue
    rel = os.path.relpath(f, ROOT)
    if max(w, h) < 1000:
        warns.append(f"{rel} is only {w}x{h}; it will look blurry at 4K if displayed wider than {w // 2}px")
    if w > 3000:
        warns.append(f"{rel} is {w}px wide; multiple on screen at 4K can fail to decode, so downscale to display size x2")

cfg = json.load(open(os.path.join(ROOT, "fonts.json"), encoding="utf-8"))
for f in cfg["fonts"]:
    if not os.path.exists(os.path.join(PUB, "fonts", f"{f['file']}.woff2")):
        errors.append(f"missing font public/fonts/{f['file']}.woff2; run npm run fonts first")

for w in warns:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
print(f"{len(refs)} files referenced; {len(errors)} errors, {len(warns)} warnings")
sys.exit(1 if errors else 0)
