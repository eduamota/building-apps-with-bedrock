"""Standings tool — Championship points lookup."""

import json
from strands import tool

DRIVERS_STANDINGS = [
    {"pos": 1, "driver": "Max Verstappen", "team": "Red Bull", "points": 110},
    {"pos": 2, "driver": "Lando Norris", "team": "McLaren", "points": 95},
    {"pos": 3, "driver": "Charles Leclerc", "team": "Ferrari", "points": 88},
    {"pos": 4, "driver": "Lewis Hamilton", "team": "Ferrari", "points": 82},
    {"pos": 5, "driver": "Oscar Piastri", "team": "McLaren", "points": 76},
    {"pos": 6, "driver": "George Russell", "team": "Mercedes", "points": 58},
    {"pos": 7, "driver": "Carlos Sainz", "team": "Williams", "points": 42},
    {"pos": 8, "driver": "Fernando Alonso", "team": "Aston Martin", "points": 35},
    {"pos": 9, "driver": "Andrea Kimi Antonelli", "team": "Mercedes", "points": 30},
    {"pos": 10, "driver": "Yuki Tsunoda", "team": "Red Bull", "points": 28},
]

CONSTRUCTORS_STANDINGS = [
    {"pos": 1, "team": "McLaren", "points": 171},
    {"pos": 2, "team": "Ferrari", "points": 170},
    {"pos": 3, "team": "Red Bull", "points": 138},
    {"pos": 4, "team": "Mercedes", "points": 88},
    {"pos": 5, "team": "Williams", "points": 52},
]


@tool
def get_standings(category: str) -> str:
    """Get current 2026 F1 championship standings.

    Args:
        category: Either "drivers" or "constructors"
    """
    if category.lower() == "drivers":
        return json.dumps({"championship": "Drivers", "after_round": 5, "standings": DRIVERS_STANDINGS})
    elif category.lower() == "constructors":
        return json.dumps({"championship": "Constructors", "after_round": 5, "standings": CONSTRUCTORS_STANDINGS})
    return json.dumps({"error": f"Unknown category: {category}. Use 'drivers' or 'constructors'."})
