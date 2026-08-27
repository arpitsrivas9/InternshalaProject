#!/usr/bin/env python3
"""
Scrape product details from an MDComputers search results page.

Usage:
    python scraper.py "external harddrive"
    python scraper.py "ssd" --output products.csv
"""

import argparse
import csv
import re
import sys
from typing import Dict, List, Tuple
from urllib.parse import quote, urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://mdcomputers.in/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    )
}


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def parse_products(html: str) -> List[Dict[str, str]]:
    """Extract product details from an MDComputers results document."""
    soup = BeautifulSoup(html, "html.parser")
    products: List[Dict[str, str]] = []
    seen_urls = set()

    # OpenCart-style product result cards. Keep selectors flexible because
    # storefront themes can change without changing the product URLs.
    cards = soup.select(
        ".product-thumb, .product-layout, .product-grid-item, "
        ".product-list-item, .product-item"
    )

    for card in cards:
        link = card.select_one(
            "h4 a, h3 a, .name a, .product-name a, "
            "a[href*='product/product']"
        )
        if not link:
            continue

        product_url = urljoin(BASE_URL, link.get("href", ""))
        name = clean_text(link.get_text(" ", strip=True))
        if not name or product_url in seen_urls:
            continue

        price = card.select_one(".price, .product-price")
        availability = card.select_one(
            ".stock, .availability, .out-of-stock, .in-stock"
        )
        products.append(
            {
                "product_name": name,
                "price": clean_text(price.get_text(" ", strip=True)) if price else "",
                "availability": (
                    clean_text(availability.get_text(" ", strip=True))
                    if availability
                    else ""
                ),
                "product_url": product_url,
            }
        )
        seen_urls.add(product_url)

    # Fallback for layouts that do not wrap links in a product card.
    if not products:
        for link in soup.select("a[href*='product/product']"):
            name = clean_text(link.get_text(" ", strip=True))
            href = link.get("href", "")
            product_url = urljoin(BASE_URL, href)
            if name and len(name) >= 3 and product_url not in seen_urls:
                products.append(
                    {
                        "product_name": name,
                        "price": "",
                        "availability": "",
                        "product_url": product_url,
                    }
                )
                seen_urls.add(product_url)

    return products


def scrape_products(search_term: str) -> Tuple[List[Dict[str, str]], str]:
    search_term = search_term.strip()
    if not search_term:
        raise ValueError("Search term cannot be empty.")

    url = f"{BASE_URL}?route=product/search&search={quote(search_term)}"

    response = requests.get(url, headers=HEADERS, timeout=20)
    response.raise_for_status()
    if "cf-error-details" in response.text or "Attention Required" in response.text:
        raise RuntimeError(
            "MDComputers returned a Cloudflare access page. "
            "Try again from a permitted network or use a saved HTML page."
        )
    return parse_products(response.text), url


def save_csv(products, filename):
    fields = ["product_name", "price", "availability", "product_url"]
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(products)


def main():
    parser = argparse.ArgumentParser(description="Scrape MDComputers products.")
    parser.add_argument("search_term", help="Product search term")
    parser.add_argument(
        "--output",
        default="products.csv",
        help="CSV output filename (default: products.csv)",
    )
    args = parser.parse_args()

    try:
        products, url = scrape_products(args.search_term)
    except (requests.RequestException, RuntimeError, ValueError) as exc:
        print(f"Request failed: {exc}", file=sys.stderr)
        sys.exit(1)

    if not products:
        print(
            "No products were found. The website markup may have changed "
            "or the site may require additional access."
        )
        return

    save_csv(products, args.output)
    print(f"Search URL: {url}")
    print(f"Products found: {len(products)}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
