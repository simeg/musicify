.PHONY: build ci coverage clean deploy deps fmt lint serve test test-ci verify-deps

BINS = $(shell npm bin)

REACT_SCRIPTS = $(BINS)/react-scripts
PRETTIER = $(BINS)/prettier
YARN = $(shell which yarn)
REFMT = $(shell which refmt)

build:
	$(REACT_SCRIPTS) build

ci: deps verify-deps lint test-ci build
	@echo "Web App CI: OK 👌"

coverage:
	@echo "Not implemented yet"

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

test:
	@$(REACT_SCRIPTS) test

test-ci:
	@echo "Not implemented yet"
	#@$(REACT_SCRIPTS) test --ci

verify-deps:
	@$(YARN) check --integrity
