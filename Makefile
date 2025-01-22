.PHONY: lint format check ci

lint:
	uv run ruff check . --fix

format:
	uv run ruff format .

check:
	uv run mypy .

test:
	uv run pytest .

ci: format lint check test
