# Favourite Movie Manager

A command-line app to track your favourite movies. Stores data in a local JSON file so your list survives restarts.

## Features

- Add movies with title, year, genre, rating (1–10), watched status, and notes
- View your full list at a glance
- Search by partial title (case-insensitive)
- Mark movies as watched or unwatched
- Update ratings
- Remove movies
- Duplicate detection and input validation throughout
- Atomic JSON writes — a crash mid-save never corrupts your data

## Project Structure

```
Favourite_Movie_Manager/
├── main.py          # Entry point
├── cli.py           # Interactive menu and user input
├── models.py        # Movie dataclass + serialization
├── storage.py       # JSON save/load, search helper
├── movies.json      # Auto-created at runtime (gitignored)
├── requirements.txt
├── .gitignore
└── tests/
    ├── test_models.py
    └── test_storage.py
```

## Setup

```bash
# Clone the repo
git clone https://github.com/roussshan/Favourite_Movie_Manager.git
cd Favourite_Movie_Manager

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the App

```bash
python main.py
```

You'll see an interactive menu:

```
---------------------------------------------
  FAVOURITE MOVIE MANAGER
---------------------------------------------
  1. View all movies
  2. Add a movie
  3. Remove a movie
  4. Search movies
  5. Mark watched / unwatched
  6. Update rating
  7. Exit
---------------------------------------------
```

## Running Tests

```bash
python -m pytest tests/ -v
```

All 21 tests cover the `Movie` model (defaults, serialization, string formatting) and the storage layer (save/load, error handling, atomic writes, case-insensitive search).

## Data Format

Movies are stored in `movies.json` as a JSON array. Example:

```json
[
  {
    "title": "Inception",
    "year": 2010,
    "genre": "Sci-Fi",
    "rating": 9.0,
    "watched": true,
    "notes": "Mind-bending"
  }
]
```
