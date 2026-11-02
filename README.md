# firstmate-showcase

This site has moved to https://codeami.github.io/ (the demo is at https://codeami.github.io/ai-life-os/). The source now lives in [codeami/codeami.github.io](https://github.com/codeami/codeami.github.io).

This repo keeps only redirect stubs so old links to https://codeami.github.io/firstmate-showcase/ still work:

- Every former page is a small page that sends the browser to the same path under `https://codeami.github.io/ai-life-os/` (meta refresh, plus `location.replace` when JavaScript is on).
- Pages retired in the new site go to the closest page: `s02` to `s10` to `story.html`; `harness`, `skills`, `tasks`, `testing` to `core.html`; `cast`, `vendors` to `about.html`; `overview` to `index.html#pages`.
- `404.html` sends any other path to the same path under `/ai-life-os/`.

The full history of the old site is in git. See `LICENSE`.
