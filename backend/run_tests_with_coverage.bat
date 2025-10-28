@echo off
echo Running tests with coverage...
pytest --cov=app --cov-report=html --cov-report=term-missing -v tests/
echo Coverage report generated in htmlcov/ directory
