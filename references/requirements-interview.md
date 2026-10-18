# Requirements interview

You must ask the user before confirming requirements. Goal: with the fewest back-and-forths, clarify every decision that affects the finished video in one pass and write it into `requirements.md`.

## How to ask

- Finish pre-research before asking. Questions and options must be **specific to this product** ("the climax shot is the AI turning one sentence into a budgeting app," not "what should the climax shot show").
- Use a structured question tool (Cursor's `AskQuestion`, Claude Code's `AskUserQuestion`; if you have neither, list numbered options in your reply). 5–8 questions per round, usually done in two rounds. Put the recommended option first, mark it `(recommended)`, and include a one-line reason in the option text.
- Run `doctor.py` before the first round so you know whether the user has an ElevenLabs key and whether screenshots are possible; the options for the sound and screenshot questions must reflect the actual conditions.
- When the user answers "you decide," make the call yourself, but state your decision and reasoning in `requirements.md` so the user can see it at the confirmation step.
- If the user adds free-form text (e.g. "don't worry about licensing" or "I don't want my own voice"), record their exact words in `requirements.md`.

## Step zero: ask about positioning first when the product's status is unclear

When pre-research finds that the product **has no official source** (not released yet, only a rumor of a limited rollout, version number that does not match), ask this one question separately before the first round, because it determines how all the later assets and facts are used:

| id | Question | Options |
|---|---|---|
| direction | The official release hasn't happened. How should we make the video? | Prepare the style, music, and framework now and fill in official data on launch day (recommended) / Cover the already-released version / Cover an already-released model in the same family plus an ending teaser / Make an "early look" now: use only user-verified tests, cite a source for each, and label the whole video "unofficially confirmed" / The user has a reliable information source of their own |

If "early look" is chosen: keep a "user-tested · unofficially confirmed" marker on screen throughout; do not state any official benchmark, price, or feature claim; and end with a real screenshot of the official news page to show that "officials haven't confirmed it yet." If more than half a day passes between starting and delivering, re-verify the official status and any new cases.

## Round one: set direction

| id | Question | Common options (rewritten per product) |
|---|---|---|
| deliverable | Deliverable | MP4 + a web version from the same source (recommended) / MP4 only / web only |
| format | Aspect ratio and duration | 16:9, about 45–60 seconds (recommended) / 30-second fast cut / 70–90-second full version (reason required) / 9:16 vertical preferred / both landscape and vertical |
| hook | Opening hook (within 3 seconds; the first line must be understandable to someone with no background at all) | Pain-point entry: hit with the target user's 2–3 most real pain points in quick succession (recommended; write out this product's specific pain points) / Core-highlight entry: reveal the most striking number or work in the first second / Result entry: show the final outcome first, then flash back |
| audience | Primary audience | List 2–4 audience groups for the product + the average coverage |
| style | Style direction | **3–4 directions specific to this product, with style sample frames** (see below) |
| story | Narrative structure | Pick the 2–3 most suitable from the narrative menu in `style-directions.md` and write them as this product's concrete version. For each option write out the "first narration line" so the user can judge whether an outsider would follow it |
| hero | Climax shot | The one shot that best conveys the product's value; list 2–3 concrete options |
| audio | Sound | **With an ElevenLabs account**: compose from the storyboard + v4 narration (recommended) / music-only beat cuts + large text / the user's own recording / a single line in the user's own voice at the end. First check the account's plan and voices with `elevenlabs.py quota` and `voices`. **Without an account**: library music with beat cuts + large text (recommended) / the user's own recording / sign up for ElevenLabs now and put the key in the workspace root `.env`. **The voice is not decided in this round**: after the narration script is written, have 3 candidates (if the account has the user's own cloned voice, count it as one; pick the rest from the voice library) each read 3 representative lines, put them in `project/out/voice-candidates/`, and ask the user to listen before deciding (a cloned voice was called "odd-toned" in the Fable film and also transcribes most easily with errors). If the user gives a voice ID directly, use it and skip the candidates; but if that voice is not trained for the default model, say in your report which model you switched to |

### Style sample frames (mandatory for the `style` question)

1. Pick or invent 3–4 **clearly distinct** directions from `style-directions.md`, at least one unconventional (chibi / hand-drawn / pixel / clay / Chinese retro…). Do not make all four variants of "dark tech."
2. Produce one 16:9 sample frame per direction: put this product's real name, one real line of copy, and one representative element in the frame so the user sees "what this looks like on my product." Use an image generator if you have one (Cursor's `GenerateImage`, Codex image generation, etc.); if not, draw a 1920×1080 page in HTML/CSS and capture it with `python3 <tool dir>/template/scripts/shot.py file:///<absolute path>/A.html A --out "<output dir>/<project name>/style-frames"` (styles code can draw: minimal, typographic, pixel, neon, interface capture; for styles that need characters or illustrations, indicate with emoji / SVG and explain how the finished video will achieve them).
3. Assemble them into one image with `python3 <tool dir>/template/scripts/sheet.py --dir <style frame dir> --cols 2 --width 800 --out <style comparison.jpg>` (or show them one by one), embed the image in your reply, and only then ask the question. Put the sample frames in `<output dir>/<project name>/style-frames/` (the project has not been created yet at this point).
4. The user can mix and match ("A's palette + C's characters"); note it down.

