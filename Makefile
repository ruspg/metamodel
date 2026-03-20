.PHONY: validate lint test determinism bundle all

PYTHON      ?= python3
METAMODEL   := model/metamodel.yaml
RELCATALOG  := model/relation_catalog.yaml

all: validate lint test  ## Run all checks

validate:  ## Run validation harness
	$(PYTHON) -m tools.wave1.harness $(METAMODEL) --relation-catalog-path $(RELCATALOG)

lint:  ## Run semantic linter
	$(PYTHON) -m tools.wave1.lint $(METAMODEL)

test:  ## Run tests
	$(PYTHON) -m pytest tests/ -v --tb=short

determinism:  ## Verify bundle reproducibility
	$(PYTHON) -m tools.wave1.bundle_determinism $(METAMODEL) --relation-catalog-path $(RELCATALOG)

bundle:  ## Generate atlas bundle
	@$(PYTHON) -c "\
from pathlib import Path; \
from tools.wave1.loader import load_ontology; \
from tools.wave1.projection_builder import build_projection_model; \
from tools.wave1.atlas_bundle_generator import generate_atlas_bundle; \
o = load_ontology('$(METAMODEL)', relation_catalog_path='$(RELCATALOG)'); \
p = build_projection_model(o, profile='atlas_mvp'); \
r = generate_atlas_bundle(p, Path('generated')); \
print(r.bundle_root)"

help:  ## Show this help
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-15s %s\n", $$1, $$2}'
