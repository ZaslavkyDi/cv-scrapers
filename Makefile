.PHONY: ruff
ruff:
	poetry run ruff . --fix

.PHONY: black
black:
	poetry run black .

.PHONY: pytest-cov
pytest-cov:
	poetry run pytest --cov=cv_scrapers tests/