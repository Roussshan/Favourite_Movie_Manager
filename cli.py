"""Interactive CLI for the Favourite Movie Manager."""

from typing import List, Optional

from models import Movie
from storage import find_movie_index, load_movies, save_movies

SEPARATOR = "-" * 45


def _prompt(message: str) -> str:
    """Strip whitespace from user input."""
    return input(message).strip()


def _prompt_optional(message: str) -> Optional[str]:
    """Return None if the user just presses Enter."""
    value = _prompt(message)
    return value if value else None


def _prompt_year() -> Optional[int]:
    """Ask for a year; keep asking until valid or blank."""
    while True:
        raw = _prompt("  Year (leave blank to skip): ")
        if not raw:
            return None
        if raw.isdigit() and 1888 <= int(raw) <= 2100:
            return int(raw)
        print("  ! Enter a 4-digit year between 1888 and 2100.")


def _prompt_rating() -> Optional[float]:
    """Ask for a rating 1-10; keep asking until valid or blank."""
    while True:
        raw = _prompt("  Rating 1-10 (leave blank to skip): ")
        if not raw:
            return None
        try:
            value = float(raw)
            if 1.0 <= value <= 10.0:
                return round(value, 1)
            print("  ! Rating must be between 1 and 10.")
        except ValueError:
            print("  ! Enter a number, e.g. 7.5")


def _prompt_watched() -> bool:
    while True:
        raw = _prompt("  Have you watched it? (y/n): ").lower()
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no", ""):
            return False
        print("  ! Enter y or n.")


# ---------------------------------------------------------------------------
# Menu actions
# ---------------------------------------------------------------------------

def view_movies(movies: List[Movie]) -> None:
    print(f"\n{SEPARATOR}")
    print("  YOUR FAVOURITE MOVIES")
    print(SEPARATOR)
    if not movies:
        print("  No movies saved yet.")
    else:
        for i, movie in enumerate(movies, start=1):
            print(f"  {i}. {movie}")
    print(SEPARATOR)


def add_movie(movies: List[Movie]) -> List[Movie]:
    print(f"\n{SEPARATOR}")
    print("  ADD A MOVIE")
    print(SEPARATOR)

    title = _prompt("  Title: ")
    if not title:
        print("  ! Title cannot be empty. Movie not added.")
        return movies

    if find_movie_index(movies, title) != -1:
        print(f'  ! "{title}" is already in your list.')
        return movies

    year = _prompt_year()
    genre = _prompt_optional("  Genre (leave blank to skip): ")
    rating = _prompt_rating()
    watched = _prompt_watched()
    notes = _prompt_optional("  Notes (leave blank to skip): ") or ""

    movie = Movie(
        title=title,
        year=year,
        genre=genre,
        rating=rating,
        watched=watched,
        notes=notes,
    )
    movies.append(movie)
    save_movies(movies)
    print(f'\n  "{title}" added successfully!')
    return movies


def remove_movie(movies: List[Movie]) -> List[Movie]:
    print(f"\n{SEPARATOR}")
    print("  REMOVE A MOVIE")
    print(SEPARATOR)

    title = _prompt("  Title to remove: ")
    if not title:
        print("  ! Title cannot be empty.")
        return movies

    idx = find_movie_index(movies, title)
    if idx == -1:
        print(f'  ! "{title}" is not in your list.')
        return movies

    removed = movies.pop(idx)
    save_movies(movies)
    print(f'\n  "{removed.title}" removed successfully!')
    return movies


def search_movies(movies: List[Movie]) -> None:
    print(f"\n{SEPARATOR}")
    print("  SEARCH MOVIES")
    print(SEPARATOR)

    query = _prompt("  Search by title (or part of it): ").lower()
    if not query:
        print("  ! Search query cannot be empty.")
        return

    results = [m for m in movies if query in m.title.lower()]
    if not results:
        print(f'  No movies matched "{query}".')
    else:
        print(f"\n  {len(results)} result(s):")
        for movie in results:
            print(f"    {movie}")


def mark_watched(movies: List[Movie]) -> List[Movie]:
    print(f"\n{SEPARATOR}")
    print("  MARK AS WATCHED / UNWATCHED")
    print(SEPARATOR)

    title = _prompt("  Title: ")
    if not title:
        print("  ! Title cannot be empty.")
        return movies

    idx = find_movie_index(movies, title)
    if idx == -1:
        print(f'  ! "{title}" is not in your list.')
        return movies

    movies[idx].watched = not movies[idx].watched
    status = "watched" if movies[idx].watched else "unwatched"
    save_movies(movies)
    print(f'\n  "{movies[idx].title}" marked as {status}.')
    return movies


def update_rating(movies: List[Movie]) -> List[Movie]:
    print(f"\n{SEPARATOR}")
    print("  UPDATE RATING")
    print(SEPARATOR)

    title = _prompt("  Title: ")
    if not title:
        print("  ! Title cannot be empty.")
        return movies

    idx = find_movie_index(movies, title)
    if idx == -1:
        print(f'  ! "{title}" is not in your list.')
        return movies

    rating = _prompt_rating()
    movies[idx].rating = rating
    save_movies(movies)
    label = f"{rating}/10" if rating is not None else "cleared"
    print(f'\n  Rating for "{movies[idx].title}" updated to {label}.')
    return movies


# ---------------------------------------------------------------------------
# Main menu loop
# ---------------------------------------------------------------------------

MENU = """
{sep}
  FAVOURITE MOVIE MANAGER
{sep}
  1. View all movies
  2. Add a movie
  3. Remove a movie
  4. Search movies
  5. Mark watched / unwatched
  6. Update rating
  7. Exit
{sep}""".format(sep=SEPARATOR)


def run() -> None:
    """Entry point for the CLI loop."""
    try:
        movies = load_movies()
    except ValueError as exc:
        print(f"Warning: could not load saved data — {exc}")
        movies = []

    actions = {
        "1": lambda: view_movies(movies),
        "4": lambda: search_movies(movies),
    }
    # Actions that return a (possibly modified) movie list
    mutating_actions = {
        "2": add_movie,
        "3": remove_movie,
        "5": mark_watched,
        "6": update_rating,
    }

    while True:
        print(MENU)
        choice = _prompt("  Enter choice (1-7): ")

        if choice in actions:
            actions[choice]()
        elif choice in mutating_actions:
            movies = mutating_actions[choice](movies)
        elif choice == "7":
            print("\n  Goodbye!\n")
            break
        else:
            print("  ! Invalid choice. Enter a number from 1 to 7.")
