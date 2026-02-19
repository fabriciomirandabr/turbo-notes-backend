.PHONY: lint lint-fix test test-cov
test:
	cd backend && pytest -v

test-cov:
	cd backend && pytest --cov=notes --cov=config --cov-report=term-missing --cov-fail-under=80

lint:
	ruff check notes config manage.py && ruff format --check notes config manage.py

lint-fix:
	ruff check notes config manage.py --fix && ruff format notes config manage.py
