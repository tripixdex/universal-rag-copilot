.PHONY: format lint test tree

format:
	python -m ruff format src tests

lint:
	python -m ruff check src tests

test:
	python -m pytest -q

tree:
	@find . -maxdepth 3 -type d | sort
