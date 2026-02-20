.PHONY: install install-dev test lint format clean run

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=videograb --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

lint:
	flake8 videograb/ --max-line-length=110

format:
	black videograb/ tests/

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	rm -rf .coverage htmlcov/ dist/ build/ *.egg-info/

run:
	python -m videograb.cli --interactive
