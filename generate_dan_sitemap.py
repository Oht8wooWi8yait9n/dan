#!/usr/bin/env python3
"""
Generate a consolidated, clean Sitemap (XML) and URL list (TXT) for Divers Alert Network (dan.org).
This aggregates all relevant content sitemaps (Alert Diver articles, Health Resources,
Diseases & Conditions, Incident Reports, Research Studies, Blog Posts, and Core Pages)
while filtering out image tags, tag/taxonomy archives, and duplicate listings.
"""

import os
import sys
import xml.etree.ElementTree as ET
import requests

BASE_SITEMAP_INDEX = "https://dan.org/sitemap_index.xml"

# High-value content sitemaps to include
CONTENT_SITEMAPS = [
    "https://dan.org/dan_alert_diver-sitemap.xml",
    "https://dan.org/dan_alert_diver-sitemap2.xml",
    "https://dan.org/dan_health_resources-sitemap.xml",
    "https://dan.org/dan_diseases_conds-sitemap.xml",
    "https://dan.org/dan_diving_incidents-sitemap.xml",
    "https://dan.org/dan_research_study-sitemap.xml",
    "https://dan.org/dan_divers_blog-sitemap.xml",
    "https://dan.org/page-sitemap.xml",
    "https://dan.org/post-sitemap.xml",
    "https://dan.org/tribe_events-sitemap.xml",
]

# Patterns in URLs that should be excluded (e.g. utility / auth pages)
EXCLUDE_URL_PATTERNS = [
    "/my-account",
    "/cart",
    "/checkout",
    "/login",
    "/password-reset",
    "/wp-login",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

XML_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def fetch_sitemap_urls(session: requests.Session, sitemap_url: str) -> list[str]:
    print(f"[*] Fetching: {sitemap_url.split('/')[-1]}...")
    try:
        r = session.get(sitemap_url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"    [!] Error: Status code {r.status_code}")
            return []
        root = ET.fromstring(r.content)
        urls = []
        for url_elem in root.findall(f"{XML_NS}url"):
            loc_elem = url_elem.find(f"{XML_NS}loc")
            if loc_elem is not None and loc_elem.text:
                url_str = loc_elem.text.strip()
                if not any(pattern in url_str for pattern in EXCLUDE_URL_PATTERNS):
                    urls.append(url_str)
        print(f"    Discovered {len(urls)} URLs.")
        return urls
    except Exception as e:
        print(f"    [!] Failed to parse {sitemap_url}: {e}")
        return []


def main():
    print("=" * 60)
    print(" Divers Alert Network (dan.org) Sitemap Generator")
    print("=" * 60)

    session = requests.Session()
    session.headers.update(HEADERS)

    all_urls = set()

    for sitemap_url in CONTENT_SITEMAPS:
        urls = fetch_sitemap_urls(session, sitemap_url)
        all_urls.update(urls)

    sorted_urls = sorted(list(all_urls))
    print("\n" + "=" * 60)
    print(f"[+] Total unique content URLs aggregated: {len(sorted_urls)}")
    print("=" * 60)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_sitemap = os.path.join(script_dir, "dan_sitemap.xml")
    out_txt = os.path.join(script_dir, "dan_urls.txt")

    with open(out_txt, "w") as f:
        for u in sorted_urls:
            f.write(u + "\n")

    with open(out_sitemap, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in sorted_urls:
            f.write(f"  <url><loc>{u}</loc></url>\n")
        f.write("</urlset>\n")

    print(f"[+] Saved sitemap XML: {out_sitemap}")
    print(f"[+] Saved URLs list:   {out_txt}")


if __name__ == "__main__":
    main()
