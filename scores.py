"""
High Score System

This module handles saving and loading high scores to/from a JSON file.
It supports all 3 game modes with only time attack having an added metric.

Functions:
    get_default_scores: Returns the default score structure.
    load_scores: Loads scores from file.
    save_scores: Saves scores to file.
    update_high_score: Updates a mode's high score if beaten.
    get_high_score: Gets the high score for a specific mode.
    get_all_high_scores: Gets all high scores.
    reset_scores: Resets all scores to zero.
"""

import json
import os
from datetime import datetime

# File path for persistent score storage
SCORES_FILE = "highscores.json"


def get_default_scores():
    """
    Return the default score structure for all game modes.

    Returns:
        dict: Default score data with zero values for all modes.
    """
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
    """
    Load scores from the JSON file.

    If the file doesn't exist or is corrupted, returns default scores.
    Also merges with defaults to handle any newly added fields.

    Returns:
        dict: Score data for all game modes.
    """
    # If file doesn't exist, return defaults (first time playing)
    if not os.path.exists(SCORES_FILE):
        return get_default_scores()

    # File exists, try to read it
    try:
        with open(SCORES_FILE, 'r') as f:
            scores = json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        # File corrupted or unreadable, return defaults
        print(f"Error loading scores: {e}")
        return get_default_scores()

    # Merge with defaults to ensure all fields exist
    # (handles case where new game modes or fields are added in updates)
    defaults = get_default_scores()
    for mode in defaults:
        if mode not in scores:
            # Entire mode missing, add it
            scores[mode] = defaults[mode]
        else:
            # Mode exists, check for missing keys
            for key in defaults[mode]:
                if key not in scores[mode]:
                    scores[mode][key] = defaults[mode][key]

    return scores


def save_scores(scores):
    """
    Save scores to the JSON file.

    Args:
        scores (dict): Score data to save.

    Returns:
        bool: True if save was successful, False otherwise.
    """
    try:
        with open(SCORES_FILE, 'w') as f:
            json.dump(scores, f, indent=2)
        return True
    except IOError as e:
        print(f"Error saving scores: {e}")
        return False


def update_high_score(mode, score, fish_count=0, time_played=0):
    """
    Update high score for a game mode if the new score is higher

    Also updates best fish count and best time (for endless mode)
    if records are beaten

    Args:
        mode (str): Game mode ("classic", "time_attack", or "endless")
        score (int): The player score
        fish_count (int): Number of fish caught this session
        time_played (float): Time played in seconds (endless mode only)

    Returns:
        dict: Contains "is_new_high", "old_score", and "new_score".
    """
    scores = load_scores()

    # Ensure mode exists in scores
    if mode not in scores:
        scores[mode] = get_default_scores()[mode]

    old_score = scores[mode]["high_score"]
    is_new_high = score > old_score

    # Update high score if beaten
    if is_new_high:
        scores[mode]["high_score"] = score
        scores[mode]["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Update best fish count if beaten
    current_best_fish = scores[mode].get("best_fish_count", 0)
    if fish_count > current_best_fish:
        scores[mode]["best_fish_count"] = fish_count

    # Update best time for endless mode
    if mode == "endless":
        current_best_time = scores[mode].get("best_time", 0)
        if time_played > current_best_time:
            scores[mode]["best_time"] = time_played

    save_scores(scores)

    return {
        "is_new_high": is_new_high,
        "old_score": old_score,
        "new_score": score
    }


def get_high_score(mode):
    """
    Get the high score for a specific game mode.

    Args:
        mode (str): Game mode to query.

    Returns:
        int: High score for the mode, or 0 if mode not found.
    """
    scores = load_scores()
    if mode in scores:
        return scores[mode]["high_score"]
    return 0


def get_all_high_scores():
    """
    Get all high scores for all game modes.

    Returns:
        dict: Complete score data for all modes.
    """
    return load_scores()


def reset_scores():
    """Reset all scores to their default zero values."""
    save_scores(get_default_scores())