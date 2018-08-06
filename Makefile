.PHONY: build deploy deps lint login start serve test test-coverage upload-coverage

# Travis cannot use 'pushd' or 'popd' without SHELL defined
SHELL := /bin/bash
IMAGE_NAME = musicify

SOURCE_FILES = $(shell find ./server -type f -name "*.py" -not -path "./test/*")

build:
	@docker build -t $(IMAGE_NAME):latest .

deploy: lint test build login
	@heroku container:push web --app=musicify
	@heroku container:release web --app=musicify

deps:
	@pip install -r ./server/requirements.txt

lint:
	@pycodestyle --format=pylint server/src server/test server/app.py
	@echo "Lint: OK 👌"

login:
	@heroku container:login
	@echo "Login: OK 👌"

start:
	@docker run -p 8000:8000 --restart=always $(IMAGE_NAME):latest

serve:
	@python3 server/app.py

test:
	@pushd server; python -m pytest test && echo "Tests: OK 👌"; popd

test-coverage:
	@pushd server; python -m pytest --cov=./src && echo "Tests: OK 👌"; popd

type-check:
	@mypy $(SOURCE_FILES)
	@echo "Type Check: OK 👌"

upload-coverage:
	@pushd server; codecov && echo "Coverage Upload: OK 👌"; popd
