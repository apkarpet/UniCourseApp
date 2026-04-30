"""
csv_handler.py

Handles saving scraped courses to CSV 
and normalizes raw filed values.

Design decisions:
    - Append Mode ("a"): so repeated runs build up the dataset over time.
    - Normalization happens BEFORE saving so the CSV is always clean.
    - Duplicate detection is by (title + provider) to avoid double-entries
      when the same scraper runs twice.
"""

import csv 
import os 
import pandas as pd 

CSV_FILE = "courses_1115507.csv"

FIEDNAMES = ["title", "provider", "category", "difficulty", "cost", "duration", "language"]

DIFFICULTY_MAP = {
    # Begginner synonyms
    "beginner": "Beginner",
    "easy": "Beginner",
    "intro": "Beginner",
    "introductory": "Beginner",
    "foundation": "Beginner",
    "basic": "Beginner",
    "level 1": "Beginner",

    # intermediate synonyms 
    "intermediate": "Intermediate",
    "medium": "Intermediate",
    "level 2": "Intermediate",

    # advanced synonyms
    "advanced": "Advanced",
    "expert": "Advanced",
    "hard": "Advanced",
    # cs 
    "computer science":   "Computer Science",
    "cs":                 "Computer Science",
    "programming":        "Computer Science",
    "coding":             "Computer Science",
    "software":           "Computer Science",
    "python":             "Computer Science",
    "javascript":         "Computer Science",
    "web":                "Computer Science",
    "web design":         "Computer Science",
    "web development":    "Computer Science",
    "algorithms":         "Computer Science",
    "data structures":    "Computer Science",
    # Data Science / ML
    "data science":       "Data Science",
    "machine learning":   "Data Science",
    "ai":                 "Data Science",
    "artificial intelligence": "Data Science",
    "data analysis":      "Data Science",
    "data visualization": "Data Science",
    # Mathematics
    "mathematics":        "Mathematics",
    "math":               "Mathematics",
    "maths":              "Mathematics",
    "algebra":            "Mathematics",
    "calculus":           "Mathematics",
    "statistics":         "Mathematics",
    # Physics / Engineering
    "physics":            "Physics",
    "engineering":        "Engineering",
    "electrical":         "Engineering",
    # Other
    "general":            "General",computer science":   "Computer Science",
    "cs":                 "Computer Science",
    "programming":        "Computer Science",
    "coding":             "Computer Science",
    "software":           "Computer Science",
    "python":             "Computer Science",
    "javascript":         "Computer Science",
    "web":                "Computer Science",
    "web design":         "Computer Science",
    "web development":    "Computer Science",
    "algorithms":         "Computer Science",
    "data structures":    "Computer Science",
    # Data Science / ML
    "data science":       "Data Science",
    "machine learning":   "Data Science",
    "ai":                 "Data Science",
    "artificial intelligence": "Data Science",
    "data analysis":      "Data Science",
    "data visualization": "Data Science",
    # Mathematics
    "mathematics":        "Mathematics",
    "math":               "Mathematics",
    "maths":              "Mathematics",
    "algebra":            "Mathematics",
    "calculus":           "Mathematics",
    "statistics":         "Mathematics",
    # Physics / Engineering
    "physics":            "Physics",
    "engineering":        "Engineering",
    "electrical":         "Engineering",
    # Other
    "general":            "General",
    "graduate": "Advanced",
    "level 3": "Advanced"
}

CATEGORY_MAP = {
    "computer science":   "Computer Science",
    "cs":                 "Computer Science",
    "programming":        "Computer Science",
    "coding":             "Computer Science",
    "software":           "Computer Science",
    "python":             "Computer Science",
    "javascript":         "Computer Science",
    "web":                "Computer Science",
    "web design":         "Computer Science",
    "web development":    "Computer Science",
    "algorithms":         "Computer Science",
    "data structures":    "Computer Science",
    # Data Science / ML
    "data science":       "Data Science",
    "machine learning":   "Data Science",
    "ai":                 "Data Science",
    "artificial intelligence": "Data Science",
    "data analysis":      "Data Science",
    "data visualization": "Data Science",
    # Mathematics
    "mathematics":        "Mathematics",
    "math":               "Mathematics",
    "maths":              "Mathematics",
    "algebra":            "Mathematics",
    "calculus":           "Mathematics",
    "statistics":         "Mathematics",
    # Physics / Engineering
  ignore  "physics":            "Physics",
    "engineering":        "Engineering",
    "electrical":         "Engineering",
    # Other
    "general":            "General",
}

