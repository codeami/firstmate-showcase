# firstmate-showcase

How one person runs a fleet of AI agents like vendor teams: the FirstMate orchestrator, its flow and its human review gates.

This repo is a small static site with five main pages: a short mock chat with the orchestrator, How it works, Skills, Harness flow, and What works today. That last page says plainly what works and what is only designed. Every other page, such as "Agents as vendors", sits under "More" in the menu.

Read it at https://codeami.github.io/firstmate-showcase/

The pages are plain HTML, `style.css` and `nav.js`. There is no build step for them. Open `index.html` from disk to read it locally.

The two interactive maps, `maps/skills.html` and `maps/flow.html`, are built files. Their source is `maps/src/*/map.json` and the shell in `maps/_shared/` comes from [super-board](https://github.com/EricTechPro/super-board) by EricTechPro (MIT; see `maps/_shared/NOTICE`). To rebuild: `python3 -I maps/_shared/build.py maps/src/skills/map.json maps/skills.html` (and the same for `flow`).

The supervisor and most crew mechanics are upstream [Firstmate](https://github.com/kunchenguid/firstmate) by Kun Chen and contributors. See `LICENSE` for this repo's licence.
