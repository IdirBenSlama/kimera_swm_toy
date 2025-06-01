# Kimera SWM Makefile
# Replaces the numerous run_* scripts with a single entry point

.PHONY: help install lint test test-unit test-integration test-functional format clean

help:
	@echo "Kimera SWM Development Commands:"
	@echo "  install     - Install dependencies"
	@echo "  lint        - Run linting (ruff)"
	@echo "  test        - Run all tests"
	@echo "  test-unit   - Run unit tests only"
	@echo "  test-integration - Run integration tests only"
	@echo "  test-functional  - Run functional tests only"
	@echo "  format      - Format code (black)"
	@echo "  clean       - Clean cache and temp files"

install:
	poetry install --with dev

lint:
	ruff check src tests scripts
	ruff format --check src tests scripts

test:
	pytest -v

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-functional:
	pytest tests/functional/ -v

format:
	ruff format src tests scripts
	black src tests scripts

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf _nocache_temp
	rm -f *.db