# Sphinx documentation. `make html` creates .venv and installs
# requirements.txt when needed, then builds.
# `make serve` builds the HTML and serves it at http://0.0.0.0:8000/.

PYTHON        ?= python3
VENV          ?= .venv
SPHINXOPTS    ?=
SPHINXBUILD   ?= $(VENV)/bin/sphinx-build
SOURCEDIR     = source
BUILDDIR      = build
PORT          ?= 8000
BIND          ?= 0.0.0.0

.PHONY: help html clean venv serve

help: $(SPHINXBUILD)
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

html: $(SPHINXBUILD)
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

venv: $(SPHINXBUILD)

serve: html
	@echo "Serving docs at http://$(BIND):$(PORT)/ (Ctrl-C to stop)"
	@$(PYTHON) -m http.server "$(PORT)" --bind "$(BIND)" --directory "$(BUILDDIR)/html"

clean:
	rm -rf "$(BUILDDIR)"

%: $(SPHINXBUILD)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

# Keep the catch-all Sphinx target from rebuilding these files.
Makefile: ;
requirements.txt: ;

$(VENV)/bin/sphinx-build: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
	touch $@
