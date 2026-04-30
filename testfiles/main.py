"""
Collect data from all 6 sources and save to CSV.
"""

from api_fetchers import fetch_open_library, fetch_youtube, fetch_github 
from scrapers import scrape_mit_ocw, scrape_freecodecamp
from csv_handler import save_courses 

def collect_all() -> list[dict]:
    all_courses = []

    print("\n── APIs ──────────────────────────────────────────────")
    all_courses += fetch_open_library(max_results=10)
    all_courses += fetch_github(max_results=10)
    all_courses += fetch_youtube(max_results=10)    # skips if key not set
 
    # ── 3 Scraping sources ─────────────────────────────────────
    print("\n── Scrapers ───────────────────────────────────────────")
    all_courses += scrape_mit_ocw(max_courses=15)
    all_courses += scrape_freecodecamp()
 
    # ── Save ───────────────────────────────────────────────────
    print("\n── Saving ─────────────────────────────────────────────")
    save_courses(all_courses)
 
    print(f"\nPhase 1 complete. Total collected this run: {len(all_courses)}")
    return all_courses
 
 
if __name__ == "__main__":
    collect_all()
