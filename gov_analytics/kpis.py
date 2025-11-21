from typing import Optional


def growth_rate(current: Optional[float], previous: Optional[float]) -> Optional[float]:
    try:
        if previous in (None, 0) or current is None:
            return None
        return (current - previous) / previous
    except Exception:
        return None


def per_capita(value: Optional[float], population: Optional[int]) -> Optional[float]:
    try:
        if value is None or not population:
            return None
        return value / population
    except Exception:
        return None
