# Verification checklist

Verification is done by the AI independently: find a problem → fix it → re-capture and re-check, delivering only when everything passes.

## A. Automated gates (must be 0 ERROR)

```bash
npm run fonts                 # reports missing glyphs → change the font or the copy
python3 scripts/elevenlabs.py vo    # with narration: every line OK (fits in its time window + transcript matches)
npm run mix                   # mix; with narration it prints vo_margin, every line must be ≥ +8 dB
python3 scripts/elevenlabs.py check-mix   # with narration: transcribe the finished mix, overall match ≥ 0.97, every line audible
npm run check:assets          # missing files / images too small or too large / missing fonts
npm run lint                  # eslint + tsc
```

After the finished video:

```bash
python3 scripts/check_video.py out/final-4k.mp4 --scale 2   # spec, log errors, loudness, per-scene frame extraction
```

If the render log contains any error like `cannot be decoded`, treat it as a failure even if the render "succeeded" (see the pitfalls doc).

## B. Image review (every round)

```bash
node scripts/stills.mjs --scenes && python3 scripts/sheet.py   # two frames per scene at 35% / 85%
node scripts/stills.mjs 11.4 11.6 18.7                          # extra captures at key transitions, drop points, and moments when text has fully appeared
```

Open `out/sheet.jpg`, and enlarge anything suspicious with the original image (`out/stills/*.jpg`). Confirm item by item:

**Text**
- [ ] All text has enough contrast against its background: light gradient text on a light background, white text at the center of a light effect, and text in the same color family as its background all need fixing (darken the color, add an outline or glow, dim the background).
- [ ] No overflow, truncation, or unintended line breaks; a Chinese title does not break in the middle of a word (something like "五大核心心 / 法" needs a layout or font-size fix).
- [ ] Occluded text: when cards are stacked, check whether the text of the card behind is covered.
- [ ] Numbers, names, and URLs are all correct and match the research notes.
- [ ] Every explanatory sentence you wrote yourself (qualifiers like "pure SVG," "with a soundtrack," "seven art styles," "only recently popular") can be found verbatim in the original post / official page; if not, delete it.
- [ ] Text over video footage (especially in fast-cut montages where the picture flickers bright and dark) has a dark backing strip, not just a text shadow.

**Story** (against principle 4 of AGENTS.md)
- [ ] Outsider retelling test: reading only the narration script in `timing.json`, write out the "chain of events" in 5 sentences. Whichever sentence does not connect to the previous one, or whichever word needs background knowledge to understand, fix that sentence or add an explanation card.
- [ ] The first narration line and the first screen of large text, taken alone, still explain "what this is, what happened."
- [ ] Text and voice say the same thing: on-screen large text appears at most 1.5 seconds before the narration, never after it.

**Pacing** (against "Pacing: floors + density" in AGENTS.md)
- [ ] Every piece of text stays long enough to read; showcase shots ≥ 1.3 seconds, fast cuts ≥ 0.65 seconds, information scenes ≥ 3.5 seconds.
- [ ] The URL / CTA appears at the highest climax and stays ≥ 3 seconds.
- [ ] The screenshot at 3 seconds already shows a pain point or core highlight; the first high-energy moment appears before 5 seconds.
- [ ] Extract frames at 0.5-second intervals across the first 0–12 seconds and look through them: at most 2 shots in the first 4 seconds; each focal point and each line of text in a push-in holds for a full 1.4 seconds (the second version of Fable packed 3 shots into the first 4 seconds and two focal points into 2 seconds, and was called "too fast, no time to see the picture").
- [ ] Extract frames at 1-second intervals (pass 0,1,2,… to `node scripts/stills.mjs`) and check section by section: no stretch of more than 2 consecutive seconds where "nothing new appears on screen"; pure transitions ≤ 0.6 seconds.
- [ ] Put all the scene screenshots side by side: the same layout does not appear 3 times in a row.
- [ ] Total duration is within the confirmed range (45–60 seconds by default).

