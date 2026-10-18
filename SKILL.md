---
name: promo-video-maker
description: Make a promo video with commercial polish (4K MP4 + web version) for a product, website, app, SaaS, open-source project, course, AI model, or event. The pipeline covers research, requirements interview, style sample frames, real 4K page screenshots, music with beat cuts, AI narration, mixing, and automated verification. Use it when the user says "make a promo video," "make a product intro video," "make a promotional video / trailer," "make a video for this project," or asks for a promo video, product trailer, or launch video.
---

# Product Promo Video Maker

The complete working specification is `AGENTS.md` in this same directory. Before starting any work, read it from beginning to end with a file-reading tool, then follow it strictly; the detailed method for each stage is in the `references/` directory alongside it, to be read on demand as AGENTS.md directs.

When invoked as a Skill, the paths map like this (the "Two usage modes and path conventions" section of AGENTS.md explains this fully):

- `<tool dir>` is the directory containing this `SKILL.md`, where `template/` and `references/` also live.
- `<output dir>` is `promo/` under the current workspace root. Write all project files there, never into `<tool dir>`.

The first step is always the requirements interview: do not start production before confirming the requirements with the user.
