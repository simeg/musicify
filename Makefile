.PHONY: ci build codecov deploy deps lint login start serve test test-cov

# Travis cannot use 'pushd' or 'popd' without SHELL defined
SHELL := /bin/bash
IMAGE_NAME = musicify

SOURCE_FILES = $(shell find . -type f -name "*.py" -not -path "./test/*")

ci: deps lint test test-cov codecov

build:
	docker build -t $(IMAGE_NAME):latest .

codecov:
	codecov

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
	python -m pytest

test-cov:
	python -m pytest --cov=./src