**Real assets**
- [ ] Every feature segment has a real interface screenshot or real work image, no fewer than 8 across the whole film; there is one fast-cut montage of ≥ 8 real works.
- [ ] Real screenshots are sharp at 4K (source width ≥ display width × 2); screenshots contain no promo banners, floating bars, or personal privacy information (the account avatar or username in the top-right).
- [ ] Screenshots are not squashed or stretched: for each scene with a screenshot, pick a frame and check whether the circular avatars, logos, and icons in the screenshot are still perfect circles, and whether the glyphs look narrower than the original. Look especially at scenes that zoom into or pan across a screenshot (the old template for Yupi AI Navigation squashed all screenshots by 1.12–1.3×).
- [ ] Clear source, clear placement: screenshot assets are sharp (not blurry at 4K) and cropped well (the subject is not cut off).
- [ ] The works / features shown really belong to this product, with no duplicates (the same work does not appear as two similar screenshots).
- [ ] Every scene has continuous micro-motion, with no dead frames; no black screens or wrong-frame flashes around transitions.
- [ ] The style matches the requirements confirmation and has not slid back to "the default dark tech look."

**Web version** (if there is one)
- [ ] `npm run web` opens, and the poster frame, loading progress, play, pause, end screen, and CTA buttons all work; no extra controls cover the picture during playback.
- [ ] Audio is continuous and single: in **real Chrome** (Playwright or DevTools MCP) press play and read `<audio>.currentTime` every 0.25 seconds; within 10 seconds it should rise by 1.0 per second and never go backward; a hook counting `AudioBufferSourceNode.prototype.start` should read 0. The AI tool's built-in browser is slower than real Chrome, so its results are only indicative.
- [ ] Pause and close the test page immediately after testing (both the test Chrome and the built-in browser): their sound comes out of the user's speakers and overlaps what the user is listening to.
- [ ] When showing the web version to the user, use `npm run web:serve` (which supports range requests for audio), then open `http://127.0.0.1:18765` in the **system browser** (macOS `open`, Windows `start`, Linux `xdg-open`). Do not use `python3 -m http.server` (no Range support), and do not let the user listen in the AI tool's built-in browser: the web version of Yupi AI Navigation sent no sound at all after play was pressed in the built-in browser, and the user reported "there's no sound," while the same page worked fine in Chrome.
- [ ] It stops on the last frame (`moveToBeginningWhenEnded={false}`), and the CTA does not overlap the text in the end frame.

**Audio**
- [ ] The `python3 scripts/mix.py --env` curve matches the design: entry point, build-up, drop jump, sudden stop, and ending decay.
- [ ] Sound-effect timings match the visual events (spot-check 2–3, comparing screenshot times with cue times).
- [ ] `vo` is all `OK`, `check-mix` passes, and `voice.keywords` lists the brand name and URL (whole-sentence similarity lets a mispronounced brand name through; see section 3 of `narration.md`).
- [ ] If you changed the narration model, voice settings, or toggled `sts`: you have already given the user 3 sample lines and gotten confirmation.
- [ ] The narration matches the visuals: the projects and numbers it names are really on screen at that moment (use Scribe word-level timestamps to check keywords, e.g. a URL must be spoken only after it appears on screen).
- [ ] The opening music mood matches the visuals (the pain-point section is puzzled / tense, not high-energy from the first beat).

## C. Before delivery

- [ ] The finished video has been copied to `<output dir>/<project name>/` with a matching file name (`promo-4k.mp4`).
- [ ] The revision log in `requirements.md` is up to date; `research-notes.md` lists the origin of every asset.
- [ ] The report states the points the user must confirm in person (sound, real data, third-party asset licensing).
- [ ] For products or cases that can change (unreleased products, rumors, like counts): re-verify once before delivery and write any changes into the research notes.
- [ ] If ElevenLabs assets were used, the research notes state the plan used at generation time (the free plan cannot be used commercially), plus the voice name and ID and the prompts.
