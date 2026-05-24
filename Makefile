.PHONY: install run-web daily weekly test lint compile

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install ".[dev]"

run-web:
	python3 -m uvicorn apps.web.main:app --host 0.0.0.0 --port 8000

daily:
	python3 -m services.jobs.cli daily-run

weekly:
	python3 -m services.jobs.cli weekly-run

test:
	pytest

lint:
	ruff check .

compile:
	python3 -m compileall apps packages services scripts
