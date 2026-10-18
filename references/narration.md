# Narration (ElevenLabs voiceover)

When the user has an ElevenLabs account, narration is added to the promo video by default, so that someone who has never seen the product can keep up by **listening** too. The whole pipeline is generated with one command plus two automated checks, and since the AI cannot hear sound, **every judgment relies on transcription and level measurement**.

## 1. Preparation

- Install the official skill: `npx skills add elevenlabs/skills@text-to-speech -g -y` (composition and sound effects are in section 6 of `music-and-beats.md`).
- Put the key in the workspace root `.env` (per `.env.example`, `ELEVENLABS_API_KEY=...`) or set it as an environment variable, shared by all projects; do not let the user paste it into chat. Use `python3 scripts/elevenlabs.py quota` to see the plan and quota.
- The default model is `eleven_v4` (good Chinese, most natural). **v4 does not support speed or style**: the speaking rate cannot be adjusted, so the only way to fit each line into its time window is to control the character count.

## 2. Choosing a voice

`python3 scripts/elevenlabs.py voices --zh` lists the voices in the account and the popular Chinese voices in the voice library.

1. **First check whether the account has a cloned voice belonging to the product's author or brand** (the ones whose category is `professional` or `cloned` in the `voices` list). If so, include it in the listen candidates, but **do not use it by default**: the Claude Fable 5.5 film used the author's own cloned voice throughout, and after listening the user said "a lot of the tones are a bit off," and was only satisfied after switching to Haoran from the voice library; on the same script, the cloned voice transcribed at 0.968 in the mix while Haoran was 1.000. A professional cloned voice must be trained per model, and when the state is not `fine_tuned` it returns `voice_not_fine_tuned`, in which case use a voice-library voice first and switch the `voiceId` back and rerun once training finishes (see section 6).
   - Before `elevenlabs.py vo` starts, it automatically checks the training state (`fine_tuning.state` from `GET /v1/voices/<id>`), exits if the voice is not trained for the current model, and lists the models it is trained for. If v4 is not trained but another model is, there are two paths:
     - **Switch to the trained `eleven_multilingual_v2`** (supports `speed` and `style`). It is the steadiest for ordinary Chinese, but **it runs brand names together**: in the Yupi AI Navigation film, "鱼皮 AI" was run together into "pai," heard as "鱼排," and adding commas, quotes, splitting letters, or generating in segments did not help; the sentence-end reverb tail was 90–360 ms, and the user heard an "echo."
     - **Read with `eleven_v3`, then convert back to the person's own timbre** (`voice.model: "eleven_v3"`, `voice.sts: true`). v3 was not trained for the cloned voice; used directly it reads accurately with a tail of only 40–110 ms, but the user said "the voice doesn't sound like mine anymore"; the script then uses the trained `eleven_multilingual_sts_v2` to convert each line back to the person's own timbre. Yupi AI Navigation ultimately used this path, and all 12 lines transcribed correctly.
     - Which to choose depends on the script: if it has brand names, English abbreviations run together with Chinese ("鱼皮 AI," "面试鸭 App"), take the second path; for a pure-Chinese script take the first. Either way, list the brand names and URLs in `voice.keywords` (see section 3).
   - Comparing models does not require editing timing.json: `vo --model eleven_flash_v2_5 --out /tmp/vo-flash --only hook,cta`. Mianshiya compared multilingual_v2, turbo v2.5, and flash v2.5: flash was occasionally the most accurate but varied the most between generations of the same line; multilingual_v2 with high stability was the steadiest.
   - A cloned voice articulates less steadily than a voice-library voice: in the Mianshiya film, at stability 0.5 on multilingual_v2, "一万多道题" was heard as "一模多刀," and only at **0.85** did it stabilize. When generating, add `--takes 4`: generate up to 4 takes per line and keep the one that transcribes most accurately.
2. Otherwise pick 3 candidates (advertising / narration categories, standard Mandarin, an age and gender that fit the style) and test them with the 3 most representative lines:

```bash
python3 scripts/elevenlabs.py vo --voice <voice_id> --out /tmp/vo-<name> --only hook,brand,cta
```

3. Compare objectively: transcript match (all should be 1.00), **the amount of speed-up needed** (closer to 1.0 is better; too much speed-up sounds mechanical), and duration headroom. Give the user the listen files and the comparison; when the user says "you decide," pick the one whose speaking rate best fits the time window and write it into the requirements confirmation.
4. How to assemble the listen files: for each voice, string the 3 representative lines (opening, densest line, climax) into one file, normalize to -16 LUFS, and name the file after the voice's character:

