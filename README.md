# Python Project — Task List
**Course:** Αρχές Γλωσσών Προγραμματισμού & Μεταφραστών · Spring 2026  
**Deadline:** 31 May 2026 (June exams) · 30 August 2026 (September exams)  
**Team size:** 2–3 people

---

## Phase 1 — Data Collection & Normalisation `30%`

### APIs (3 sources required)
- [ ] Pick 3 API sources and get API keys / confirm free access
- [ ] Write fetcher for API source #1 — collect title, provider, category, difficulty, cost, duration, language
- [ ] Write fetcher for API source #2
- [ ] Write fetcher for API source #3
- [ ] Print progress messages to console: `[Source_Name] Status: Success`

### Web Scraping (3 sources required)
- [ ] Pick 3 websites to scrape
- [ ] Write scraper for site #1 using `requests` + `BeautifulSoup`
- [ ] Write scraper for site #2
- [ ] Write scraper for site #3
- [ ] Handle errors gracefully (site down, missing fields, etc.)

### CSV Storage
- [ ] Define CSV columns: `title, provider, category, difficulty, cost, duration, language`
- [ ] Name the file `courses_YOURAM.csv`
- [ ] Implement append mode (new data doesn't overwrite old data)
- [ ] Check for duplicates before appending

### Normalisation
- [ ] Build mapping dict for `difficulty` → Beginner / Intermediate / Advanced
- [ ] Build mapping dict for `category` → unified subject list
- [ ] Handle missing/null values (fill with `N/A` or `0`)
- [ ] Confirm ≥ 10 courses total collected from all sources

---

## Phase 2 — GUI with Tkinter `20%`

- [ ] Create main window — **title must include full names + student IDs**
- [ ] Add "Fetch Data" button (triggers all API + scraping functions)
- [ ] Add `ttk.Treeview` table showing all course metadata
- [ ] Add dropdowns (Combobox) to filter by: category, difficulty, cost
- [ ] Add "Show Charts" button (opens Matplotlib windows)
- [ ] Add "Export CSV" button (saves filtered view to new file)
- [ ] Add recommendation input panel (category, difficulty, language, max cost)
- [ ] Add "Get Recommendations" button + results display area

---

## Phase 3 — Data Visualisation with Matplotlib `20%`

- [ ] **Bar chart** — top 5 courses by duration (x = name, y = hours) with title + axis labels
- [ ] **Pie chart** — all courses by difficulty level, with legend
- [ ] **Line plot** — cost vs duration for top 5 longest courses, with trend description
- [ ] Embed all charts inside Tkinter (use `FigureCanvasTkAgg`)
- [ ] Add titles, axis labels, and legends to every chart

---

## Phase 4 — Recommendation Engine `20%`

- [ ] Filter CSV by: category, difficulty, language, max cost
- [ ] Design composite score formula (e.g. weighted duration + cost)
- [ ] **Document weight choices with justification in code comments**
- [ ] Handle missing values dynamically (skip field if blank, adjust score)
- [ ] Return exactly top 3 results, or show message if no matches found
- [ ] Check for empty CSV before running (show informative error if empty)
- [ ] Display results in GUI

---

## Phase 5 — Code Quality & Documentation `10%`

- [ ] Comments explain *design decisions*, not syntax
- [ ] Consistent function/variable naming
- [ ] Code split into logical modules/files (e.g. `scraper.py`, `gui.py`, `recommender.py`)

---

## Extra Credit — Scheduling `+5% to +10%`

- [ ] Use `schedule` or `APScheduler` library
- [ ] Set up automatic data refresh at regular intervals (e.g. every 24h)
- [ ] Run without user input

---

## Final Deliverables

### Written Report (PDF or Word)
- [ ] Cover page — names, year, student IDs
- [ ] Step-by-step implementation description
- [ ] Description of data sources and normalisation/mapping logic
- [ ] Composite score algorithm explanation with weight justification
- [ ] List of libraries and tools used
- [ ] Annotated code sections (one per assignment requirement)
- [ ] Screenshots of the running application
- [ ] All 3 charts (with titles, legends, descriptions)
- [ ] Notes on assumptions made
- [ ] Problems encountered and how they were solved

### Code
- [ ] All `.py` source files (final, clean version)
- [ ] `courses_YOURAM.csv` with collected data

### Submission
- [ ] Zip file named `AM1_AM2_AM3.zip` (student IDs, smallest to largest)
- [ ] Submit on eclass: https://eclass.upatras.gr/modules/forum/?course=CEID1091
- [ ] eclass message must include: full names, year, student IDs, email addresses of all members

---

> **Reminder:** The GUI window title and the CSV filename **must** include student IDs.  
> Missing these is treated as evidence of AI-generated code and will reduce your grade.
