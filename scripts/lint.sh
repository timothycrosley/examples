#!/bin/bash
set -euxo pipefail

poetry run cruft check
poetry run mypy --ignore-missing-imports examples/
poetry run isort --check --diff examples/ tests/
poetry run black --check examples/ tests/
poetry run flake8 examples/ tests/
poetry run safety check -i 39462
poetry run bandit -r examples
