# Product Promo Video Maker · Workflow

The user gives you only a **product name** (or a one-sentence request), and you must produce a product promo video with commercial polish: independent research → requirements interview → asset collection → production → verification → export and delivery.

> Top-level goal: **make someone who has never heard of this product want to use it after watching.** The visuals must have the finish of a commercial film, and the information must be true, legible, and keep up with the pace.

"Product" here is broad: apps, websites, SaaS, open-source projects, courses, AI models, communities, and events all count. Who the user is and what product they make is unknown, so **do not assume the user is any particular person, and do not assume the user already has any account**. If something is missing, ask.

---

## Four overarching principles (read first)

1. **There are only three kinds of human checkpoints; everything else is automatic.**
   - **Requirements confirmation** (mandatory): clarify in step 2, write it into `requirements.md`, and only start work after the user has explicitly agreed.
   - **Listen and sign off**: the music and the narration voice must be heard by the user before being finalized (the AI cannot hear sound). Try to move these earlier or merge them into one round; skip them if the user said "you decide" during the requirements interview.
   - **Blockers only the user can resolve**: a login is needed, a fact cannot be verified, asset copyright is uncertain and the user has not authorized it, or a required environment piece is missing.
   Apart from these, do not disturb the user mid-production.
2. **Every product's style, narrative, effects, and layout are different; a fixed template is not allowed.**
   Some products suit a movie trailer, others suit chibi cartoon, hand-drawn, pixel art, a minimal keynote... The style direction must be proposed as several clearly distinct candidates for this product, and **the user must see style sample images and sign off**.
   Any existing finished work in `<output dir>` is only the answer for "that one product"; **copying its colors, layout, shots, or effects is forbidden**.
3. **Style is the packaging; the real product is the star. Grab attention at the start and never drag.** (From shared feedback across several videos: "the pacing is slow, real screenshots are missing, the music doesn't fit.")
   - **Deliver a pain point or the core highlight within the first 3 seconds, and reach the first high-energy moment within 5 seconds** (music drop + brand / selling point). No slow warm-up, and no ceremonial transitions like "typing a search".
   - **Real interface screenshots / real work are the star of every feature segment**; AI-generated images and code-drawn visuals only handle packaging and transitions. If you cannot get them, ask the user first (the user can log in; when there is no account, download the original image or video from a public endpoint, e.g. `xgrab.py`). Do not pad the video with redrawn cards.
