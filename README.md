# Nectar of Instruction — Search App

Search across all texts, translations, and purports of the Nectar of Instruction (NOI) by Srila Prabhupada.

## How to Use

1. Run the scraper to fetch the book content:
   ```
   python3 scraper.py
   ```
2. Open `index.html` in your browser
3. Type any word or phrase and press Enter or click Search

## Features

- Searches all 12 sections (Preface + 11 Texts)
- Filter by individual text using the buttons
- Highlights matching words in results
- Links directly to the full text on vedabase.io

## Files

- `scraper.py` — fetches all pages and saves to `data.json`
- `data.json` — scraped book content (auto-generated)
- `index.html` — the search interface

## Source

Book: [Nectar of Instruction on vedabase.io](https://vedabase.io/en/library/noi/)
