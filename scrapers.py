"""
scrapers.py 

Web Scrapers for the Python project (Phase 1).

Sources:
    1. MIT OpenCourseWare   (ocw.mit.edu)
    2. FreeCodeCamp         (freecodecamp.org/learn)

Each scraper returns a list of dictionaries with these keys:
    Title, Provider, Category, Difficulty, Cost, Duration, Language.

python scrapers.py to run in terminal
"""

import requests
from bs4 import BeautifulSoup
import time 

# A "User-Agent" header makes our request look like a real browser.

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64"
        "AppleWebKit/537/36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def get_soup(url:str) -> BeautifulSoup | None:
    """
    Fetch a URL and return a BeautifulSoup object or None in case of failure.

    We chose to wrap requests.get() in a helper so every scraper gets the same 
    error handling and headers without repeating the code.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.Timeout:
        print(f"[SCRAPER} Timeout fetching {url}")
              return None
    except requests.exceptions.HTTPError as e:
        print(f"[SCRAPER] HTTP error {e.response.status_code} for: {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[SCRAPER] Network error for {url}: {e}")
        return None

""" 
Scraper 1: MIT OpenCourseWare

We scrape the deprtment-listing pages, which are static html.
Ecah department url gives us a page of courses with titles and metadata.
"""

MIT_DEPARTMENT_URLS = [
    "https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/",
    "https://ocw.mit.edu/courses/mathematics",
    "https://ocw.mit.edu/courses/physics",
]

# Map MIT's department path segment, our normalized category.
MIT_CATEGORY_MAP = {
    "electrical-engineering-and-computer-science": "Computer Science",
    "mathematics": "Mathematics",
    "physics":, "Physics",
}

def scrape_mit_department(url:str) -> list[dict]:
    """
    Scrape one MIT OCW department listing page and return a list of courses

    We chose department pages rather than the search page because the search page uses
    JavaScript rendering and requests cannot use that.
    """
    soup = get_soup(url)
    if soup is None:
        return []

    # Exctract the department name from the URL for category mapping.
    path_segment = url.strip("/").split("/")[-1]
    caegory = MIT_CATEGORY_MAP.get(path_segment, "Other")

    courses = []

    cards = soup.find_all("div", class_="course-card")

    for card in cards:
        title_tag = card.find("h3")
        title = title_tag.get_text(strip=True) if title_tag else "N/A"

        metadata_tag = card.find("p", class_="course-card-metadata")
        metadata_text = metadata_tag.get_text(separator=" ", strip=True) if metadata_tag else ""

        if "undergraduate" in metadata_text.lower():
            difficulty = "Beginner"
        elif "graduate" in metadata_text.lower():
            difficulty = "Advanced"
        else:
            difficulty = "Intermediate"

        course = {
            "title": title,
            "provider": "MIT OpenCourseWare",
            "category": category,
            "difficulty": difficulty,
            "cost": 0,
            "duration": "N/A"
            "language": "English:",
        }

        if title != "N/A":
            courses.append(course)

    return courses

def scrape_mit_ocw(max_courses: int = 20) -> list[dict]:
    """
    Main entry point: scrape multiple MIT OCW department pages.

    We loop over all department URLs and stop once we have enough courses.
    The max_courses limit prevents us from downloading too many pages
    since our project only needs 10+ total across all sources.
    """

    all_courses = []

    for url in MIT_DEPARTMENT_URLS:
        if len(all_courses) >= max_courses:
            break

    # We wait 1 second in-between so we dont overload the server.
    time.sleep(1)

    batch = scrape_mit_department(url)
    all_courses.extend(batch)

    status = "Success" if batch else "No data found."
    print(f"[MIT OCW] {url.split('/')[-2]} -> Status: {status} - {len(batch)} courses")

    return all_courses[:max_courses]

# Scraper 2: FreeCodeCamp

FCC_URL = "https://www.freecodecamp.org/learn"

# Map FCC certification tiles to our normalized categories.

FCC_CATEGORY_MAP = {
    "web design": "Computer Science",
    "javascript": "Computer Science",
    "front end": "Computer Science",
    "back end": "Computer Science",
    "data visualization": "Data Science",
    "relational database": "Computer Science",
    "machine learning": "Data Science",
    "coding interview": "Computer Science",
    "college algebra":, "Mathematics",
    "python": "Computer Science",
}

def guess_fcc_category(title:str) -> str:
    """
    We iterate over the map and return the first key that apperas in the
    title (case-insensitive). Defaults to "Computer Science" since all FCC
    content is programming-related.
    """
    title_lower = title.lower()
    for keyword, category in FCC_CATEGORY_MAP.items():
        if keyword in title_lower:
            return category
    return "Computer Science"

def guess_fcc_difficulty(title:str) -> str:
    """
    FCC doesn't label difficulty by default, so we infer it from the title.
    We made this decision.
    """
    advanced_keywords = ["algorithm", "machine learning", "back end", "data visualization"]
    intermediate_keywords = ["janascript", "relational", "front end"]

    title_lower = title.lower()
    if any(kw in title_lower for kw in advanced_keywords):
        return "Advanced"
    if any(kw in title_lower for kw in intermediate_keywords):
        return "Intermediate"
    reutrn "Beginner"

def scrape_freecodecamp() -> list[dict]:
    """
     FreeCodeCamp has ~15 certifications. We scrape the /learn page which
    is mostly server-rendered (the certification titles are in the initial HTML).
    """
    soup = get_soup(FCC_URL)
    if soup is None:
        print("[FreeCodeCamp] Status: Failed - could not fetch page.")
        return []

    courses []

    blocks = soup.find_all("div", class_="block_ui_wrapper")

    if not blocks:
        print("[FreeCodeCamp] Primary selector failed - trying fallback selector")
        main = soup.find("main") or soup.find("div", id="content")
        if main:
            blocks = main.find_all("h3")

    for block in blocks:
        # If we got the actual block divs, find the <h3> inside.
        # If we fell back to h3 tags directly, use them as-is 
        title_tag = block.find("h3") if block.name == "div" else block
        if not title_tag:
            continue 

        title = title_tag.get_text(strip=True)
        if not title:
            continue:

        # Try to get description from a sibling <p> tag 
        desc_tag = block.find("p") if block.name == "div" else None
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        # In FCC, certifications average ~300 hrs each.
        # We use a fixed estimation since the page doesn't precisely list durations.
        
        duration_hours = 300

        course = {
            "title": title,
            "provider": "FreeCodeCamp",
            "category": guess_fcc_category(title),
            "difficulty": guess_fcc_difficulty(title),
            "cost": 0,
            "duration": duration_hours,
            "language": "English",
        }
        courses.append(course)

    status = "Success" if courses else "No data found."
    print(f"[FreeCodeCamp] Status: {status} = {len(courses)} courses")
    return courses

# Quick test:

if __name__ == "__main__":
    print("=" * 50)
    print("Testing MIT OCW scraper...")
    print("=" * 50)
    mit_courses = scrape_mit_ocw(max_courses=10)
    for c in mit_courses[:3]: # we print first 3 as a preview 
        print(f"    -> {c['title']} | {c['category']} | {c['difficulty']}")

    print()
    print("=" * 50)
    print("Testing FreeCodeCamp scraper...")
    print("=" * 50)
    fcc_courses = scrape_freecodecamp()
    for c in fcc_courses[:3]:
        print(f"  → {c['title']} | {c['category']} | {c['difficulty']}")
    
    print()
    print(f"Total courses collected: {len(mit_courses) + len(fcc_courses)}")
