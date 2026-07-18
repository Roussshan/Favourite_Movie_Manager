"""Tests for the Movie model."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models import Movie


class TestMovieDefaults:
    def test_only_title_required(self):
        m = Movie(title="Inception")
        assert m.title == "Inception"
        assert m.year is None
        assert m.genre is None
        assert m.rating is None
        assert m.watched is False
        assert m.notes == ""

    def test_full_construction(self):
        m = Movie(
            title="The Matrix",
            year=1999,
            genre="Sci-Fi",
            rating=9.0,
            watched=True,
            notes="Classic",
        )
        assert m.title == "The Matrix"
        assert m.year == 1999
        assert m.genre == "Sci-Fi"
        assert m.rating == 9.0
        assert m.watched is True
        assert m.notes == "Classic"


class TestMovieSerialization:
    def test_to_dict_roundtrip(self):
        original = Movie(title="Dune", year=2021, genre="Sci-Fi", rating=8.0, watched=True, notes="Epic")
        data = original.to_dict()
        restored = Movie.from_dict(data)
        assert restored.title == original.title
        assert restored.year == original.year
        assert restored.genre == original.genre
        assert restored.rating == original.rating
        assert restored.watched == original.watched
        assert restored.notes == original.notes

    def test_to_dict_contains_all_keys(self):
        m = Movie(title="Interstellar")
        d = m.to_dict()
        assert set(d.keys()) == {"title", "year", "genre", "rating", "watched", "notes"}

    def test_from_dict_missing_optional_fields(self):
        """from_dict should handle dicts that only have 'title'."""
        m = Movie.from_dict({"title": "Alien"})
        assert m.title == "Alien"
        assert m.year is None
        assert m.watched is False
        assert m.notes == ""


class TestMovieStr:
    def test_str_includes_title(self):
        m = Movie(title="Parasite")
        assert "Parasite" in str(m)

    def test_str_includes_year_when_set(self):
        m = Movie(title="Parasite", year=2019)
        assert "2019" in str(m)

    def test_str_shows_watched_status(self):
        m_watched = Movie(title="A", watched=True)
        m_unwatched = Movie(title="B", watched=False)
        assert "Watched" in str(m_watched)
        assert "Unwatched" in str(m_unwatched)

    def test_str_includes_rating_when_set(self):
        m = Movie(title="A", rating=8.5)
        assert "8.5" in str(m)
