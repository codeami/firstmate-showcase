# firstmate-showcase

The Chart Room: how one captain runs a crew of AI agents, safely. By Ashish Raina, program manager turned AI-crew operator. It covers the FirstMate orchestrator, its flow and its human review gates.

This repo is a small static site. The home page, `index.html`, is a plain chat with EA-bot: each turn gives one true fact and three options to click, and any option can be saved to a review-later list, grouped in folders, with a small map that grows as topics are opened. Its script is the `chat` block in `tour/tour.json`. Progress and the list stay in the browser's localStorage. Under the chat, a strip of the day's numbers links to the pages that explain them.

Field Notes, `blog/`, holds the published posts, harness and alignment first. The posts, `blog/index.html` and `arena.html` (the harness arena, lifted from one post) are built from the owner's private drafts by a script kept outside this repo, because its edit list quotes the private strings it removes; edit the drafts and rebuild rather than editing these pages by hand. `safety.html` (Safety by design) and `about.html` are hand-written. All of these use the kit through `article.css` and `article.js`.

Six main pages sit behind it: The story (`story.html`, "How it works, from the very beginning": a short chat with EA-bot for someone new to AI, in the kit's chat style), How it works, Core logic, Skills, Harness flow, and What works today. That last page says plainly what works and what is only designed. Every other page, such as "Agents as vendors", sits under "More" in the menu.

Read it at https://codeami.github.io/firstmate-showcase/

The pages are plain HTML, `style.css` and `nav.js`. There is no build step for them. Open `story.html` from disk to read it locally. The home page chat fetches `tour/tour.json`, so serve the folder to read it: `python3 -m http.server`, then open `/`.

`kit/` is the shared Harbor Signal look for every front end: `tokens.css` (the only file with colours), `kit.css` (the shared parts), `bosun.svg` (the mascot) and `index.html`, a style guide showing every part in light and dark. Other apps link the two CSS files from https://codeami.github.io/firstmate-showcase/kit/. Of the showcase pages, the home page chat, Field Notes, the arena, Safety by design and About use the kit.

The two interactive maps, `maps/skills.html` and `maps/flow.html`, are built files. Their source is `maps/src/*/map.json` and the shell in `maps/_shared/` comes from [super-board](https://github.com/EricTechPro/super-board) by EricTechPro (MIT; see `maps/_shared/NOTICE`). To rebuild: `python3 -I maps/_shared/build.py maps/src/skills/map.json maps/skills.html` (and the same for `flow`).

The guided tour, `tour/index.html`, draws everything from `tour/tour.json`, the one script for the tour. It fetches that file, so serve the folder to read it locally: `python3 -m http.server`, then open `/tour/`.

The second brain map, `brain/index.html`, reads `brain/notes.js`. Both it and `brain/notes/*.md` are built from the owner's private wiki, but only for the slugs in `brain/allowlist.txt`, plus the notes written for this site in `brain/site-notes/` (the three talk modes). A privacy pass drops any line with a never-send term, a user name, a local path or an email. To rebuild: `python3 -I brain/build.py --src <wiki nodes folder> --never-send <terms file>`.

The supervisor and most crew mechanics are upstream [Firstmate](https://github.com/kunchenguid/firstmate) by Kun Chen and contributors. See `LICENSE` for this repo's licence.
