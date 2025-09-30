#!/usr/bin/env bash
set -euo pipefail
python -m pip install --upgrade pip cyclonedx-bom pip-licenses >/dev/null
cyclonedx-py --output sbom.json --spec-version 1.4 --format json || cyclonedx-bom -e -o sbom.json
pip-licenses --format=json --with-authors --with-urls > licenses.json
echo "SBOM: sbom.json  | Licenses: licenses.json"