```bash
ffmpeg -i /tmp/vo-haoran/hook.mp3 -i /tmp/vo-haoran/clues.mp3 -i /tmp/vo-haoran/climax.mp3 \
  -filter_complex "[0][1][2]concat=n=3:v=0:a=1,loudnorm=I=-16" "out/voice-candidates/A-Haoran(deep,steady·advertising).mp3"
```

**Listen first, write the full script after**: finalize the voice before generating all the lines. If the voice is changed after the whole film is generated, every line's duration changes and the time windows must be re-laid.

**Changing the model also counts as changing the voice**: the same `voiceId` with a different model (v2 → v3) or with timbre conversion added sounds different. Yupi AI Navigation switched to v3 to fix a pronunciation, and since the transcripts were all correct it went straight to remix and delivery; the user's first feedback was "the voice doesn't sound like mine anymore." So whenever the model, `settings`, or `sts` changes, produce 3 sample lines for the user to confirm before generating everything.

Codefather used Haoran (`pU9NaAwkoR3v0Mrg3uKz`, the "advertising" category in the voice library, deep and resonant): among three candidates only its opening line needed no speed-up.

## 3. Writing the narration script

Write it into `voice.lines` in `src/timing.json`, one line per scene:

```json
{"id": "cta", "at": 50.3, "end": 56.6, "text": "…现在就上 codefather.cn，免费开始！", "say": "…现在就上 codefather 点 C N，免费开始！", "duckDb": -14}
```