4. **Speak plainly so an outsider understands on the first pass.** (From one video's feedback: "it leaves people a bit lost, especially at the start, the story isn't told clearly.")
   - Open with one plain sentence saying "what this is, what happened," then build suspense. A riddle-style opening means nothing to someone who does not know the background.
   - String the narration into a story following "what it is → what happened → how to prove it → the result → what to do now," where each line connects to the previous one; on-screen text and narration should show two sides of the same thing, not talk past each other.
   - The first time insider jargon, memes, or a person's name appears, add a one-line explanation card (e.g. "Tibo = the person who leads Codex at OpenAI").
   - Before delivery, run the "outsider retelling test": reading only the narration script, can you retell the whole chain of events? If not, rewrite the script.

---

## Two usage modes and path conventions

This tool can be cloned and opened directly, or installed as a Skill into an AI tool and called from another workspace. Both modes share this one specification; only the directory locations differ. Below, two placeholders are used consistently:

| Placeholder | Clone mode (the workspace is this repository) | Skill mode (called from another workspace) |
|---|---|---|
| `<tool dir>` | The repository root | The install directory of this Skill, i.e. the directory containing `SKILL.md` and this file (e.g. `~/.claude/skills/promo-video-maker`) |
| `<output dir>` | `<tool dir>/outputs` | `promo/` under the current workspace root |

How to tell which mode you are in: if this AGENTS.md and `template/` are directly in the current workspace root, it is clone mode; otherwise it is Skill mode.

Skill mode has four additional conventions:
- If the current workspace is the product being promoted (its code repository, its documentation directory), that is the best first-hand material: read the README, docs, and code first, then go to the official site.
- When the workspace is a git repository, add `promo/` to its `.gitignore` (finished videos and project files run to several GB, and the project may contain a `.env`), and tell the user.
- Do not write any project file into `<tool dir>`: the whole directory is overwritten when the Skill updates.
- Put the ElevenLabs key in the workspace root `.env` or the `ELEVENLABS_API_KEY` environment variable.

## Directory structure

```
<tool dir>/
├── SKILL.md           # Skill entry point (read by the AI tool when installed as a Skill; it just points to this file)
├── AGENTS.md          # This specification (CLAUDE.md just points to it)
├── README.md          # Human-facing introduction
├── .env.example       # Copy to .env and fill in the ElevenLabs key (optional); shared by all projects
├── references/        # Detailed methods per stage (read as needed)
├── template/          # ★ The only skeleton source for new projects: Remotion project + web player page + full script set (style-agnostic)
├── docs/              # Images used by the README; ignore during production
└── outputs/           # Finished-video repository in clone mode (already in .gitignore, never committed)

<output dir>/
└── <project name>/    # One subdirectory per product
```

## Output directory rules (mandatory)

- Create a **simple, direct, descriptive directory name** for each product under `<output dir>`, e.g. `budget-app-promo/`, `some-open-source-project-promo/`. **Forbidden**: bare codenames like `vibe-promo` or `project-01`. If the product name itself is already a proper name, keep it as is.
- The structure inside the directory is fixed, and all deliverable file names follow the same convention:

```
<output dir>/<project name>/
├── promo-4k.mp4        # Named per the confirmed spec: promo-1080p.mp4, promo-vertical.mp4 …
├── requirements.md     # Checkpoint artifact: every decision the user signed off
├── research-notes.md   # Product facts, data sources, asset list and their origins
├── web/                # Build output when a web version is wanted (copy it over after npm run web:build)
└── project/            # The complete source code copied from <tool dir>/template
```

- **Every new project is copied from `<tool dir>/template`** (command in step 3). Do not copy another existing project, and do not build from scratch.
- Keep intermediate files (screenshots, contact sheets, render logs) in `project/out/`; do not pile them into the project directory.
- Below, "project directory" means `<output dir>/<project name>/`, and "project workspace" means the `project/` under it. Scripts are run from inside the project workspace.

---

## Tool equivalents

This specification works in Cursor, Claude Code, Codex, and other AI coding tools. Different tools name capabilities differently; find the substitute in the table below, and **when a capability is missing, use the fallback in the right column rather than skipping the step**.

| What to do | If you have this kind of tool | If not |
|---|---|---|
| Structured questions (step 2) | Cursor's `AskQuestion`, Claude Code's `AskUserQuestion` | List numbered questions and options in your reply (put the recommended one first) and ask the user to reply by number |
| Generate style sample frames, backgrounds, characters (steps 2, 4) | Cursor's `GenerateImage`, Codex image generation | Draw a 1920×1080 sample frame with HTML/CSS or Remotion code, capture it with `node scripts/stills.mjs` or Playwright; for character-based styles, indicate with emoji / SVG |
| Web search and scraping (steps 1, 4) | firecrawl, the tool's built-in web search / scraping | `curl` + read the HTML; use `gh api` for GitHub data |
| Capture 4K web screenshots (step 4) | `python3 scripts/shot.py` (Playwright, works in every tool; first choice) | Chrome DevTools MCP also works; when the user is already logged in via the AI tool's built-in browser, use `snapshot.js` + `snapshot.py` (see `references/asset-sourcing.md`) |
| Task list (throughout) | A TodoWrite-style tool in Cursor / Claude Code | Maintain a progress checklist in your replies |

---

## Process overview

```
Progress checklist (copy into your task list to track):
- [ ] 0. Environment check: python3 <tool dir>/template/scripts/doctor.py
- [ ] 1. Pre-research: establish what the product is and what assets already exist
- [ ] 2. Requirements interview ★ human checkpoint: multiple rounds of questions + style sample frames → requirements.md → explicit user agreement
- [ ] 3. Create project: copy template, write the first draft of timing/theme/fonts
- [ ] 4. Deep research and asset collection → research-notes.md
- [ ] 5. Music and beat grid: ElevenLabs composes from the storyboard (or pick from a library) → ★ listen → timing.json
- [ ] 6. Storyboard and production: implement scene by scene
- [ ] 7. Narration and mixing: ★ listen to voices → generate narration + transcript check → align sound effects → keep the voice above the music
- [ ] 8. Verification loop: automated gates + manual review of per-scene screenshots, fixing until everything passes
- [ ] 9. Export and delivery: render → finished-video gate → copy to the project directory → report
- [ ] 10. Revision (when feedback arrives): record the exact words → sync the template → redo only the necessary steps for the scope of the change → update the docs → back up the old version, then deliver
```

### 0. Environment check (first time only)

Run `python3 <tool dir>/template/scripts/doctor.py` from the workspace root. It only checks, never installs:

- `MISSING` items are required (Node.js 18+, ffmpeg, Python 3.9+ and its dependencies, Chinese fonts). Python dependencies can be installed directly with `pip install -r <tool dir>/template/requirements.txt`; tell the user before installing. For system software like Node and ffmpeg, give the user the install command and ask them to install it before continuing.
- `WARN` items are optional: without Playwright you cannot use `shot.py` to capture screenshots; without an ElevenLabs key you cannot generate narration or custom music (take this into account when offering sound options in step 2).
- This tool is mainly polished on macOS. On Windows / Linux the fonts automatically fall back to Microsoft YaHei / Noto Sans CJK; for other differences, consult `references/pitfalls.md` when you hit them.

### 1. Pre-research (within 10 minutes, so you can ask good questions)

- **Verify the product's official status first**: does this product appear on the official site / official news page, and what is the latest version number. What the user calls "the new XX" may not be released yet (a pitfall we hit: a model version that was only a rumor in a limited rollout). When there is no official source, stop immediately and ask about positioning: wait for the official release / cover the already-released version / make an "early look" with an "unofficially confirmed" label throughout.
- Work out where the product lives: a local path? an official site? GitHub? an app? First ask yourself whether you can get **first-hand material** (docs, screenshots, real data). When the user gave only a vague sentence with no product name at all, make the product name and URL the first question.
- Get quickly: a one-sentence positioning, target users, core selling points, provable numbers (stars, user count, number of articles), brand color and logo, and existing visual assets.
- Tools: read local files directly; use search / scraping tools for web pages; use `gh api` for GitHub data.

### 2. Requirements interview (★ the only mandatory human checkpoint)

Follow `references/requirements-interview.md`. Key points:

- Ask with a structured question tool, and **give a recommendation tailored to this product for every question**, with a reason.
- Required dimensions: deliverable form, aspect ratio and duration, audience, **style direction**, **narrative structure**, **opening hook** (pain point or core highlight), climax shot, sound plan, **real screenshot sources** (are public pages enough, or does the user need to log in), asset copyright boundaries, URL and CTA, export spec, and mid-production review method.
- **Offer sound-plan options based on the user's situation**: with an ElevenLabs account, recommend "compose from the storyboard + AI narration"; without an account, recommend "library music + large captions" and tell the user what extra is possible once a key is configured. Do not decide the voice in this round; produce a listen sample after the narration script is written (see step 7).
- Default duration recommendation: **45–60 seconds**; anything over 60 seconds needs an explicit request from the user, with the reason written into the requirements confirmation.
- **The style direction must be visualized**: propose 3–4 clearly distinct directions for this product (pick from `references/style-directions.md` or invent your own, with at least one "unexpected" one such as chibi, hand-drawn, or pixel), produce one 16:9 style sample frame for each (draw it with code when you have no image generator, see "Tool equivalents"), and put them together for the user to choose from.
- Write all conclusions into `requirements.md` (template in `references/requirements-interview.md`), and only move to step 3 after the user confirms "accurate, start production".

### 3. Create project

```bash
mkdir -p "<output dir>/<project name>" && cp -R "<tool dir>/template" "<output dir>/<project name>/project" && cd "<output dir>/<project name>/project" && npm install
```

- `src/timing.json`: aspect ratio (`width`/`height`), frame rate, total duration, scene table. The **single source of truth** for all time points; both the visuals and the mix read from here.
- `src/lib/theme.ts`: rewrite the color palette and font variables to match the confirmed style.
- `fonts.json`: choose fonts by style (see the fonts section of `references/asset-sourcing.md`), then run `npm run fonts`.
- `web/config.ts` + the CSS variables in `web/style.css`: brand name, CTA links, button colors. Put the product logo at `public/img/logo.png` (used by the web version's corner badge and favicon; `check:assets` errors if it is missing).

### 4. Deep research and asset collection

Follow `references/asset-sourcing.md`. Produce `research-notes.md`: product facts (each with a source), the list of work / features to show, and the origin of every asset.

Iron rules:
- **Facts must be verifiable**: numbers, features, and author information all need a source; never invent.
- **Every explanatory sentence you put on screen must also be findable in a source**: do not add qualifiers to a case that the original post did not say ("pure SVG," "with a soundtrack," "seven art styles," "only recently popular" were all nearly written wrong). When unsure, delete the words.
- **Second-hand coverage is only a lead; always trace back to the original post**: do not use cases whose original post cannot be found; for the same work reposted by several people, credit only the original author; dates in second-hand coverage are often in Beijing time, so defer to the official page.
- **The work shown must really have been made by this product.** No matter how good an official demo image or a third-party case looks, it cannot be passed off as this product's (a pitfall we hit: a 3D open-world screenshot that was actually an official demo from a different model vendor).
- **Look at the full set when picking images**: batch-download every image in each document, generate a contact sheet per document, and pick document by document; the best result images are often in the second half of an article.
- After picking, preview the real crop used in the video with `images.py crop`, then decide the `objectPosition`.
- **Real screenshot quota**: at least 1 real interface screenshot or real work image per feature segment, and no fewer than 8 across the whole video; also include one fast-cut montage made of 8 or more real work / project screenshots.
- **Screenshots must be usable at 4K**: capture with `python3 scripts/shot.py <url> <name>` at 1920×1080 @2x, giving 3840×2160. For pages that need a login, run `shot.py --login <url>` first and ask the user to log in in the window that opens and then close it. For other capture methods (DevTools MCP, re-rendering a built-in browser snapshot), see the "Real interface screenshots" section of `references/asset-sourcing.md`.
- **Screenshots placed in the frame must keep their original aspect ratio**: use the template's `src/components/BrowserFrame.tsx` (set `ratio` to the source image width / height). Screenshots were once all squashed horizontally because Tailwind's `img { max-width: 100% }`; the template's `src/index.css` has already fixed this.
- Code-redrawn cards are only for cases where "the information in a screenshot is too small and needs to be enlarged for emphasis," and they must appear right next to the corresponding real screenshot.

### 5. Music and beat grid

Follow `references/music-and-beats.md`. **When the user has a paid ElevenLabs account, prefer composing from the storyboard** (sections 0 and 6: write the opening mood, drops, breakdowns, and climax into a segment plan, generate 2 versions, measure the real structure, then make the visuals follow the music). With no account, use a library: search 6–10 tracks by style → `music.py analyze` to shortlist 3–4 that **hit a drop at 4–5 seconds (the opening mood segment may have no drums) and have 2 or more drops across the track** → cut 30 seconds of each and normalize loudness to -14 LUFS.

Whichever source you use, put the candidates in `project/out/music-candidates/` and **ask the user to listen and sign off** (you can combine this with the login-screenshot round) → after a choice is made, use `music.py grid` to get exact beats → `music.py bars` to see the energy per bar.
- If the intro is too long, cut in 1–2 bars before the drop (`musicOffset`); do not make the audience wait.
- Prefer tracks with beat consistency ≥ 0.9, so fast-cut beats land accurately.

Scene boundaries fall on bar lines or half-bar lines; write `beat / bar / drop / musicOffset` into timing.json, and put each scene's internal pacing parameters (card interval, per-item reveal step) into `pace`, so that **the visual code and mix.py read the same set of parameters** and stay in sync when pacing changes.

### 6. Storyboard and production

- Write the storyboard table first (it can go at the end of `requirements.md` or in `research-notes.md`): scene / start and end time / visuals / on-screen text / assets / sound-effect points.
- One component per scene, taking absolute time `t` and returning `null` outside its time window (see the template's own `src/scenes/Example.tsx`). The animation helpers are in `src/lib/anim.ts`: `ramp / keys / impulse / shake / typed / beatAt`.
- Register assets that need web preloading in `src/assets.ts`.
- To place a downloaded demo video in the film, use `src/ui/Clip.tsx` (plays by absolute time, can start from the Nth second of the source video, can change speed, muted by default); first re-encode the source video with the ffmpeg command in the component's comment (`-g 30` is required for exact frame seeking).
- Every piece of on-screen text must satisfy "Pacing: floors + density" (below). Prefer deleting words or splitting scenes over making the audience fall behind; at the same time every bar needs something new, so prefer splitting into more short scenes over stretching one layout for a long time.

### 7. Narration and mixing

**Narration** (follow `references/narration.md`; needs ElevenLabs; skip this section if the user chose a music-only plan): write the narration script into `voice.lines` in `timing.json` (each line has `at / end / text / say`, fitted into the scene time window within a character budget) → **listen to voices**: 3 candidates (if the account has the user's own cloned voice, count it as one; pick the rest from the voice library) each read 3 representative lines, ask the user to choose → generate and verify with one command:

```bash
python3 scripts/elevenlabs.py vo              # generate line by line (default eleven_v4; if a cloned voice is not trained for that model the script exits and lists the available models) + trim silence + auto speed-up on overrun + Scribe transcript comparison + brand-word check + tail measurement; all must be OK
python3 scripts/elevenlabs.py vo --takes 4    # when a cloned voice articulates unsteadily: generate up to 4 takes per line and keep the one that transcribes most accurately
```

- **Always put brand names and URLs into `voice.keywords`**: whole-sentence similarity will let a brand name with one or two wrong characters pass, while a word in `keywords` fails as soon as it is missing.
- When a cloned voice has no v3 / v4 training and the script has a brand name mixed with English, use `"model": "eleven_v3", "sts": true`: v3 reads accurately, then converts back to the person's own timbre. If you change the model, voice settings, or `sts`, give the user 3 sample lines first before generating everything (see section 2 of `references/narration.md`).
- **Do not write your own generation script to bypass `vo`**: if the project has no `elevenlabs.py`, run the template sync in step 10 first.

`scripts/mix.py` is this project's cue sheet and calls `scripts/audiolib.py`. For how music enters, builds, and how sound effects align with visual events, see `references/music-and-beats.md`. When there is narration, the music is automatically ducked according to `duck_curve`, and `vo_margin` is printed at runtime (each narration line must sit at least 8 dB above the music). After mixing, run `python3 scripts/mix.py --env` to see the loudness curve; with narration, also run `python3 scripts/elevenlabs.py check-mix` to transcribe the finished mix (overall match ≥ 0.97, every line audible, and URLs checked especially carefully).

### 8. Verification loop (automatic, do not skip)

Follow `references/verification-checklist.md`. Each round:

```bash
npm run fonts && npm run mix && npm run check:assets && npm run lint
node scripts/stills.mjs --scenes && python3 scripts/sheet.py      # open out/sheet.jpg and review image by image
```

When review finds a problem → fix → re-capture, until the checklist fully passes. At key transitions, add screenshots at specific moments (`node scripts/stills.mjs 11.4 11.6 …`).
Once everything passes, render a `npm run render:preview` and watch it through quickly.

### 9. Export and delivery

```bash
npm run render:4k        # or render:1080, per the confirmed spec; the log is written to out/render.log
python3 scripts/check_video.py out/final-4k.mp4 --scale 2      # must be 0 ERROR, and open the frame-extraction contact sheet to look it over
```

- Copy the finished video to the project directory `<output dir>/<project name>/` with a matching name (`promo-4k.mp4`); if a web version is wanted, run `npm run web:build` and copy `out/web` to `web/`.
- Run the 4K render in the background and poll progress; you can write the delivery notes while it renders. Times vary widely: a ~50-second film can take about 4 minutes at best, while a ~70-second film with many large images on screen and heavy effects takes 12–18 minutes.
- Do not run file-generating commands (`mix`, `render`, `fonts`) inside `<tool dir>/template`, or the artifacts will be copied into every future new project; if you want to try something, copy it to `/tmp/x` first and run there.
- When only the audio changed (voice swap, narration edit, mix tweak) there is no need to re-render: after `npm run mix`, swap `public/audio/mix.wav` into the finished video with ffmpeg (`-c:v copy`, see section 6 of `references/narration.md`), then run the finished-video gate.
- When the user says "run it" or wants to see the result, **open only one playback source** (either the MP4 or the web version, not both). Playing both at once sounds like an echo. Close test pages as soon as you are done testing.
- Serve the web version with `npm run web:serve` (`out/web`, port 18765), or run `npx -y http-server . -p <port> -a 127.0.0.1 -c-1` under `web/`, then open it in the **system browser** (macOS `open`, Windows `start`, Linux `xdg-open`). http-server supports Range requests while `python3 -m http.server` does not, so audio cannot be read on demand. Do not let the user listen inside the AI tool's built-in browser: in one case not a single sound played there. First check whether the port is taken (`lsof -i :<port>`): if another project occupies it, use a different port rather than stopping someone else's service.
- When narration is added for the first time, keep the previous no-narration version as `promo-4k-music-only.mp4`; later, when changing the music, produce `out/mix-music.wav` with `python3 scripts/mix.py --no-vo` and swap it in.
- When the user reports "echo / doubled voice," troubleshoot in the order in section 7 of `references/narration.md`, and first work out whether the problem is in the file or in the player.
- Reporting: state the result first (file location, spec, duration), then the key creative decisions, and finally list **the points the user must confirm in person** (especially sound—the AI cannot hear audio and can only rely on waveform analysis).

### 10. Revision (when feedback arrives)

Pitfalls in revision all come from "the project and the docs stayed on the previous version":

1. **Record the exact words in the revision log of `requirements.md`**, then write the plan. If the user repeats the previous round's feedback in a new message, check first whether it has already been handled, state the current status of each item when reporting, and do not redo it as a new issue.
2. **Sync the template first**: `python3 scripts/sync_template.py` lists generic scripts and web playback logic that differ from the template (the template may have had bug fixes or new features since the project was copied); after confirming the differences, use `--apply`. If an old project lacks this script, copy it over from the template first.
3. **Decide which steps to redo based on the scope of the change**:

   | What changed | What to redo |
   |---|---|
   | Only audio (narration script, voice, mix) | Step 7 → swap the audio track without re-rendering (step 9) |
   | Music swap | Re-measure beats in step 5 → align scene times to the new track → steps 6–9 |
   | Scene added, removed, or reordered | Steps 6–9; **rewrite `mix.py` for the new storyboard** (it references scene names and pace, so an old cue sheet will not match the new visuals) |

4. **Keep the docs with the current version**: replace the "final storyboard" in `requirements.md` with the new version (add a narration column if there is narration), and update the music and narration sources in `research-notes.md`.
5. **Back up the old finished video** to `project/out/v<N>/` first, then copy the new version to the project directory.
6. **Update `project/out/handoff-summary.md` every round**: current deliverables, a structural summary of `timing.json`, the generation pipeline for narration and screenshots, verified data, and key files. Revisions often span several days with the context compacted several times, and later work must be able to pick up from this summary and the project files alone.
7. **If the same thing is rejected twice, stop deciding it yourself**: the AI cannot hear and cannot judge "whether it feels right." When your own music choices are rejected twice, widen the styles, produce 5–6 candidates layered with the narration for the user to pick from; usually one round settles it.

---

## Pacing: floors + density

Two opposite pieces of feedback: a 64-second film was called "too fast, the audience can't keep up" (fast cuts at 0.45 seconds, no time to read); later, several 73–78-second films were called "slow-paced" (long opening build-up, repeated layouts, idle camera fly-throughs). Conclusion: **"fast / slow" is not determined by the number of seconds, but by whether the text can be finished reading (floors) and whether there is something new on screen (density)**. Both must be satisfied.

**Floors** (so the text can be read):

| Content | Minimum dwell |
|---|---|
| Named showcase shot (headline feature / work) | 1.3 seconds |
| A single shot in a fast-cut montage | 0.65 seconds (below this it can only be atmosphere; do not count on the audience reading text) |
| An information scene with one screen title + a set of cards / data | 3.5 seconds (can be shorter with little text; split the scene when there are many cards rather than making it longer) |
| URL, QR code, CTA | 3 seconds or more, placed at the film's highest climax, and not only at the end |
| Elements appearing one by one | Interval ≥ 0.3 seconds; hold at least 0.8 seconds after all have appeared |
| Fast cuts with large text layered in the opening | At most 2 shots in the first 4 seconds (each ≥ 2 seconds); text appears line by line, holding at least 1.5 seconds after the last line appears |
| Multiple focal points in one shot (a push from A to B) | Each focal point ≥ 1.4 seconds (excluding travel time); two focal points + two lines of text need at least 4 seconds, so do not squeeze them into 2 |

**Density** (so the visuals don't drag):

| Rule | Requirement |
|---|---|
| Opening | A pain point or core highlight within 3 seconds, the first high-energy moment within 5 seconds |
| New-information interval | From any moment, within the next bar (about 2 seconds) there must be new information or an obvious visual event; a pure transition / camera fly-through ≤ 0.6 seconds |
| Layout repetition | Use the same layout at most 2 times in a row; rotate layouts across parallel feature segments (full-page scroll, multi-image collage, zoom-in focus, split-screen comparison…) |
| Single-scene duration | Except for the climax and the CTA, a single scene ≤ 2 bars (about 4 seconds); split long content into two scenes with different layouts |
| Total duration | 45–60 seconds by default |

---

## Tech stack

- **Remotion 4 + React 19**: deterministic frame-by-frame rendering, exportable at 4K60; the same set of components plays live in the browser via `@remotion/player`.
- **Python (numpy / scipy / Pillow / fontTools / Playwright) + ffmpeg**: mixing, beat analysis, asset processing, web screenshots, font subsetting, finished-video checking. Dependencies in `<tool dir>/template/requirements.txt`.
- **ElevenLabs** (optional; official skills: `text-to-speech` / `music` / `sound-effects` / `setup-api-key`): v4 narration, composition from the storyboard, custom sound effects, and Scribe transcript verification. Put the key in the workspace root `.env` (per `.env.example`; in clone mode that is the repository root) or the `ELEVENLABS_API_KEY` environment variable, shared by all projects; if a single project needs a different key, put it in its `project/.env`.
- **Mixkit** (free, commercially usable library): the music and sound-effect source when there is no ElevenLabs.
- Generated images: the AI tool's own image generation (style sample frames, backgrounds, characters, 3D logos); when there is none, draw with code.

## Script quick reference (source files in `<tool dir>/template/scripts/`; after copying into the project, run them from the project workspace)

| Script | Purpose |
|---|---|
| `doctor.py` | Environment check: Node, ffmpeg, Python dependencies, Playwright, Chinese fonts, ElevenLabs key |
| `shot.py` | Open a URL and capture a 4K page image at 1920×1080 @2x (`--scroll` for multiple screens, `--tall` for a long image, `--hide` to hide banners, `--login` to let the user log in once) |
| `images.py` | `grab` batch-download document images · `sheet` build a contact sheet per document · `crop` preview the crop for the target aspect ratio · `prepare` downscale into public · `info` check dimensions |
| `music.py` | `search/get` Mixkit music and sound effects · `analyze` structure and BPM · `grid` exact beats · `tempo` for trailer-style compositions where grid is unreliable, measure BPM by autocorrelation · `bars` per-bar energy table |
| `elevenlabs.py` | `vo` generate and verify narration from timing.json (`voice.keywords` brand-word check, `voice.sts` conversion back to the person's own timbre, `tail_ms` echo check) · `check-mix` transcribe the finished mix and compare · `voices` list voices · `music` compose in segments · `sfx` sound effects · `stt` transcribe · `quota` quota |
| `audiolib.py` / `mix.py` | Mixing library / this project's cue sheet (`--env` prints the loudness curve; `voice_lines` / `duck_curve` / `vo_margin` handle narration; `splice` stitches the music on bar lines per the `music` table in `timing.json`; `muffle` low-passes a stretch to create a quiet passage) |
| `sync_template.py` | When revising or continuing an old project, list the generic scripts / web playback logic that differ from the template; `--diff` to see the differences, `--apply` to sync |
| `xgrab.py` | Fetch an X post's metadata + original images and video by tweet id (fxtwitter public API, no login, follows the system proxy automatically) |
| `snapshot.js` / `snapshot.py` | Export a self-contained HTML from an already-logged-in page / re-render it locally at 1920×1080 @2x into a 4K screenshot (use when the user is already logged in via the AI tool's built-in browser) |
| `fonts.py` | Subset fonts per `fonts.json` and report missing glyphs |
| `stills.mjs` / `sheet.py` | Render screenshots at given moments or for each scene / assemble them into a contact sheet with scene names |
| `check_assets.py` | Pre-render gate: missing files, images too small or too large, missing fonts |
| `check_video.py` | Finished-video gate: spec, errors in the render log, loudness, per-scene frame extraction |

## Reference docs

| Document | When to read it |
|---|---|
| `references/requirements-interview.md` | Step 2: what to ask, how to ask, and the requirements.md template |
| `references/style-directions.md` | Step 2: the menu of styles and narrative structures (a menu, not defaults) |
| `references/asset-sourcing.md` | Step 4: sources and methods for product assets, web screenshots, icons, fonts, AI-generated images, and music and sound effects |
| `references/music-and-beats.md` | Steps 5, 7: ElevenLabs composition and sound effects, track selection, beat grid, music entry, sound-effect alignment, loudness |
| `references/narration.md` | Step 7: narration voices, script character budgets, generation and transcript verification, ducking the music under the voice, swapping only the audio track without re-rendering, echo troubleshooting |
| `references/verification-checklist.md` | Steps 8, 9: automated gates + the image review checklist |
| `references/pitfalls.md` | Skim before starting; check here first when something odd happens |
| `references/case-retrospectives.md` | Read once before starting: each of the 5 delivered films' style, feedback, and fixes, plus the real shape of the `music` stitch table and `voice` narration table in `timing.json`. **Learn the methods only; do not copy the styles** |
