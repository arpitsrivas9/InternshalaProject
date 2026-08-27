#!/usr/bin/env bash
set -euo pipefail

CSV_URL="https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv"
OUTPUT_FILE="${1:-sorted_companies.csv}"
if command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
else
    echo "Python 3 is required but was not found in PATH." >&2
    exit 1
fi

TMP_FILE="$(mktemp)"
trap 'rm -f "$TMP_FILE"' EXIT

curl -L --fail --silent --show-error "$CSV_URL" -o "$TMP_FILE"

"$PYTHON_BIN" - "$TMP_FILE" "$OUTPUT_FILE" <<'PY'
import csv
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, newline="", encoding="utf-8-sig") as source:
    reader = csv.DictReader(source)

    headers = set(reader.fieldnames or [])
    company_column = "Name" if "Name" in headers else "Security"
    location_column = "Location" if "Location" in headers else "Headquarters Location"
    required = {company_column, location_column, "Founded"}
    missing = required - headers
    if missing:
        raise SystemExit(f"Missing required columns: {', '.join(sorted(missing))}")

    rows = []
    for row in reader:
        rows.append({
            "Company": row[company_column].strip(),
            "Location": row[location_column].strip(),
            "Founded": row["Founded"].strip(),
        })

def year_key(row):
    value = row["Founded"]
    try:
        return (0, int(value))
    except ValueError:
        return (1, value.lower())

rows.sort(key=year_key)

with open(output_file, "w", newline="", encoding="utf-8") as destination:
    writer = csv.DictWriter(
        destination,
        fieldnames=["Company", "Location", "Founded"]
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"Processed {len(rows)} companies.")
print(f"Sorted output written to: {output_file}")
PY
