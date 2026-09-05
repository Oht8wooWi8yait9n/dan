# Divers Alert Network (dan.org) Sitemap & URL Index

This repository provides a consolidated, clean XML sitemap and complete URL index for **Divers Alert Network** ([dan.org](https://dan.org)).

It aggregates all core content areas while stripping out image metadata tags, category/tag duplicate archive pages, author listings, and utility cart/account URLs:
- **Alert Diver Magazine** (1,654+ in-depth articles on diving physiology, equipment safety, and underwater exploration)
- **Diving Diseases & Conditions** (Decompression sickness, barotrauma, ear equalization, marine envenomations, fitness to dive)
- **Health Resources & Medical Guidance** (Health FAQs, safety checklists, oxygen provider info)
- **Diving Incident Reports** (Case studies, safety analysis, lessons learned)
- **Research Studies** (Chamber data, flying after diving, bubble studies)
- **Divers Blog & News** (Latest community posts, safety alerts)
- **Core Educational & Safety Pages** (Courses, training, safety guidelines)

## Files

- `dan_sitemap.xml`: Full standard XML sitemap containing all 2,521 clean content URLs.
- `dan_urls.txt`: Plain text list of all 2,521 URLs (one per line).
- `generate_dan_sitemap.py`: Standalone Python script used to aggregate and regenerate the sitemap.
- `.github/workflows/update-sitemap.yml`: GitHub Actions workflow that automatically updates the sitemap weekly.

## Usage with Onyx Web Connector

To index Divers Alert Network in Onyx:

1. Copy the **Raw** URL of `dan_sitemap.xml`:
   ```
   https://raw.githubusercontent.com/Oht8wooWi8yait9n/dan/main/dan_sitemap.xml
   ```
2. In Onyx Admin UI (**Connectors** -> **Web**):
   - **Connector Name**: `DAN` (or `Divers-Alert-Network`)
   - **Base URL**: `https://raw.githubusercontent.com/Oht8wooWi8yait9n/dan/main/dan_sitemap.xml`
   - **Scrape Method**: `sitemap`
3. Click **Create Connector**.

## Periodic Updates

- **Automatic (GitHub Actions)**: A scheduled workflow runs every Sunday at midnight UTC (`.github/workflows/update-sitemap.yml`) to check for new articles or page updates. You can also trigger it manually from the Actions tab on GitHub.
- **Manual Regeneration**:
  ```bash
  python3 generate_dan_sitemap.py
  ```
