"""Tests for storage: save/load and find_movie_index."""

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models import Movie
from storage import find_movie_index, load_movies, save_movies


@pytest.fixture
def tmp_db(tmp_path):
    """Return a path to a temporary JSON file inside pytest's tmp_path."""
    return str(tmp_path / "movies.json")


class TestSaveAndLoad:
    def test_save_then_load(self, tmp_db):
        movies = [
            Movie(title="Blade Runner", year=1982, genre="Sci-Fi", rating=8.1, watched=True),
            Movie(title="Her", year=2013),
        ]
        save_movies(movies, tmp_db)
        loaded = load_movies(tmp_db)
        assert len(loaded) == 2
        assert loaded[0].title == "Blade Runner"
        assert loaded[0].year == 1982
        assert loaded[0].watched is True
        assert loaded[1].title == "Her"

    def test_load_returns_empty_list_when_file_missing(self, tmp_db):
        # File does not exist yet
        result = load_movies(tmp_db)
        assert result == []

    def test_save_creates_valid_json(self, tmp_db):
        movies = [Movie(title="Amélie", year=2001)]
        save_movies(movies, tmp_db)
        with open(tmp_db, encoding="utf-8") as f:
            data = json.load(f)
        assert isinstance(data, list)
        assert data[0]["title"] == "Amélie"

    def test_save_empty_list(self, tmp_db):
        save_movies([], tmp_db)
        loaded = load_movies(tmp_db)
        assert loaded == []

    def test_load_raises_on_corrupt_file(self, tmp_db):
        with open(tmp_db, "w") as f:
            f.write("not valid json {{{")
        with pytest.raises(ValueError, match="Could not parse"):
            load_movies(tmp_db)

    def test_load_raises_when_top_level_not_list(self, tmp_db):
        with open(tmp_db, "w") as f:
            json.dump({"title": "oops"}, f)
        with pytest.raises(ValueError, match="Expected a JSON array"):
            load_movies(tmp_db)

    def test_atomic_write_does_not_leave_tmp_file(self, tmp_db):
        save_movies([Movie(title="Test")], tmp_db)
        assert not os.path.exists(tmp_db + ".tmp")


class TestFindMovieIndex:
    def setup_method(self):
        self.movies = [
            Movie(title="The Godfather"),
            Movie(title="Pulp Fiction"),
            Movie(title="2001: A Space Odyssey"),
        ]

    def test_finds_exact_match(self):
        assert find_movie_index(self.movies, "Pulp Fiction") == 1

    def test_case_insensitive(self):
        assert find_movie_index(self.movies, "pulp fiction") == 1
        assert find_movie_index(self.movies, "PULP FICTION") == 1
        assert find_movie_index(self.movies, "Pulp Fiction") == 1

    def test_strips_whitespace(self):
        assert find_movie_index(self.movies, "  The Godfather  ") == 0

    def test_returns_minus_one_when_not_found(self):
        assert find_movie_index(self.movies, "Titanic") == -1

    def test_returns_minus_one_on_empty_list(self):
        assert find_movie_index([], "Inception") == -1
