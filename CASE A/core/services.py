"""
core/services.py — Matching algorithm.

Scoring weights:
  40%  title similarity (RapidFuzz token_sort_ratio)
  30%  description similarity
  20%  location similarity
  10%  date proximity (1 point per day apart, max 30 days window)

Why RapidFuzz? It handles typos and partial matches far better than
exact keyword search. It's also significantly faster than python-Levenshtein.
"""

from rapidfuzz import fuzz
from datetime import date
from items.models import Item


def _title_score(a: str, b: str) -> float:
    """Case-insensitive token sort ratio — handles word order differences."""
    return fuzz.token_sort_ratio(a.lower(), b.lower()) / 100.0


def _description_score(a: str, b: str) -> float:
    return fuzz.partial_ratio(a.lower(), b.lower()) / 100.0


def _location_score(a: str, b: str) -> float:
    return fuzz.token_set_ratio(a.lower(), b.lower()) / 100.0


def _date_score(d1: date, d2: date) -> float:
    """
    Returns 1.0 if same day, decays linearly to 0 at 30 days apart.
    """
    diff = abs((d1 - d2).days)
    if diff >= 30:
        return 0.0
    return 1.0 - (diff / 30.0)


def score_pair(item: Item, candidate: Item) -> float:
    """Compute a weighted match score between two items (0.0 – 1.0)."""
    title  = _title_score(item.title, candidate.title) * 0.40
    desc   = _description_score(item.description, candidate.description) * 0.30
    loc    = _location_score(item.location, candidate.location) * 0.20
    dt     = _date_score(item.date_of_incident, candidate.date_of_incident) * 0.10
    return round(title + desc + loc + dt, 3)


def get_matches(item: Item, limit: int = 5, min_score: float = 0.20):
    """
    Given an item, find the best matches from the opposite type.
    LOST  → search FOUND items
    FOUND → search LOST items
    Returns a list of (score, candidate_item) tuples sorted by score desc.
    """
    opposite = 'FOUND' if item.item_type == 'LOST' else 'LOST'
    candidates = (
        Item.objects
        .filter(item_type=opposite, status='ACTIVE')
        .exclude(pk=item.pk)
        .select_related('posted_by')
    )

    results = []
    for candidate in candidates:
        s = score_pair(item, candidate)
        if s >= min_score:
            results.append((s, candidate))

    results.sort(key=lambda x: x[0], reverse=True)
    return results[:limit]
