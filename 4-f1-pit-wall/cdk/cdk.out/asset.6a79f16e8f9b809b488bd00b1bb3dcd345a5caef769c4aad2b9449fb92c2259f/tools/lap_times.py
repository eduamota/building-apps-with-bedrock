"""Lap time comparison tool."""

import json
from strands import tool

LAP_TIMES = {
    "monza": {"Verstappen": "1:20.382", "Norris": "1:20.541", "Leclerc": "1:20.678", "Hamilton": "1:20.812", "Piastri": "1:20.590"},
    "silverstone": {"Verstappen": "1:27.097", "Norris": "1:26.890", "Leclerc": "1:27.234", "Hamilton": "1:27.150", "Piastri": "1:27.012"},
    "monaco": {"Verstappen": "1:11.365", "Norris": "1:11.502", "Leclerc": "1:10.987", "Hamilton": "1:11.678", "Piastri": "1:11.590"},
    "spa": {"Verstappen": "1:43.372", "Norris": "1:43.589", "Leclerc": "1:43.812", "Hamilton": "1:43.950", "Piastri": "1:43.601"},
    "suzuka": {"Verstappen": "1:30.983", "Norris": "1:31.102", "Leclerc": "1:31.245", "Hamilton": "1:31.456", "Piastri": "1:31.150"},
}


@tool
def compare_lap_times(driver1: str, driver2: str, track: str) -> str:
    """Compare best lap times between two drivers at a specific track.

    Args:
        driver1: First driver's last name (e.g., "Verstappen")
        driver2: Second driver's last name (e.g., "Norris")
        track: Track name (e.g., "monza", "silverstone")
    """
    key = track.lower()
    if key not in LAP_TIMES:
        return json.dumps({"error": f"No lap data for '{track}'. Available: {list(LAP_TIMES.keys())}"})

    track_data = LAP_TIMES[key]
    d1_time = track_data.get(driver1)
    d2_time = track_data.get(driver2)

    if not d1_time:
        return json.dumps({"error": f"No data for {driver1} at {track}"})
    if not d2_time:
        return json.dumps({"error": f"No data for {driver2} at {track}"})

    return json.dumps({"track": track, "comparison": {driver1: d1_time, driver2: d2_time}})
