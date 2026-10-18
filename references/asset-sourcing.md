# Asset sourcing

Asset priority: **first-hand product material > AI-generated > web material**. First-hand material (real interfaces, real works, real data) is the source of persuasiveness; AI generation is mainly used for atmosphere, backgrounds, characters, and logo rendering.

Register every asset in `research-notes.md`: file → source (path/URL) → which scene it is used in.

---

## 1. First-hand product material

### Local repository / docs
- Read the README, the directory structure, and the section headings first, and count the real numbers (number of articles, images, words, modules). Write the counting method and results into the research notes, and use only the counted numbers in the film.
- Batch-download document images and build a contact sheet per document to pick through:

```bash
python3 scripts/images.py grab "<repo path>/20 项目实战" "<repo path>/15 模型动态" -o /tmp/imgs
python3 scripts/images.py sheet /tmp/imgs            # one _sheet_<group>.jpg per document; look through them one by one
python3 scripts/images.py crop out/pick.jpg /tmp/imgs/ab12c_03.png /tmp/imgs/9f0e1_11.png
python3 scripts/images.py prepare /tmp/imgs/ab12c_03.png public/works/hotpulse.jpg
```

- **Check the context of every image**: what are the paragraphs before and after it saying? Was it made by this product, or is it an official demo / a comparison target / a reference case? If unsure, do not use it.
- Common problems with screenshots: one image is a multi-screen collage (three phone screens side by side), has annotation boxes drawn on it, or is half cropped. Choose "finished-result images," not "process images."

### Official site / online product
- Use `firecrawl scrape` to get the copy and structure, and **at the same time extract the URLs of every work image on the page**. Posts, docs, and course landing pages often contain a large number of high-resolution real photos (the "project learning advice" post on Codefather alone has 38 project screenshots at 2000–4400px), so take stock first before deciding whether to log in.
- Real interfaces can be rebuilt in layers: redraw the cards, buttons, and lists in React, which allows far more animation than a static screenshot (Vibe's "little fish bookkeeping" app grows into place piece by piece this way). But rebuilding is an **addition** on top of a screenshot; it cannot replace the screenshot itself.

### Real interface screenshots (usable at 4K)
- **Prefer `scripts/shot.py`** (Playwright, works in any AI tool): `python3 scripts/shot.py <url> <name> --scroll 0 1400` captures at 1920×1080 @2x, giving `out/shots/<name>-<index>.jpg` at 3840×2160. `--hide` takes a CSS selector to hide banners and floating bars, `--eval` takes a snippet of JS for finer cleanup, and `--tall 4200 --scale 1.25` captures a full-page long image.
- **When a login is needed**: first run `python3 scripts/shot.py --login <url>` (in the background); it opens a browser window with a UI; ask the user to log in **in that window** (scan a QR code, etc.) and close the window when done. The login state is stored in `out/.browser-profile/`, and later `shot.py` captures in this project carry it. When asking the user to log in, **say clearly which window it is**: users often volunteer "I'll log you in via the built-in browser," but the built-in browser cannot capture high-resolution images.
- **Chrome DevTools MCP also works** (if your AI tool has it): `new_page` to open → `emulate` to set `viewport: "1920x1080x2"` → `evaluate_script` to clean the page → `take_screenshot` (`format: "jpeg", quality: 92, filePath: ...`), again giving 3840×2160.
- **Do not use an AI tool's built-in browser to capture product images** (e.g. Cursor's built-in browser): its screenshots are at most the window width (about 900px, 1× pixels); once you emulate a higher resolution or pixel density, the capture becomes a repeated tiled image. It is only good for showing the user a preview.
- **When the user is already logged in via the built-in browser**: do not make them log in again; switch to "snapshot + local re-render." Use `browser_cdp`'s `Runtime.evaluate` to run `scripts/snapshot.js` (`awaitPromise: true`, `returnByValue: true`); it scrolls through the page to trigger lazy loading, inlines all styles, and returns a self-contained HTML; if the response is too large it is saved to a file, and you hand that file to `python3 scripts/snapshot.py <file> <name> --scroll 0 1400` to render a 3840×2160 screenshot at 1920×1080 @2x in local Chromium, hiding the account avatar in the top-right by default. For long pages add `--tall 4200 --scale 1.25`. Image URLs are online, so rendering needs network access; when a site has hotlink protection the script sends the original site's Referer. This is how Yupi AI Navigation's knowledge-base tutorials (full text requires login) were captured.
- **Screenshot timeouts** (DevTools MCP): when the user switches windows during login, Chrome stops producing frames and `take_screenshot` times out forever. Do `select_page` with `bringToFront: true` first, then capture.
- **Clean the page**: before capturing, hide promo banners (`img[alt*=广告]`, any full-width banner containing "特惠 / 续费"), the floating toolbar on the right, and the floating bar at the bottom; scroll to the area you want to show before capturing.
- **What to capture**: the home page, the real page corresponding to each feature segment, members-only content (after logging in), work / project detail pages, and review / results pages. If you want a scrolling effect, capture several screens above and below on the same page, or capture a full-page long image.
- **For a feature segment showing "there are a lot," capture the list / summary page, not a single detail page**: the second version of Codefather's learning-path segment used the "Java learning path" detail page, and the user said it "should show the learning path list page." When the quantity is the selling point (100+ paths, 30 project sets), let the audience see that long list scrolling.
- **Capture a full-page long image**: on many sites the content area scrolls independently inside the page (`document.body.scrollHeight` equals the viewport height), so `fullPage` cannot capture it. The trick is to temporarily raise the viewport: `shot.py --tall 3000`, or set `viewport: "1920x3000x2"` with `emulate` in DevTools (change it back to `1920x1080x2` afterward), giving 3840×6000. Then crop out just the column containing the list (larger text), and scroll it inside a window in the video using the template's `src/components/BrowserFrame.tsx` (`ratio` set to the source image width / height, `scroll` 0–1).
- **Screenshots placed in the frame must keep their original aspect ratio**: the template's `src/index.css` has already removed Tailwind's `max-width: 100%` on `img`. The Yupi AI Navigation project used an old template, and when the browser window enlarged the screenshot by 1.12–1.3×, the image width was pushed back to the window width while the height stayed the same, so every screenshot was squashed horizontally and the user spotted it immediately. When writing your own image container, compute both width and height from the source image's ratio; do not set only one side and rely on `max-width` as a fallback.
- Put screenshots in `public/shots/` and project images in `public/works/`; for scenes with many images on screen (an image wall), prepare separate thumbnails of ≤ 800px.

