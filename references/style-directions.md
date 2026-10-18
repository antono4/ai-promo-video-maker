# Style directions and narrative structure menu

This is a **menu, not defaults**. Every product must be recombined based on its character, audience, and assets, and signed off by the user after seeing sample frames. You can mix and match, and you can invent directions outside this menu.

Answer three questions first when choosing a direction:
1. **What is the product's character?** (professional and reliable / young and playful / high-end and restrained / geeky and hardcore / warm and companionable)
2. **What is the most persuasive material?** (real interface screenshots / finished works / data / user stories / a character IP)
3. **Where will the audience watch it?** (Bilibili landscape / TikTok vertical / looping on a site's home page / a big screen at a launch event)

---

## Style directions

Each direction lists: what products it suits, visuals, motion, fonts, sound, and implementation notes in Remotion.

### Movie trailer (used by the Vibe Coding course)
- Suits: products that want a "big event" feel, courses, platform products.
- Visuals: dark, volumetric light, film grain, vignette, widescreen black bars, one brand color + one accent color.
- Motion: strong contrast from stillness → burst; push-ins and pull-outs, 3D perspective, impact white flashes, screen shake, fast-cut montage.
- Fonts: heavy geometric display type (Alimama ShuHeiTi / Smiley Sans) + PingFang body text.
- Sound: suppressed intro → build-up → impact drop, with plenty of risers / whooshes / low-frequency impacts.
- Implementation: `impulse` for white flashes and impact scaling, `shake` for screen shake, CSS 3D (perspective + rotateX/Y) for camera motion.

### Chibi cartoon / mascot
- Suits: tools and apps for the general public, young people, and students; products with an IP character or that can design one.
- Visuals: highly saturated candy colors, thick outlines, rounded corners, big-head small-body characters, sticker-like elements, white or light background.
- Motion: bouncy (`EASE.back` / Remotion `spring`), squash and stretch, character expression changes, elements "popping" in, lively pacing.
- Fonts: rounded or handwritten-feel heavy type (ZCOOL KuaiLe, Smiley Sans in rounded scenarios, Alibaba PuHuiTi Heavy).
- Sound: upbeat ukulele / whistling / electronic pop, with "pop," "ding," and "whoosh" sound effects.
- Implementation: finalize one main character with an image generator first, then use it as reference to generate multiple expressions / actions (keeping the same character), as transparent PNGs; animate the character's breathing, jumping, and swaying loops with transforms.

### Apple keynote minimal
- Suits: products with a strong sense of design and high-end positioning, hardware, professional software.
- Visuals: large areas of pure white or pure black with generous whitespace, a single focal point, oversized titles, the product interface or physical object centered, very thin lines.
- Motion: slow, precise, restrained; large text appears word by word, the interface slides in smoothly, almost no flicker or shake.
- Fonts: PingFang / SF style, with contrast between large sizes and light weights.
- Sound: piano or ambient electronic, a small amount of refined sound effects.
- Implementation: long `EASE.inOut` easing, one thing per screen; note that the pacing floors still apply.

### Interface capture (product tour)
- Suits: SaaS, productivity tools, and developer tools where the features are the selling point.
- Visuals: real interface screenshots placed in device frames / browser frames, magnifier focus, cursor clicks, highlight boxes.
- Motion: simulate real operations—typing, clicking, dragging, results appearing; the camera follows the cursor and pushes in.
- Fonts: the interface's own font + concise caption text.
- Sound: light electronic, with keyboard and click sounds aligned to each operation.
- Implementation: `typed()` for character-by-character typing; rebuild screenshots in layers (background + movable cards), which is far more vivid than one static screenshot.

### Hand-drawn doodle / whiteboard explainer
- Suits: products that explain a concept, education, warm and approachable brands.
- Visuals: paper texture, hand-drawn lines, marker color blocks, handwriting.
- Motion: line drawing (SVG stroke-dashoffset), elements that look drawn into existence, a slightly jittering frame-by-frame feel.
- Fonts: handwriting.
- Sound: acoustic guitar, the rustle of pen strokes.
- Implementation: `@remotion/paths`'s `evolvePath` for drawing lines; use `random()` + the frame number for "boiling line" jitter.

### Pixel retro / 8-bit game
- Suits: games, developer communities, geek-oriented products, fun tools.
- Visuals: pixel type, low-resolution palettes, CRT scanlines, game UI (health bars, XP, levels).
- Motion: frame-by-frame jumps (no smooth tweening), pixel explosions, "LEVEL UP."
- Fonts: pixel fonts (Zpix and other open-source pixel Chinese fonts).
- Sound: chiptune, 8-bit sound effects.
- Implementation: quantize `t` to 12fps before computing animation, `image-rendering: pixelated`.

### Cyberpunk neon
- Suits: AI, security, hardcore tech products.
- Visuals: neon on black (magenta / cyan), glitch, scanlines, HUD interfaces, code rain.
- Motion: RGB separation, flicker, sliced displacement, HUD numbers rolling.
- Sound: dark synths, glitch sound effects.

### Magazine layout / Swiss graphic design
- Suits: content products, media, products with a strong brand feel.
- Visuals: grid systems, large type-size contrast, color blocks, cropped photos, numbering.
- Motion: sliding and shifting blocks, text reveal masks, color-block wipe transitions.
- Sound: rhythmic lo-fi / jazz / house.

### 3D clay / toy texture
- Suits: lifestyle, family and kids, warm and cute products.
- Visuals: clay or plastic-textured 3D scenes and characters (produced by an image generator), soft shadows, shallow depth of field.
- Motion: stop-motion feel (10–12fps jitter), bouncy.

### Chinese retro / ink wash
- Suits: culture, Chinese style, digital products in traditional industries.
- Visuals: ink wash bleeding, rice paper, seals, vermilion accents, vertical text.
- Motion: ink-spread masks, scroll unrolling, brush-drawn characters.

### Kinetic typography
- Suits: products with no good assets whose selling point rests on a single line; also works as a segment inside other styles.
- Visuals: text only, creating impact through size, weight, color, and arrangement.
- Motion: characters popping in, scale impacts, words pushing each other apart, text changing with the beat.

---

## Narrative structures

Also a menu. When recommending to the user, write it as **this product's concrete version** (what goes in each segment).

| Structure | Flow | Suits |
|---|---|---|
| Pain point → turn → proof → call to action | "Are you also…" → "Now all you need is…" → a barrage of features / works / data → URL | Most tools and courses (Vibe used its variant: hook → one sentence becomes a product → works → content overview → free → logo) |
| One-take product tour | The camera travels continuously through the product's interfaces | SaaS with good-looking interfaces and coherent features |
| Character story | A character hits a problem → uses the product → life changes | Chibi, apps for the general public |
| Before / after | The same thing: before use vs after use, split screen or re-enacted | Productivity-improvement products |
| Number barrage | A string of striking numbers + visual evidence | Platforms and open-source projects with impressive data |
| Countdown / challenge | "Build an app in 10 minutes" with a timer | Products that emphasize speed and simplicity |
| Testimonial collage | Real reviews, screenshots, danmaku flying past | Products with good word of mouth (testimonials must be real) |
| Event / leak | One sentence on what happened → "so what actually happened" → how it was discovered → how it was verified → the results shown off → the current official status → what you can do | A new model in limited rollout, a product leak, an event that just broke out (Claude Fable 5.5 used this) |

**Suspense cannot replace explanation**: the first version of Fable opened with "it's labeled Fable 5.1, but the answer isn't it?"; insiders found it clever, but outsiders had no idea what it was talking about. First explain the event in one plain sentence ("Fable 5.5 hasn't been released, yet some people are already using it"), and put the suspense after "what happened." Each narration segment should ideally start by connecting to the end of the previous one ("how was it verified?" "the people who switched started showing off their work"), so the audience can keep up.

## General quality checklist (consider regardless of style)

- **Style is the packaging; real screenshots are the star**: every style must leave the main picture area for real interface screenshots and real works (browser window frames, phone frames, manga panels, pixel screens… can all be containers for screenshots), with style elements handling transitions and atmosphere.
- **Open straight into a pain point or highlight**: style setup cannot take up the first 3 seconds.
- The picture needs **layers**: background layer / subject layer / foreground accents; do not paste one image across the whole screen.
- **Combine motion and stillness**: every scene needs at least one continuous micro-motion (slow push, floating, breathing) to avoid dead frames.
- **Design the transitions**: match the style (impact white flash / wipe / mask / object passing through) and align them with the music's downbeats.
- **Enough contrast between text and background**: light gradient text on a light background and white text overlapping a light effect are both pitfalls we hit.
- **The highest climax must carry the URL / CTA**.