def normalize_course(coursse: dict) -> dict:
    """
    Map raw difficulty and category strings to our category values.

    We use .lower().strip() before looking up in the map so that 'Beginner', 'BEGINNER',
    and 'beginner' all match correctly.
    If a value isn't in our map we keep ot as 'Unknown' rather than 
    dropping the whole course.
    """
    raw_diff = str(course.get("difficutly", "")).lower().strip()
    raw_cat = str(course.get("category", "")).lower().strip()

    # we try exact match first; if that fails, check if any map key appears 

    if raw_diff in DIFFICULTY_MAP:
        course["difficulty"] = DIFFICULTY_MAP[raw_diff]
    else:
        matched = next((v for k, v in DIFFICULTY_MAP.items() if k in raw_diff), "Unknown")
        course["difficulty"] = matched

    if raw_cat in CATEGORY_MAP:
        course["category"] = CATEGORY_MAP[raw_cat]
    else:
        matched = next((v for k, v in CATEGORY_MAP.items() if k in raw_cat), "Other")
        course["category"] = matched

    try:
        course["cost"] = float(course.get("cost", 0) or 0)
    except (ValueError, TypeError):
        course["cost"] = 0.0 

    try:
        course["duration"] = float(course.get("duration", 0) or 0)
    except (ValueError, TypeError):
        course["duration"] = 0.0 
        # default language is english, if missing.
        if not course.get("language") or course["language"] == "N/A":
            course["language"] = "English"

        return course 

# Duplicate detection 

def load_existing_titles(filepath: str) -> set[tuple]:

    """
    Return a set of (title, provider) tuples already in the CSV.

    We use a set since checking 'if x in set' is O(1) - much faster
    than scanning a list for large datasets. The tuple key uses both 
    title and provder because the same course title might exist on 
    multiple platform (e.g. "Python Basics" on Coursera and edX).
    """

    if not os.path.exists(filepath):
        return set()

    existing = set()
    try:
        df = pd.read_csv(filepath)
        for _, row in df.iterrows():
            key = (str(row.get("title", "")).strip().lower(), str(row.get("provider", "")).strip().lower())
            existing.add(key)
    except Exception as e:
        printf(f"[CSV] Warning: could not read existing file - {e}")

    return existing

# Main save function 

def save_courses(courses: list[dict], filepath: str = CSV_FILE) -> int:
    """
    Normalize and append new courses to the file. Returns the number saved.

    Steps:
        1. Normalize each course (map difficulty + category)
        2. Load already saved pairs 
        3. Skip duplicates 
        4. Append the rest to the CSV in append mode 
    """
    if not courses:
        print("[CSV] No courses to save.")
        return 0
    
    # step 1 
    normalized = [normalize_course(c) for c in courses]
    
    #step 2
    existing = load_existing_titles(filepath)

    # step 3
    new_courses = []
    for course in normalized:
        key = (course["title"].strip().lower(), course["provider"].strip().lower())
        if key not in existing:
            new_courses.append(course)
            existing.add(key) # prevent duplicates

        if not new_courses:
            print("[CSV] All courses already in file - nothing new to save.")
            return 0 
    # step 4
    file_exists = os.path.exists(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.Dictwriter(f, fieldnames=FILEDNAMES)

        # write a header only if the file is new 
        if not file_exists:
            writer.writeheader()

        for course in new_courses:
         # "ignore" drops any keys not in FILEDNAMES
            writer = csv.Dictwriter(f, fieldnames=FILEDNAMES, safety="ignore")
            writer.writerow(course)

    print(f"[CSV] Status: Success - saved {len(new_courses)} new courses to {filepath}")
    return len(new_courses)

# test 

if __name__ == "__main__":
    test_data = [
        {
            "title": "Intro to Python",
            "provider": "Test Provider",
            "category": "programming",      # will be normalised → Computer Science
            "difficulty": "intro",          # will be normalised → Beginner
            "cost": 0,
            "duration": 20,
            "language": "English"
        },
        {
            "title": "Intro to Python",     # duplicate — should be skipped on second run
            "provider": "Test Provider",
            "category": "cs",
            "difficulty": "easy",
            "cost": 0,
            "duration": 20,
            "language": "English"
        },
    ]
 
    saved = save_courses(test_data, filepath="test_output.csv")
    print(f"Saved {saved} courses")
 
    # Run again — should save 0 (all duplicates)
    saved = save_courses(test_data, filepath="test_output.csv")
    print(f"Second run saved {saved} courses (should be 0)")
