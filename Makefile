.PHONY: test report lint format

test:
	python -m pytest -q

report:
	python scripts/make_research_report.py

lint:
	python -m ruff check src scripts tests

format:
	python -m black src scripts tests
