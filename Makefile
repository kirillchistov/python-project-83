.PHONY: install dev start build build-css watch-css render-start lint

PORT ?= 8000
export PATH := $(CURDIR)/.venv/bin:$(PATH)

install:
	uv sync

dev:
	uv run flask --debug --app page_analyzer:app run

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh

build-css:
	npm ci
	mkdir -p page_analyzer/static
	npx @tailwindcss/cli -i ./assets/app.css -o ./page_analyzer/static/style.css --minify

watch-css:
	npx @tailwindcss/cli -i ./assets/app.css -o ./page_analyzer/static/style.css --watch

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
	uv run flake8
