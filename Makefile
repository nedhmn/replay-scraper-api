lint:
	uv run ruff check .
	uv run ruff format .

type-check:
	uv run mypy app

check:
	make lint
	make type-check

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".ruff_cache" -exec rm -rf {} +

generate-api-key:
	uv run python3 -m scripts.generate_api_key

dev:
	uv run fastapi dev app/main.py

help:
	@echo "Available commands:"
	@echo "  lint         : Run code formatters and linters"
	@echo "  type-check   : Run type checkers"
	@echo "  check        : Run linting and type checking"
	@echo "  clean        : Remove Python cache files and build artifacts"
	@echo "  generate-api-key: Generate a new API key"
	@echo "  dev          : Run fastapi dev server"