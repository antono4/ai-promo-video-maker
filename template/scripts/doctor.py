"""Environment check: run this first on first use, on a new computer, or when a script throws an odd error. It only checks, never installs anything.

python3 <tool dir>/template/scripts/doctor.py   run from the workspace root (before a project exists)
python3 scripts/doctor.py                      run inside <output dir>/<project>/project/ (also checks node_modules)

MISSING items are required; without them you cannot make a video. WARN items are optional; missing ones only affect the corresponding feature.
"""
import importlib.util
import json
import os
import platform
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
MAC, WIN = platform.system() == "Darwin", platform.system() == "Windows"
rows = []


def report(level, name, detail, fix=""):
    rows.append(level)
    pad = 18 - sum(2 if ord(c) > 0x2E80 else 1 for c in name)
    print(f"{level:8s}{name}{' ' * pad}{detail}" + (f"\n{'':26s}→ {fix}" if fix else ""))


def install_hint(mac, win, linux):
    return mac if MAC else win if WIN else linux


def version(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=20).stdout.strip().splitlines()[0]
    except (OSError, IndexError, subprocess.TimeoutExpired):
        return ""


v = version(["node", "-v"])
major = int(re.sub(r"\D", "", v.split(".")[0]) or 0) if v else 0
if major >= 18:
    report("OK", "Node.js", v)
else:
    report("MISSING", "Node.js", v or "not installed", "install Node.js 18 or newer: https://nodejs.org")

for tool in ("ffmpeg", "ffprobe"):
    if shutil.which(tool):
        report("OK", tool, version([tool, "-version"])[:60])
    else:
        report("MISSING", tool, "not installed", install_hint("brew install ffmpeg", "winget install ffmpeg", "sudo apt install ffmpeg"))

if sys.version_info >= (3, 9):
    report("OK", "Python", platform.python_version())
else:
    report("MISSING", "Python", platform.python_version(), "Python 3.9 or newer is required")

missing = [m for m, mod in [("numpy", "numpy"), ("scipy", "scipy"), ("Pillow", "PIL"), ("fonttools", "fontTools"), ("brotli", "brotli")] if not importlib.util.find_spec(mod)]
if missing:
    report("MISSING", "Python deps", "missing " + " ".join(missing), f"pip install -r {os.path.relpath(os.path.join(ROOT, 'requirements.txt'))}")
else:
    report("OK", "Python deps", "numpy scipy Pillow fonttools brotli")

if importlib.util.find_spec("playwright"):
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            exe = p.chromium.executable_path
        if os.path.exists(exe):
            report("OK", "Playwright", "4K page captures available (scripts/shot.py)")
        else:
            report("WARN", "Playwright", "browser engine not installed", "playwright install chromium")
    except Exception as e:  # noqa: BLE001
        report("WARN", "Playwright", f"failed to start: {e}"[:80], "playwright install chromium")
else:
    report("WARN", "Playwright", "not installed; shot.py / snapshot.py cannot capture pages", "pip install playwright && playwright install chromium")

if os.path.isdir(os.path.join(ROOT, "node_modules")):
    report("OK", "npm deps", "installed")
elif os.path.basename(ROOT) == "template":
    report("OK", "npm deps", "run npm install in project/ after creating a project (do not install in template)")
else:
    report("MISSING", "npm deps", "not installed", "npm install")

try:
    from fonts import resolve

    cfg = json.load(open(os.path.join(ROOT, "fonts.json"), encoding="utf-8"))
    bad = [f["file"] for f in cfg["fonts"] if not resolve(f["source"])]
    if bad:
        report("MISSING", "Chinese fonts", f"cannot find {', '.join(bad)}", "put the font files in fonts-src/ and edit fonts.json; on Linux try sudo apt install fonts-noto-cjk")
    else:
        report("OK", "Chinese fonts", ", ".join(os.path.basename(resolve(f["source"])[0]) for f in cfg["fonts"]))
except Exception as e:  # noqa: BLE001
    report("WARN", "Chinese fonts", f"check failed: {e}"[:80])

from elevenlabs import env_files  # noqa: E402

env = os.environ.get("ELEVENLABS_API_KEY") and "environment variable"
for f in env_files():
    if not env and os.path.exists(f) and "ELEVENLABS_API_KEY=" in open(f, encoding="utf-8").read():
        env = f
if env:
    report("OK", "ElevenLabs", f"key configured ({env}); check quota with python3 scripts/elevenlabs.py quota")
else:
    report("WARN", "ElevenLabs", "not configured: narration and custom music are unavailable; will fall back to library music + captions", "when needed, write ELEVENLABS_API_KEY=... into the workspace root .env, or set it as an environment variable")

print()
if "MISSING" in rows:
    print(f"{rows.count('MISSING')} required environment items are not ready; run this again once they are installed.")
    sys.exit(1)
print("All required environment items are ready." + ("" if MAC else " This tool is mainly polished on macOS; on other systems consult references/pitfalls.md when you hit problems."))
