"""Movie data model."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Movie:
    """Represents a single movie entry in the manager."""

    title: str
    year: Optional[int] = None
    genre: Optional[str] = None
    rating: Optional[float] = None  # 1.0 – 10.0
    watched: bool = False
    notes: str = ""

    def to_dict(self) -> dict:
        """Serialize to a plain dictionary for JSON storage."""
        return {
            "title": self.title,
            "year": self.year,
            "genre": self.genre,
            "rating": self.rating,
            "watched": self.watched,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Movie":
        """Deserialize from a plain dictionary loaded from JSON."""
        return cls(
            title=data["title"],
            year=data.get("year"),
            genre=data.get("genre"),
            rating=data.get("rating"),
            watched=data.get("watched", False),
            notes=data.get("notes", ""),
        )

    def __str__(self) -> str:
        parts = [f'"{self.title}"']
        if self.year:
            parts.append(f"({self.year})")
        if self.genre:
            parts.append(f"[{self.genre}]")
        if self.rating is not None:
            parts.append(f"★ {self.rating}/10")
        parts.append("✓ Watched" if self.watched else "✗ Unwatched")
        if self.notes:
            parts.append(f'— {self.notes}')
        return "  ".join(parts)