### Cases from social platforms (X / Twitter)
When there is no official material and the cases are scattered across user posts (a new model in limited rollout, a tool that just broke out):

- **Find the original post**: second-hand coverage (新智元, 量子位, etc.) is only a lead; follow the "reference links" at the end and the usernames in screenshots back to the original post. Scraping `x.com/<user>` and a single post with firecrawl gets the body and the reply thread (the work is often in the replies). Any case whose original post cannot be found is not used at all.
- **Download the original assets**: `python3 scripts/xgrab.py <tweet id...>` goes through the fxtwitter public API without logging in, getting the original image (`name=orig`, commonly 3000–4000px) and the original video the author uploaded (commonly 1920×1080); quoted / replied-to posts are fetched one level deep as well; `--index` summarizes the author, time, likes, and body.
- **Capture the tweet itself**: X post pages open without logging in. Open at `1920x1080x2` (via `shot.py`'s `--hide`, `--eval`, or DevTools) → hide `[data-testid=BottomBar]`, `[data-testid=sidebarColumn]`, `header[role=banner]`, and the fixed-position layers containing "继续前往 / 扫码 / 查看所有回复" → read the `article`'s `getBoundingClientRect()` → capture and crop out the main post by the rectangle ×2. When the post is taller than one screen, temporarily raise the viewport.
- **Network**: on mainland China networks `pbs.twimg.com` (images) has its connection reset while `video.twimg.com` usually connects. `curl` does not read the macOS system proxy; `xgrab.py` already handles this; when writing your own command, check the proxy port first (macOS `scutil --proxy`, on other systems look at the proxy app's settings), then `export HTTPS_PROXY=http://127.0.0.1:<port>`.
- **Share pages of sites like claude.ai** have a Cloudflare human check that automation cannot get past; use the video the author uploaded instead, and state this in the research notes.
- **Verify attribution**: did the author's own words say it was made by this product / this version? When the same work is reposted by several people (both 宝玉 and indigo reposted the Superman animation), credit only the original author; when the author themselves did not say clearly which model made it ("guess which one is 5.5"), do not use it. Like counts grow, so re-scrape `meta.json` once before delivery to update.
- **Credit**: label each case on screen as `@author · date`, and list all sources at the end.

### Data
- GitHub: `gh api repos/<owner>/<repo> --jq '.stargazers_count'`.
- Data from other platforms (follower counts, user counts) is taken from what the user provides or from an official public page, with the source stated.

## 2. Icons and logos

```bash
npm pack simple-icons && tar xzf simple-icons-*.tgz            # package/icons/<slug>.svg, monochrome; color it yourself when rendering
npm pack @lobehub/icons-static-svg && tar xzf lobehub-*.tgz    # comprehensive AI product icons (Claude Code, Codex, Cursor, Trae…), with -color variants
```

- simple-icons has removed some brands (such as OpenAI); for missing ones, look in LobeHub.
- After downloading, render an icon wall to check: are the names right, are the colors right, are they visible on a dark background (a monochrome black icon needs `filter: invert(1)` on a dark background).
- Get the product's own logo as an original image from the repository or official site; when a 3D / glass-textured version is needed, use an image generator with the original logo as reference.

## 3. AI-generated images

Uses: style sample frames, atmospheric backgrounds, characters, 3D logos, scene illustrations. Use the AI tool's own image generation (Cursor's `GenerateImage`, Codex image generation, etc.). When there is no image generator, draw backgrounds and decorations with code (gradients, SVG, `@remotion/noise`), switch character-based styles to emoji / SVG characters, or ask the user to provide illustration assets.

- Write the prompt clearly: aspect ratio (16:9 / 9:16), keywords for the style direction, lighting, composition, **leaving negative space for text**, and no text of any kind (text is always typeset in code).
- For character styles (chibi, mascots): produce the main character first and finalize it, then use it as the reference image for every subsequent image, changing only the expression / action so it stays the same character.
- Generated images are about 1280×720; when used as a full-screen background, grain, depth of field, or a slight blur can mask the resolution; for subjects that need to be sharp (logos, text), use vectors or code drawing.

## 4. Fonts

- Chinese body text: PingFang (built into macOS, written in `fonts.json` as `system:PingFang#index`, Regular=3 / Medium=7 / Semibold=11 / Light=15). The template defaults to `PingFang | Microsoft YaHei | Noto Sans CJK` in that order, and Windows and Linux automatically switch to the latter two; if the finished video must render exactly the same glyphs on different computers, put the font files in `fonts-src/` and reference them.
- Chinese titles are chosen by style, free and commercially usable, available directly from npm:
  - Alimama ShuHeiTi: `npm pack @fontpkg/alimama-shu-hei-ti` (geometric, techy)
  - Smiley Sans (得意黑): `npm pack @chinese-fonts/dyh` (italic, youthful)
  - Others (ZCOOL KuaiLe, Zpix pixel, LXGW WenKai's handwritten feel, etc.) can be searched on npm or in their official repositories by style
- Put font files in `fonts-src/`, register them in `fonts.json`, and subset with `npm run fonts`. The script reports **missing glyphs**; if any are missing, change the font or the copy.
- For Latin text you can use `@remotion/google-fonts` (e.g. Geist / Geist Mono), imported statically in `src/lib/fonts.ts`.
- Before choosing, render the film's real titles with Pillow and compare a few fonts, then decide.

## 5. Music and sound effects

- **ElevenLabs** (preferred when the user provides a key): composing from the storyboard, customizing sound effects to the visuals, and v4 narration all use `scripts/elevenlabs.py`. See section 6 of `music-and-beats.md` and `narration.md`. The paid plan can be used commercially; the free plan can only use sound effects and cannot be used commercially.
- **Mixkit** (commercially usable, no attribution): both music and sound effects use `scripts/music.py`:

```bash
python3 scripts/music.py search music cinematic trailer electronic uplifting   # list title/id/duration
python3 scripts/music.py search sfx whoosh impact riser typing glitch click
python3 scripts/music.py get music 726 614 -o /tmp/music
python3 scripts/music.py get sfx 790 2531 1486 -o audio-src
```

  Common sound-effect categories: `whoosh` `impact` `riser` `typing` `click` `glitch` `transition` `swoosh` `pop` `notification` `heartbeat` `bell`.
- **Remotion-hosted sound effects**: `https://remotion.media/<name>.wav` (e.g. `whoosh.wav`, `mouse-click.wav`).
- Synthesized sound effects (`audiolib.py`): low-frequency impact `sub_boom`, notification `blip`, card slide `flick`, ambient noise floor `room_tone`. **Do not pad the music with a synthesized sustained tone (a drone)**, as it easily clashes with the track's tonality (this was the cause of the "weird music" in Vibe's first opening).
- If the user asks to use a popular song and accepts the risk, follow what the user says and record it in the requirements confirmation.

## 6. Video assets

- Product demo recordings: prefer what the user provides; when there is none, you can record an online product by operating it with browser tools, or rebuild the interface in React to animate it (clearer and more controllable).
- Use web video clips only with the user's explicit authorization.
