# Create isolated Python environment with necessayr dependencies
install:
	@echo "Install Python Poetry to build the project"
	curl -sSL https://install.python-poetry.org | python3 -
	poetry env use $(shell which python3.10) && \

	@echo "Creating virtual environment"
	poetry install

# Server commands
run:
	@echo "Running API without cache"
	poetry run uvicorn src.main:app --reload

# Code linting and formatting
lint:
	poetry run ruff check --fix

format:
	poetry run ruff format .

lint-and-format: lint format