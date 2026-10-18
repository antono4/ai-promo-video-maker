"""Re-render a logged-in page snapshot exported by snapshot.js into a screenshot at high resolution in local Chromium.

python3 scripts/snapshot.py <snapshot> <name>                         # 1920×1080 @2x -> out/shots/<name>-0.jpg (3840×2160)
python3 scripts/snapshot.py <snapshot> <name> --scroll 0 1400 2800     # capture one image at each scroll position of the main scroll container
python3 scripts/snapshot.py <snapshot> <name> --tall 4200 --scale 1.25 # raise the viewport to 4200 and capture a full-page long image (also works for sites whose content area scrolls internally)
python3 scripts/snapshot.py <snapshot> <name> --hide ".float-bar" ".banner"

<snapshot> can be an .html file, the large response file returned by browser_cdp ({"result": {"value": "<JSON>"}}), or snapshot.js's JSON.
By default the account avatar in the top-right is hidden (images within the top 80px and right 240px); --keep-avatar keeps it.
Requires Playwright: pip install playwright && playwright install chromium
"""
import argparse
import json
import os
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SCROLL = """(y) => {
  const els = [document.scrollingElement, ...document.querySelectorAll('*')].filter(e => e.scrollHeight > e.clientHeight + 200 &&
    (e === document.scrollingElement || /(auto|scroll)/.test(getComputedStyle(e).overflowY)));
  const main = els.sort((a, b) => b.scrollHeight - a.scrollHeight)[0];
  if (main) main.scrollTop = y;
  window.scrollTo(0, y);
}"""

AVATAR = """() => Array.from(document.querySelectorAll('img')).filter(i => {
  const r = i.getBoundingClientRect(); return r.top < 80 && r.left > window.innerWidth - 240;
}).forEach(i => { i.style.visibility = 'hidden'; })"""


def load(path):
    text = open(path, encoding="utf-8").read()
    if path.endswith(".html"):
        return {"url": "", "title": "", "html": text}
    d = json.loads(text)
    while isinstance(d, dict) and "html" not in d:
        d = d.get("result", d.get("value"))
        if isinstance(d, str):
            d = json.loads(d)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("snapshot")
    ap.add_argument("name")
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    ap.add_argument("--scale", type=float, default=2)
    ap.add_argument("--scroll", type=int, nargs="*", default=[0])
    ap.add_argument("--tall", type=int, help="viewport height (CSS pixels); capture a full-page long image")
    ap.add_argument("--hide", nargs="*", default=[], help="CSS selectors to hide before capturing (banners, floating bars)")
    ap.add_argument("--keep-avatar", action="store_true")
    ap.add_argument("--out", default=os.path.join(ROOT, "out", "shots"))
    a = ap.parse_args()

    snap = load(a.snapshot)
    os.makedirs(a.out, exist_ok=True)
    open(os.path.join(a.out, f"{a.name}.html"), "w", encoding="utf-8").write(snap["html"])
    origin = urlparse(snap.get("url") or "")
    headers = {"Referer": f"{origin.scheme}://{origin.netloc}/"} if origin.netloc else {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": a.width, "height": a.tall or a.height}, device_scale_factor=a.scale, extra_http_headers=headers)
        pg = ctx.new_page()
        pg.set_content(snap["html"], wait_until="networkidle", timeout=120000)
        pg.wait_for_timeout(1500)
        if not a.keep_avatar:
            pg.evaluate(AVATAR)
        for sel in a.hide:
            pg.add_style_tag(content=f"{sel} {{ display: none !important; }}")
        for i, y in enumerate([0] if a.tall else a.scroll):
            pg.evaluate(SCROLL, y)
            pg.wait_for_timeout(900)
            path = os.path.join(a.out, f"{a.name}-{'tall' if a.tall else i}.jpg")
            pg.screenshot(path=path, type="jpeg", quality=90)
            print(path, (snap.get("title") or "")[:40])
        b.close()


if __name__ == "__main__":
    main()
