# MDComputers Product Scraper

A Python scraper for MDComputers search results.

## Setup

```bash
python -m pip install -r requirements.txt
```

From PowerShell, first change into this folder. For the downloaded assignment
layout, run:

```powershell
cd C:\Users\arpit\Downloads\internshala_assignment\internshala_assignment\mdcomputers-scraper
python -m pip install -r .\requirements.txt
```

## Run

```bash
python scraper.py "external harddrive"
```

Save results to a custom CSV:

```bash
python scraper.py "external harddrive" --output products.csv
```

The CSV contains product name, price, availability, and product URL.

The parser is exposed as `parse_products(html)` so saved HTML can be
reprocessed when the live site temporarily blocks automated requests. The command
also detects Cloudflare access pages and exits with an actionable error.

> Website markup can change over time. Use the scraper responsibly and respect the site's terms and robots/access policies.
