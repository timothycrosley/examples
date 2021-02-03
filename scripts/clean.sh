#!/bin/bash
set -euxo pipefail

poetry run isort examples/ tests/
poetry run black examples tests/
