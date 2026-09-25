# Sphinx documentation. `make html` creates .venv and installs
# requirements.txt when needed, then builds.

PYTHON        ?= python3
VENV          ?= .venv
SPHINXOPTS    ?=
SPHINXBUILD   ?= $(VENV)/bin/sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

.PHONY: help html clean venv

help: $(SPHINXBUILD)
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

html: $(SPHINXBUILD)
	@$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

venv: $(SPHINXBUILD)

clean:
	rm -rf "$(BUILDDIR)"

%: $(SPHINXBUILD)
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

# Keep the catch-all Sphinx target from rebuilding this file.
requirements.txt: ;

$(VENV)/bin/sphinx-build: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt
	touch $@
