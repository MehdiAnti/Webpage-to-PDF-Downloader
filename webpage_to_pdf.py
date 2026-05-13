import asyncio
import os
import re
import argparse
from pyppeteer import launch
from urllib.parse import urlparse

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name)

async def save_pdf(url: str, output_file: str):
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(url, waitUntil='networkidle0')
    await page.pdf({
        'path': output_file,
        'format': 'A4',
        'printBackground': True
    })
    await browser.close()

def main():
    parser = argparse.ArgumentParser(description="Download a webpage as PDF.")
    parser.add_argument("--url", required=True, help="URL of the page")
    parser.add_argument("--title", help="Optional title for output file")
    args = parser.parse_args()

    if args.title:
        base_name = sanitize_filename(args.title)
    else:
        parsed = urlparse(args.url)
        path = parsed.path.strip('/').replace('/', '_')
        base_name = sanitize_filename(path) or sanitize_filename(parsed.netloc) or "webpage"

    pdf_filename = f"{base_name}.pdf"
    
    # Create download directory
    download_dir = "download"
    os.makedirs(download_dir, exist_ok=True)
    pdf_path = os.path.join(download_dir, pdf_filename)

    print(f"Downloading {args.url} → {pdf_filename}")
    asyncio.run(save_pdf(args.url, pdf_path))
    print(f"✅ Created {pdf_path}")

if __name__ == "__main__":
    main()
