#!/bin/bash
set -euxo pipefail

poetry run cruft check
poetry run mypy --ignore-missing-imports examples/
poetry run isort --check --diff examples/ tests/
poetry run black --check examples/ tests/
poetry run flake8 examples/ tests/
poetry run safety check
poetry run bandit -r examples
