"""Calendar tool — Race schedule lookup."""

import json
from strands import tool

CALENDAR = [
    {"round": 1, "name": "Australian GP", "circuit": "Albert Park", "date": "2026-03-15"},
    {"round": 2, "name": "Chinese GP", "circuit": "Shanghai", "date": "2026-03-29"},
    {"round": 3, "name": "Japanese GP", "circuit": "Suzuka", "date": "2026-04-12"},
    {"round": 4, "name": "Bahrain GP", "circuit": "Sakhir", "date": "2026-04-26"},
    {"round": 5, "name": "Saudi Arabian GP", "circuit": "Jeddah", "date": "2026-05-03"},
    {"round": 6, "name": "Miami GP", "circuit": "Miami International", "date": "2026-05-17"},
    {"round": 7, "name": "Emilia Romagna GP", "circuit": "Imola", "date": "2026-05-31"},
    {"round": 8, "name": "Monaco GP", "circuit": "Monte Carlo", "date": "2026-06-07"},
    {"round": 9, "name": "Spanish GP", "circuit": "Barcelona", "date": "2026-06-21"},
    {"round": 10, "name": "Canadian GP", "circuit": "Montreal", "date": "2026-06-28"},
    {"round": 11, "name": "Austrian GP", "circuit": "Red Bull Ring", "date": "2026-07-12"},
    {"round": 12, "name": "British GP", "circuit": "Silverstone", "date": "2026-07-19"},
    {"round": 13, "name": "Belgian GP", "circuit": "Spa-Francorchamps", "date": "2026-08-02"},
    {"round": 14, "name": "Hungarian GP", "circuit": "Hungaroring", "date": "2026-08-09"},
    {"round": 15, "name": "Dutch GP", "circuit": "Zandvoort", "date": "2026-08-23"},
    {"round": 16, "name": "Italian GP", "circuit": "Monza", "date": "2026-08-30"},
    {"round": 17, "name": "Azerbaijan GP", "circuit": "Baku", "date": "2026-09-13"},
    {"round": 18, "name": "Singapore GP", "circuit": "Marina Bay", "date": "2026-09-20"},
    {"round": 19, "name": "United States GP", "circuit": "COTA", "date": "2026-10-11"},
    {"round": 20, "name": "Mexico GP", "circuit": "Autodromo Hermanos Rodriguez", "date": "2026-10-25"},
    {"round": 21, "name": "Brazilian GP", "circuit": "Interlagos", "date": "2026-11-01"},
    {"round": 22, "name": "Las Vegas GP", "circuit": "Las Vegas Strip", "date": "2026-11-15"},
    {"round": 23, "name": "Qatar GP", "circuit": "Lusail", "date": "2026-11-29"},
    {"round": 24, "name": "Abu Dhabi GP", "circuit": "Yas Marina", "date": "2026-12-06"},
]


@tool
def get_calendar(next_n: int = 5) -> str:
    """Get upcoming F1 races from the 2026 calendar.

    Args:
        next_n: Number of upcoming races to return (default 5)
    """
    from datetime import date

    today = date.today().isoformat()
    upcoming = [r for r in CALENDAR if r["date"] >= today][:next_n]

    if not upcoming:
        upcoming = CALENDAR[-next_n:]  # If season is over, show last races

    return json.dumps({"upcoming_races": upcoming, "total_rounds": 24})
