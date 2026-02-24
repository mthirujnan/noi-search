"""
Scraper for Nectar of Instruction (NOI)
Fetches all pages from vedabase.io and saves content to data.json
Run this script once to generate the data file used by the search app.

Usage: python3 scraper.py
"""

import urllib.request
import urllib.error
import ssl
import json
import re
import time

# Fix for Mac SSL certificate issue
SSL_CONTEXT = ssl.create_default_context()
SSL_CONTEXT.check_hostname = False
SSL_CONTEXT.verify_mode = ssl.CERT_NONE

BASE_URL = "https://vedabase.io/en/library/noi/"

PAGES = [
    {"id": "preface", "title": "Preface",   "url": BASE_URL + "preface/"},
    {"id": "1",       "title": "Text 1",    "url": BASE_URL + "1/"},
    {"id": "2",       "title": "Text 2",    "url": BASE_URL + "2/"},
    {"id": "3",       "title": "Text 3",    "url": BASE_URL + "3/"},
    {"id": "4",       "title": "Text 4",    "url": BASE_URL + "4/"},
    {"id": "5",       "title": "Text 5",    "url": BASE_URL + "5/"},
    {"id": "6",       "title": "Text 6",    "url": BASE_URL + "6/"},
    {"id": "7",       "title": "Text 7",    "url": BASE_URL + "7/"},
    {"id": "8",       "title": "Text 8",    "url": BASE_URL + "8/"},
    {"id": "9",       "title": "Text 9",    "url": BASE_URL + "9/"},
    {"id": "10",      "title": "Text 10",   "url": BASE_URL + "10/"},
    {"id": "11",      "title": "Text 11",   "url": BASE_URL + "11/"},
]


def fetch_page(url):
    """Fetch raw HTML from a URL."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; NOI-Search/1.0)"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15, context=SSL_CONTEXT) as response:
        return response.read().decode("utf-8")


def strip_tags(html):
    """Remove HTML tags and decode common entities."""
    text = re.sub(r"<[^>]+>", " ", html)
    text = text.replace("&nbsp;", " ")
    text = text.replace("&amp;", "&")
    text = text.replace("&lt;", "<")
    text = text.replace("&gt;", ">")
    text = text.replace("&quot;", '"')
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_content(html, page_id):
    """Pull meaningful text out of the page HTML."""

    # Try to grab the main article content block
    main_match = re.search(
        r'<article[^>]*>(.*?)</article>', html, re.DOTALL | re.IGNORECASE
    )
    if not main_match:
        # Fallback: grab the body
        main_match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL | re.IGNORECASE)

    content_html = main_match.group(1) if main_match else html

    # Remove nav, footer, script, style blocks
    for tag in ["nav", "footer", "script", "style", "header"]:
        content_html = re.sub(
            rf"<{tag}[^>]*>.*?</{tag}>", "", content_html, flags=re.DOTALL | re.IGNORECASE
        )

    text = strip_tags(content_html)

    # For verse pages, try to isolate translation sentence
    translation = ""
    trans_match = re.search(r'TRANSLATION\s*(.*?)(?:PURPORT|$)', text, re.DOTALL | re.IGNORECASE)
    if trans_match:
        translation = trans_match.group(1).strip()[:300]

    return {
        "full_text": text,
        "translation": translation,
    }


def scrape():
    results = []
    total = len(PAGES)

    print(f"Scraping {total} pages from vedabase.io...\n")

    for i, page in enumerate(PAGES, 1):
        print(f"[{i}/{total}] Fetching {page['title']}...")
        try:
            html = fetch_page(page["url"])
            content = extract_content(html, page["id"])
            results.append({
                "id": page["id"],
                "title": page["title"],
                "url": page["url"],
                "text": content["full_text"],
                "translation": content["translation"],
            })
            print(f"         OK — {len(content['full_text'])} characters")
        except Exception as e:
            print(f"         ERROR: {e}")
            results.append({
                "id": page["id"],
                "title": page["title"],
                "url": page["url"],
                "text": "",
                "translation": "",
            })

        # Be polite — don't hammer the server
        if i < total:
            time.sleep(1)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Also write data.js so index.html works when opened as a local file
    with open("data.js", "w", encoding="utf-8") as f:
        f.write("const BOOK_DATA = ")
        json.dump(results, f, ensure_ascii=False)
        f.write(";")

    print(f"\nDone! Saved {len(results)} pages to data.json and data.js")


if __name__ == "__main__":
    scrape()
