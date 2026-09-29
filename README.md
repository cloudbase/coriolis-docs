# Coriolis documentation

Documentation for [Coriolis](https://cloudbase.it/coriolis), the migration and disaster-recovery platform from Cloudbase Solutions.

The published site is [https://cloudbase.github.io/coriolis-docs/](https://cloudbase.github.io/coriolis-docs/).

## Build locally

```bash
make html
```

`make html` creates `.venv`, installs `requirements.txt`, and writes the HTML to `build/html`.

To build and open the site in a browser:

```bash
make serve
```

That serves `build/html` on all interfaces at port 8000. Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Override the address with `make serve PORT=8080 BIND=127.0.0.1`. Stop the server with Ctrl-C.

Pages are Markdown under `source/`, built with Sphinx, MyST, and the Shibuya theme.

## Publishing

Pull requests build the HTML to validate the change. Pushes to `main` build it again and deploy it to GitHub Pages.
