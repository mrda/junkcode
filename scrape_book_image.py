#!/usr/bin/env python3
#
# scrape_book_image.py - example code on how to scrape an image from a website
#
# Copyright (C) 2026 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# Or try here: http://www.fsf.org/copyleft/gpl.html
#

from __future__ import annotations

import html
import re
import sys
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
OUTPUT_DIR = Path.home() / "tmp"
ASIN_RE = re.compile(r"/(?:dp|gp/product|gp/aw/d)/([A-Z0-9]{10})", re.I)
LANDING_IMAGE_HIRES_RE = re.compile(
    r'<img\b(?=[^>]*\bid=["\']landingImage["\'])[^>]*\bdata-old-hires=["\']([^"\']+)["\']',
    re.I,
)
LANDING_IMAGE_SRC_RE = re.compile(
    r'<img\b(?=[^>]*\bid=["\']landingImage["\'])[^>]*\bsrc=["\']([^"\']+)["\']',
    re.I,
)
OG_IMAGE_RE = re.compile(
    r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
    re.I,
)
MAIN_HIRES_RE = re.compile(
    r'"variant":"MAIN"[^}]*"hiRes":"([^"]+)"',
    re.I,
)


def fetch_page(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        },
    )
    with urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def extract_asin(url: str) -> str:
    match = ASIN_RE.search(url)
    if match:
        return match.group(1).upper()
    return "unknown"


def extract_image_url(page_html: str) -> str:
    for pattern in (
        LANDING_IMAGE_HIRES_RE,
        OG_IMAGE_RE,
        MAIN_HIRES_RE,
        LANDING_IMAGE_SRC_RE,
    ):
        match = pattern.search(page_html)
        if match:
            return html.unescape(match.group(1))
    raise ValueError("Could not find a product image on the page")


def extension_for_url(image_url: str) -> str:
    path = urlparse(image_url).path
    suffix = Path(path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        return suffix
    return ".jpg"


def download_image(image_url: str) -> bytes:
    request = Request(image_url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return response.read()


def save_image(image_bytes: bytes, asin: str, extension: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"book-{asin}-{uuid.uuid4().hex}{extension}"
    output_path = OUTPUT_DIR / filename
    output_path.write_bytes(image_bytes)
    return output_path


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <product-url>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1].strip()

    try:
        page_html = fetch_page(url)
        image_url = extract_image_url(page_html)
        image_bytes = download_image(image_url)
        output_path = save_image(
            image_bytes,
            extract_asin(url),
            extension_for_url(image_url),
        )
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print(output_path)


if __name__ == "__main__":
    main()
