# Coriolis documentation

Documentation for [Coriolis](https://cloudbase.it/coriolis), the migration and disaster-recovery platform from Cloudbase Solutions.

The published site is [https://cloudbase.github.io/coriolis-docs/](https://cloudbase.github.io/coriolis-docs/).

## Build locally

```bash
make html
```

`make html` creates `.venv`, installs `requirements.txt`, and writes the HTML to `build/html`. Open `build/html/index.html` in a browser.

Pages are Markdown under `source/`, built with Sphinx, MyST, and the Read the Docs theme.

## Publishing

Pushes to `main` build the HTML and deploy it to GitHub Pages.
