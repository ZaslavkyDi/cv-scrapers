.PHONY: ruff
ruff:
	poetry run ruff . --fix

.PHONY: black
black:
	poetry run black .