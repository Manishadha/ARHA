.PHONY: setup test lint type fmt ci sbom
setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r backend/requirements.txt && pre-commit install
test:
	. .venv/bin/activate && pytest
lint:
	. .venv/bin/activate && ruff check backend tests && bandit -r backend -ll
type:
	. .venv/bin/activate && mypy backend
fmt:
	. .venv/bin/activate && black backend tests && ruff check backend tests --fix
sbom:
	./tools/sbom.sh
