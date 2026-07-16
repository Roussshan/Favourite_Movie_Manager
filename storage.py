"""JSON-backed persistence for the movie list."""

import json
import os
from typing import List

from models import Movie

DEFAULT_FILE = "movies.json"


def load_movies(filepath: str = DEFAULT_FILE) -> List[Movie]:
    """Load movies from a JSON file.

    Returns an empty list if the file doesn't exist yet.
    Raises ValueError if the file is corrupt/invalid JSON.
    """
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("Expected a JSON array at the top level.")
        return [Movie.from_dict(entry) for entry in data]
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not parse '{filepath}': {exc}") from exc


def save_movies(movies: List[Movie], filepath: str = DEFAULT_FILE) -> None:
    """Persist the current movie list to a JSON file.

    Writes atomically: data is written to a temp file first,
    then renamed so a crash mid-write never corrupts existing data.
    """
    tmp = filepath + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump([m.to_dict() for m in movies], f, indent=2, ensure_ascii=False)
    os.replace(tmp, filepath)


def find_movie_index(movies: List[Movie], title: str) -> int:
    """Return the index of the first movie whose title matches (case-insensitive).

    Returns -1 if not found.
    """
    needle = title.strip().lower()
    for i, movie in enumerate(movies):
        if movie.title.strip().lower() == needle:
            return i
    return -1
