.PHONY: install run debug clean lint lint-strict

MAP ?= maps/easy/01_linear_path.txt

install:
	@echo "Installing dependencies..."
	@uv sync
	@echo "Dependencies installed!"

run:
	@echo "Starting main script..."
	uv run python -m src "$(MAP)"

debug:
	@echo "Launching main script with debuger..."
	uv run python -m pdb src "$(MAP)"

clean:
	@echo "Deleting temporary file/folder..."
	uv run python -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__') if p.is_dir()]; shutil.rmtree('.mypy_cache', ignore_errors=True); shutil.rmtree('.pytest_cache', ignore_errors=True)"

lint:
	@echo "Checking norme and type-hint..."
	uv run flake8 src
	uv run mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@echo "Checking norme and type-hint..."
	uv run flake8 src
	uv run mypy src --strict