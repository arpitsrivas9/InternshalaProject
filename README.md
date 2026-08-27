# Internshala Full Stack Development Assignment

This repository contains the two technical assignments requested in the
Internshala application.

## Projects

### 1. MDComputers Product Scraper
Python + Requests + BeautifulSoup scraper for product search results, with CSV
export and clear handling for access-blocked responses.

Location: `mdcomputers-scraper/`

### 2. S&P 500 Shell Script
Bash script that downloads the supplied CSV, maps company name/location/founding
year fields, and sorts the records by founding year.

Location: `sp500-shell-script/`

## Important

Before submitting, run and test both projects locally. Website markup and remote
CSV data can change, so verify the output at submission time.

## Windows quick start

If your terminal is currently at `C:\Users\arpit\Downloads\internshala_assignment`,
the assignment files are inside the nested `internshala_assignment` folder:

```powershell
cd .\internshala_assignment\mdcomputers-scraper
python -m pip install -r .\requirements.txt
python .\scraper.py "external harddrive" --output .\products.csv
```

Do not run `python scraper.py` from the parent folder; that folder does not
contain `scraper.py`.