- `at` is the moment speech starts (the script trims leading and trailing silence, so the first character lands on `at`), and `end` is the latest the line may finish. Usually start 0.3–0.4 seconds after the scene begins and finish 0.1–0.2 seconds before it ends; start 0.3 seconds after a drop downbeat so as not to fight the hit.
- **Character budget**: v4 Chinese advertising pacing is about 5–6 characters per second (including punctuation pauses). A 4.36-second scene fits 14–18 characters; an 8-second fast cut fits around 30. If it overflows, cut words rather than counting on speed-up (the script auto-speeds up by at most 12%).
- **What is spoken and what is on screen complement each other; do not repeat word for word**: long sentences already on screen can be dropped (Codefather removed "一站搞定" from the narration), and the narration is responsible for tying the picture into one line. Named projects and numbers must really appear in the picture and have a source in the research notes.
- The opening narration follows the opening mood: the pain-point section uses questions ("从哪开始学？项目没亮点？面试总卡壳？"). The place where the music thins out in a breakdown is exactly right for one key line.
- Leave breathing room: after a fast cut and before the climax, leave 1–2 seconds with no speech so the music can come out (Codefather's project wall has 2 seconds without narration).
- **Write brand names and URLs into `voice.keywords`** (e.g. `["鱼皮", "codefather"]`, replaced with your product's brand name and URL body). Whole-sentence similarity lets key misspellings through: the URL line was heard as "语牌 AI 导航，ai.codefather.cn," a similarity of 0.90, which still passes as `OK`, yet what was wrong was exactly the brand name. Once listed in `keywords`, one missing occurrence in the transcript is judged `CHECK_WORD`, and `check-mix` also checks the finished mix against it.
- **A short repeated word at the start of a line easily blurs through timbre conversion**: "试试鱼皮 AI 导航！" transcribed correctly from v3's original audio, but after converting to the person's own timbre, 4 takes in a row became "设置 / 这是 / 就是鱼皮 AI 导航"; changing it to "快来试试，鱼皮 AI 导航！" passed on the first try. Leave one leading word at the start of a sentence and add a comma before the brand name.
- `say` is the text actually sent to TTS, while `text` is the script's original wording: write numbers as Chinese characters ("七十七期"); split URLs and English abbreviations ("codefather 点 C N"; capital letters are the easiest to hear clearly under music).
- Avoid words that repeatedly trip the transcription: homophones ("面经/面镜," "鸭/呀") can be ignored, but words that genuinely cannot be pronounced clearly need rewording. In the Mianshiya film, "大厂" was heard as "大汉," "保精度" as "报警盾," and "对比着学" as "对比招学"; after switching to "真题," "又快又准," and "看懂区别" they all scored 1.00.
- Lines with a very short time window (< 2.2 seconds) are hard to fit reliably, as the speaking rate fluctuates between generations. Merge them with an adjacent line (Codefather merged "数千位同学已拿到 Offer" with the URL line).
- **Sentences with embedded English or numbers are spoken more slowly**: Haoran reads pure Chinese at about 5 characters per second, but only 4–4.3 characters per second with "Fable 5.1" or "Tibo" mixed in. Budget these at 4 characters per second (count English words and "五点一" as 2–3 characters). When over, cut filler like "验证方法是" or "自己," and drop information already on screen (a date, "不联网") from the narration.
- **Words that would become a false fact when misheard must be changed**, not waved through as homophones: "一上线" was heard as "已上线" (turning into "Fable 5.5 已上线"), "五点五一正式发布" was heard as "5.51," and "最炸" as "最渣." Reword to something unambiguous: "等它正式发布," "最绝的是." Do not follow a number immediately with a word starting with "一" or "已."
- **Words a cloned voice tends to blur**: the sentence-final "五点五" (heard several times as "无电雾"), "路由" ("绿油"), "十月" ("日月" once mixed into the music), and "暗号" ("然后"). With a cloned voice, reword these spots or simply drop them from speech and let the screen carry them.

## 4. Generation and verification

```bash
python3 scripts/elevenlabs.py vo        # generate everything; lines whose text, voice, and model are unchanged use the cache and do not consume quota again
```

Each line will: generate (with the previous and next lines as context; v3 does not support this parameter and skips it automatically) → convert back to the person's own timbre if `sts` is on → trim leading and trailing silence → speed up on overrun (≤ 1.12) → transcribe and compare with Scribe → measure the sentence-end tail. Output:

- `OK`: fits in the time window and the transcript matches the script.
- `TOO_LONG`: still does not fit after speeding up to 1.12; cut words or widen the time window.
- `CHECK_TEXT`: the transcript does not match (match < 0.85). Fix `say` against what was heard. Arabic and Chinese-character numerals are converted automatically, so there are no false alarms there.
- `CHECK_WORD`: a brand name or URL in `keywords` was not heard. Rerun first (it regenerates automatically), and if it still fails, switch the model per section 2 or add commas around the brand name.
- `ECHO`: the sentence-end decays from -20 dB peak to -45 dB over more than 250 ms, which sounds like an echo under music. Switch the model (v3 + `sts`) or the voice.

Only when all are `OK` does mixing begin. Results are in `audio-src/vo/report.json`. When you rerun `vo` directly, lines that failed the previous round (except `TOO_LONG`) are regenerated automatically while passing ones use the cache; the multi-take selection with `--takes 4` happens **after** timbre conversion, because the conversion itself can also mispronounce.

**Do not bypass `vo` by writing your own generation script.** The Yupi AI Navigation project was copied before the template added `vo`, and its first narration pass used a self-written `tts.py` that only measured duration without transcribing, so "鱼皮" was heard as "鱼排" and the user caught it. If a project lacks `scripts/elevenlabs.py`, copy it over from `<tool dir>/template` first (see step 10 "Revision" in AGENTS.md).

## 5. Mixing

In `mix.py`: `voice_lines(TM, rmsDb)` reads and normalizes each line's loudness, `duck_curve(...)` generates the gain curve that ducks the music while speech plays, the music is placed with `place(..., duck=duck, tag="music")`, and the narration with `place(..., tag="voice")`. The template's `mix.py` already has this written.

- Defaults are `rmsDb: -13` and `duckDb: -9` (duck attack 0.08 seconds, release 0.35 seconds). The most important line (URL / CTA) gets its own `duckDb: -14`, with the high-frequency sound effects at that moment (flash, confetti) halved.
- `mix.py` prints `vo_margin` at runtime: how many dB each narration line sits above the music, and **all are required to be ≥ +8 dB**. Codefather initially used -18 / -7, leaving the voice only 1–2 dB above the music in high-energy sections, where it would be buried.
- Always run this after mixing:

```bash
python3 scripts/elevenlabs.py check-mix    # transcribe the finished mix; overall match ≥ 0.97 and every line audible
```

When the overall match falls a little short of 0.97, compare the transcript with the script character by character: if the remaining differences are all homophones (它/他, 接头/街头), that is acceptable, but list them in the research notes; if even one difference changes the meaning (已/一, 渣/炸, a number), the script must be changed and regenerated.

Being clearly audible on its own does not mean it stays clear in the mix: Codefather's URL transcribed as "codefather.cn" on its own but became "点 CM" once mixed into the music. It only stabilized after deepening that line's duck, softening the flash sound effect at the same moment, and writing the capitalized "C N."

**Rule out transcription error before touching the mix.** Transcribing the whole film gives a different result every time, so one line not being heard clearly does not mean the mix is wrong. `check-mix` automatically cuts out the lines that were not heard clearly and transcribes them twice more: if both are correct, it was just whole-film transcription error and nothing needs changing. Only when both are wrong should you look for a cause, and **do a control comparison first** (transcribe the same stretch 3 times before and after the change). Mianshiya hit this pitfall: "再精挑" was heard as "带金条" in the mix, and at the time it was thought the riser sound effect was covering the voice, so the sound effect was deleted. A later comparison showed that, with or without the riser, all 3 transcriptions were correct; what actually fixed it was regenerating a take with clearer articulation at the same time. So:
- When a line is genuinely not heard clearly, **regenerate that line first** (delete `raw/<id>.mp3`, run `vo --takes 4`) or reword it; this step is the most common and most effective.
- Only then suspect the sound effects. `vo_margin` only compares the voice with the music and does not count sound effects, but in practice neither full-band nor the 1.5–5 kHz band could distinguish the riser's effect on the voice margin, so rely on control transcriptions to judge. It is still advisable to soften any impact sound effect that coincides with the first spoken character.

## 6. Changing the voice / script later

Only the audio changes; the visuals do not need re-rendering:

```bash
# edit voice.voiceId or a line's text/say in timing.json
python3 scripts/elevenlabs.py vo && npm run mix && python3 scripts/elevenlabs.py check-mix
ffmpeg -i out/final-4k.mp4 -i public/audio/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -shortest out/final-4k-new-audio.mp4
```

Only changes to `at` / `end` require confirming the visual pacing; if the scene times are unchanged, just swap the audio track.

When narration is added for the first time, keep the previous no-narration version as a "music-only version" (`promo-4k-music-only.mp4`), so the user can compare and it can be used in settings where speech is inappropriate. Later, when changing the music, generate `out/mix-music.wav` with `python3 scripts/mix.py --no-vo` and swap it into the finished video the same way.

## 7. How to investigate when the user says "there's an echo / two people are talking"

The AI cannot hear, so rule things out with data in the order below, and **first determine whether the problem is in the file or in the player**:

1. **Are two playback sources open**: the web version + the MP4, multiple browser tabs, or a test page that was not closed. Open only one playback source when "running" it for the user.
2. **Is there a second voice in the file**: count audio tracks with `ffprobe` (should be 1); cross-correlate the narration stem with the finished mix, where there should be no peak above 0.1 besides 0 ms (Codefather measured a maximum of 0.02).
3. **The voice carries its own reverb**: look at each line's `tail_ms` in `audio-src/vo/report.json` (`vo` measures it automatically). Dry speech is < 200 ms; the cloned voice in the Yupi AI Navigation film was 90–360 ms on multilingual_v2 and the user said "the character has an echo," and it was only after v3 + timbre conversion (20–110 ms) that they stopped mentioning it; Shan Shan is about 500 ms. Above 250 ms the script judges `ECHO`; switch the model or the voice. Do not count on ElevenLabs' "Audio Isolation" to de-reverb afterward: it requires audio ≥ 4.6 seconds, and a single narration line errors with 400.
4. **There are vocals in the music**: transcribe the music with `elevenlabs.py stt audio-src/music.mp3`; it should show only tags like `[背景音乐]` and no words.
5. **The player**: if all of the above is normal, the problem is in the web player. Codefather hit two layers: `@remotion/media`'s Web Audio chunks being scheduled repeatedly (about 6 overlapping copies), and the Player pulling the sound back to wait for the picture (replaying half a sentence). The template's `web/App.tsx` has been changed to "use `<audio>` as the clock and let the picture follow the sound"; the verification method is in the web version section of `verification-checklist.md`.

The finished MP4 does not have this problem: its audio track is muxed directly into the file, so the player does not reschedule it.

## 8. Licensing

Narration generated on a paid plan is commercially usable with no attribution; the free plan cannot be used commercially and requires attribution to elevenlabs.io. When a voice-library voice is used, record the voice name and ID in the research notes.
