PYTHON ?= python3
PIP ?= $(PYTHON) -m pip

.PHONY: help install check test baseline-qualify clean clean-deep build source-zip release-verify packaging-smoke

help:
	@echo "Available targets:"
	@echo "  make install         - install the repo in editable mode with api/test extras"
	@echo "  make check           - run the full repo gate"
	@echo "  make test            - install extras and run the test suite"
	@echo "  make baseline-qualify - run the canonical baseline qualification gate"
	@echo "  make clean           - remove transient residue"
	@echo "  make clean-deep      - remove transient residue and generated runtime files"
	@echo "  make build           - build wheel and sdist"
	@echo "  make source-zip      - create a clean source zip"
	@echo "  make release-verify  - run release verification"
	@echo "  make packaging-smoke - run packaging smoke tests in isolation"

install:
	bash scripts/install_editable.sh

check:
	bash scripts/check_everything.sh

test:
	bash scripts/test_suite.sh

baseline-qualify:
	bash scripts/baseline_qualification.sh

clean:
	bash scripts/clean_repo.sh

clean-deep:
	bash scripts/clean_repo.sh --deep

build:
	$(PIP) install build
	$(PYTHON) -m build

source-zip:
	$(PIP) install -e .
	$(PYTHON) scripts/make_source_zip.py

release-verify:
	$(PIP) install -e ".[api,test]"
	$(PYTHON) -m hyperflow.release_verify --pretty

packaging-smoke:
	bash scripts/packaging_smoke.sh
