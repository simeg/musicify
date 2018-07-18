.PHONY: ci build deploy deps serve start lint login test test-cov type-check

# Travis cannot use 'pushd' or 'popd' without SHELL defined
SHELL := /bin/bash
IMAGE_NAME = musicify

SOURCE_FILES = $(shell find . -type f -name "*.py" -not -path "./test/*")

ci: deps lint test

build:
	docker build -t $(IMAGE_NAME):latest .

deploy: lint test build login
	heroku container:push web
	heroku container:release web

deps:
	pip install -r requirements.txt

lint:
	pycodestyle --format=pylint src test app.py

login:
	heroku container:login

start:
	docker run -p 8000:8000 --restart=always $(IMAGE_NAME):latest

serve:
	python3 app.py

test:
	@echo "Not implemented yet"
#	pushd test; pytest; popd

test-cov:
	@echo "Not implemented yet"
#	pushd test; py.test --cov-report=html:../coverage --cov-report=term --no-cov-on-fail --cov src; popd

type-check:
	mypy $(SOURCE_FILES)
