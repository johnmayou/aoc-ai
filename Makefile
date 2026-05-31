lint:
	@ruff check .
	@mypy .

fmt:
	@ruff format .
	@ruff check . --fix

flint: fmt lint

test:
	pytest -vvv src