#!/usr/bin/env bash
set -euo pipefail
FILE="docs/daily_log.md"
DATE=$(date +%F)
{
  echo
  echo "Date: ${DATE}"
  echo "Progress:"
  echo "- [done] "
  echo "- [wip] "
  echo "- [next] "
  echo "Risks/Decisions:"
  echo "- "
  echo "Checks:"
  echo "- Tests green?  yes/no"
  echo "- Lint/format?  yes/no"
  echo "- CVE scan?     clean/issues"
} >> "$FILE"
echo "Appended daily entry to ${FILE}"
