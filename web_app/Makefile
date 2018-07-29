.PHONY: all build ci deploy fmt lint serve test-ci test verify-deps

BINS = $(shell npm bin)

REACT_SCRIPTS = $(BINS)/react-scripts
PRETTIER = $(BINS)/prettier
YARN = $(shell which yarn)
REFMT = $(shell which refmt)

build:
	$(REACT_SCRIPTS) build

ci: verify-deps lint test-ci build

clean:
	rm -rf ./node_modules

deploy: ci
	@echo "Not implemented yet"
	#git push heroku master

deps:
	@$(YARN) install

fmt:
	@$(REFMT) --in-place src/**/*.re

lint:
	@echo "Not implemented yet"

serve:
	@$(YARN) start

test-ci:
	@CI=true $(REACT_SCRIPTS) test

test:
	@$(REACT_SCRIPTS) test

verify-deps:
	@$(YARN) check --integrity
