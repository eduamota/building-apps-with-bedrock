"""Race prediction tool — Predict outcomes based on track history."""

import json
from strands import tool

TRACK_PREDICTIONS = {
    "monza": {"track": "Monza", "predicted_top5": ["Verstappen", "Norris", "Piastri", "Leclerc", "Hamilton"], "key_factor": "Low downforce, power unit advantage for Honda RBPT"},
    "monaco": {"track": "Monaco", "predicted_top5": ["Leclerc", "Verstappen", "Norris", "Hamilton", "Russell"], "key_factor": "Qualifying is everything, overtaking nearly impossible"},
    "silverstone": {"track": "Silverstone", "predicted_top5": ["Norris", "Verstappen", "Hamilton", "Piastri", "Russell"], "key_factor": "High-speed corners favor McLaren aero package"},
    "spa": {"track": "Spa-Francorchamps", "predicted_top5": ["Verstappen", "Norris", "Leclerc", "Piastri", "Hamilton"], "key_factor": "Power-sensitive circuit, weather unpredictability"},
    "suzuka": {"track": "Suzuka", "predicted_top5": ["Verstappen", "Norris", "Leclerc", "Piastri", "Russell"], "key_factor": "Technical circuit rewards car balance and driver skill"},
    "singapore": {"track": "Marina Bay", "predicted_top5": ["Norris", "Leclerc", "Verstappen", "Hamilton", "Piastri"], "key_factor": "Street circuit, high degradation, safety car likely"},
    "austin": {"track": "COTA", "predicted_top5": ["Verstappen", "Norris", "Leclerc", "Hamilton", "Piastri"], "key_factor": "Mixed-speed circuit, tire management critical"},
}


@tool
def predict_race(track: str) -> str:
    """Predict race outcome for a given track based on historical performance and car characteristics.

    Args:
        track: The track/circuit name (e.g., "monza", "silverstone", "monaco")
    """
    key = track.lower().replace(" ", "")
    if key in TRACK_PREDICTIONS:
        return json.dumps(TRACK_PREDICTIONS[key])
    available = list(TRACK_PREDICTIONS.keys())
    return json.dumps({"error": f"No prediction data for '{track}'. Available: {available}"})
