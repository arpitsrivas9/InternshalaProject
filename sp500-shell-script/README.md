# S&P 500 Shell Script

Downloads the supplied S&P 500 constituents CSV, extracts company name, location,
and founding year, then sorts the records by founding year.

## Requirements

- Bash
- curl
- Python 3 (used only for robust CSV parsing; the script detects `python3` or `python`)

## Run

```bash
chmod +x script.sh
./script.sh
```

Or choose an output filename:

```bash
./script.sh companies_sorted.csv
```

Source CSV:

https://raw.githubusercontent.com/datasets/s-and-p-500-companies/refs/heads/main/data/constituents.csv

The source currently labels the required fields `Security`, `Headquarters Location`,
and `Founded`. The script maps these to the output columns `Company`, `Location`,
and `Founded` (and also accepts the older `Name`/`Location` headers).
