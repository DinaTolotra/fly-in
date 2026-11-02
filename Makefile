.PHONY: install run debug clean lint lint-strict

MAP ?= maps/easy/01_linear_path.txt

install:
	uv sync

run:
	uv run python -m fly_in "$(MAP)"

debug:
	uv run python -m pdb -m fly_in "$(MAP)"

clean:
	uv run python -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__') if p.is_dir()]; shutil.rmtree('.mypy_cache', ignore_errors=True); shutil.rmtree('.pytest_cache', ignore_errors=True)"

lint:
	uv run flake8 .
	uv run mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 .
	uv run mypy . --strict