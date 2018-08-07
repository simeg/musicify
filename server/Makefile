.PHONY: build ci coverage deploy deps lint login start serve test test-coverage type-check upload-coverage

# Travis cannot use 'pushd' or 'popd' without SHELL defined
SHELL := /bin/bash
IMAGE_NAME = musicify

SOURCE_FILES = $(shell find . -type f -name "*.py" -not -path "./test/*")

build:
	@docker build -t $(IMAGE_NAME):latest .

ci: deps lint test
	@echo "Server CI: OK 👌"

coverage: test-coverage upload-coverage

deploy: lint test build login
	@heroku container:push web --app=musicify
	@heroku container:release web --app=musicify

deps:
	@pip install -r ./requirements.txt

lint:
	@pycodestyle --format=pylint src test app.py
	@echo "Lint: OK 👌"

login:
	@heroku container:login
	@echo "Login: OK 👌"

start:
	@docker run -p 8000:8000 --restart=always $(IMAGE_NAME):latest

serve:
	@python3 app.py

test:
	@python -m pytest test
	@echo "Tests: OK 👌"

test-coverage:
	@python -m pytest --cov=src
	@echo "Test Coverage: OK 👌"

type-check:
	@mypy $(SOURCE_FILES)
	@echo "Type Check: OK 👌"

upload-coverage:
	@codecov
	@echo "Coverage Upload: OK 👌"