## Round two: set details

| id | Question | Common options |
|---|---|---|
| assets | Asset copyright boundaries | Loose and compliant: own assets + AI-generated images + commercially usable music, third-party logos used only for reference (recommended) / Strict: no third-party logos, CC0 music / Looser: the user bears the risk |
| showcase | Features / works to highlight | List the candidates found in pre-research, multi-select; ask whether anything must appear or must be excluded |
| screens | Real screenshot sources | Public pages + work images in posts / docs (recommended to take full stock first and tell the user how many can be obtained) / pages that need a login: ask the user to log in in a Chrome window / the user provides screenshots or screen recordings directly |
| music | Music | Give 3–4 thirty-second samples (`project/out/music-candidates/`) and ask the user to choose; or ask about style preference (electronic / funk / inspiring epic / upbeat pop) / the user brings their own track |
| cta | URL and call to action | Which URL to write, where to put it (at least once at the highest climax + at the end), and the button text |
| credit | Author / brand endorsement | Cover in depth / mention in passing / do not show |
| web | Web version | Run locally (recommended to start here) / deploy to EdgeOne Pages / Vercel / embed in an existing site |
| review | Mid-production review | Fully automatic through to delivery after requirements confirmation (default) / rough cut first, then polish / still-frame storyboard first |
| export | Export spec | 4K60 + 1080p60 (recommended) / 1080p60 / 4K30 |

The last question is always:

| confirm | Is the consensus above accurate? After confirmation, fully automatic production begins. | Accurate, start production / Something needs adjusting |

## requirements.md template

```markdown
# <product name> promo video · requirements confirmation

## Product
- One-sentence positioning:
- Target users:
- Core selling points (by importance):
- Provable data (with sources):
- URL / download entry:

## Decisions
| Item | Decision | Notes (user's exact words / my reasoning) |
|---|---|---|
| Deliverable | | |
| Aspect ratio and duration | | |
| Audience | | |
| Style direction | | attach sample frame file names |
| Narrative structure | | |
| Climax shot | | |
| Sound | | |
| Asset copyright boundaries | | |
| Highlighted features | | |
| URL and CTA | | |
| Author endorsement | | |
| Web version | | |
| Review method | | |
| Export spec | | |

## Style notes
- Color palette:
- Fonts:
- Motion language (pacing, easing, transition style):
- Texture (grain, light effects, outlines, shadows…):
- Explicitly not wanted:

## Narrative and storyboard (first draft; refined during production)
| Segment | Duration | Visuals | On-screen text | Audio |
|---|---|---|---|---|

## Revision log
- (append each round of user feedback and the outcome here)
```
