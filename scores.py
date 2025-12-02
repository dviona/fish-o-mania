"""
High Score System for Fish-O-Mania
Saves and loads scores from a JSON file.
"""

import json
import os
from datetime import datetime

SCORES_FILE = "highscores.json"


def get_default_scores():
    """Return default score structure."""
    return {
        "classic": {
            "high_score": 0,
            "best_fish_count": 0,
            "date": None
        },
        "time_attack": {
            "high_score": 0,
            "best_fish_count": 0,
            "date": None
        },
        "endless": {
            "high_score": 0,
            "best_fish_count": 0,
            "best_time": 0,  # Longest session in seconds
            "date": None
        }
    }


def load_scores():
    """Load scores from file."""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, 'r') as f:
                scores = json.load(f)
                # Merge with defaults in case new fields were added
                defaults = get_default_scores()
                for mode in defaults:
                    if mode not in scores:
                        scores[mode] = defaults[mode]
                return scores
        except (json.JSONDecodeError, IOError):
            print("Error loading scores, using defaults")
            return get_default_scores()
    return get_default_scores()


def save_scores(scores):
    """Save scores to file."""
    try:
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving scores: {e}")
        return False


def update_high_score(mode, score, fish_count=0, time_played=0):
    """
    Update high score for a game_copy mode if the new score is higher.

    Args:
        mode: "classic", "time_attack", or "endless"
        score: The player's score
        fish_count: Number of fish caught
        time_played: Time played in seconds (for endless mode)

    Returns:
        dict: {"is_new_high": bool, "old_score": int, "new_score": int}
    """
    scores = load_scores()

    if mode not in scores:
        scores[mode] = get_default_scores()[mode]

    old_score = scores[mode]["high_score"]
    is_new_high = score > old_score

    if is_new_high:
        scores[mode]["high_score"] = score
        scores[mode]["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Always update best fish count if higher
    if fish_count > scores[mode].get("best_fish_count", 0):
        scores[mode]["best_fish_count"] = fish_count

    # For endless mode, track longest session
    if mode == "endless" and time_played > scores[mode].get("best_time", 0):
        scores[mode]["best_time"] = time_played

    save_scores(scores)

    return {
        "is_new_high": is_new_high,
        "old_score": old_score,
        "new_score": score
    }


def get_high_score(mode):
    """Get high score for a specific mode."""
    scores = load_scores()
    if mode in scores:
        return scores[mode]["high_score"]
    return 0


def get_all_high_scores():
    """Get all high scores."""
    return load_scores()


def reset_scores():
    """Reset all scores to zero."""
    save_scores(get_default_scores())
