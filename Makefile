install:
	python -m pip install -e '.[dev]'

run:
	uvicorn app.main:app --reload

test:
	pytest -q

lint:
	ruff check src tests

format:
	ruff format src tests

typecheck:
	mypy src

demo:
	python -m app.cli demo --output-dir ./demo-output

all: lint typecheck test
