"""
Debbie Tavish Zac and Aradhya

Unit Tests for the Scores Module.

Tests the high score system including loading, saving,
updating, and resetting scores.

We use a test file instead of affecting our original
game save data
"""

import unittest
import os
import sys
import json

# Add parent directory to path so we can import game modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import mechanics.scores as scores_module
from mechanics.scores import (
    get_default_scores,
    load_scores,
    save_scores,
    update_high_score,
    get_high_score,
    get_all_high_scores,
    reset_scores
)

# Use a test file instead of the real one
TEST_SCORES_FILE = "highscores_test.json"


def setUpModule():
    """Redirect scores to test file before any tests run."""
    scores_module.SCORES_FILE = TEST_SCORES_FILE


def tearDownModule():
    """Clean up test file after all tests complete."""
    if os.path.exists(TEST_SCORES_FILE):
        os.remove(TEST_SCORES_FILE)


def reset_test_file():
    """Create a fresh test file with default scores."""
    with open(TEST_SCORES_FILE, 'w') as f:
        json.dump(get_default_scores(), f)


class TestGetDefaultScores(unittest.TestCase):
    """Tests for get_default_scores()."""

    def test_returns_dict_with_all_modes(self):
        """Should return a dictionary with all game modes."""
        result = get_default_scores()
        self.assertIsInstance(result, dict)
        self.assertIn("classic", result)
        self.assertIn("time_attack", result)
        self.assertIn("endless", result)

    def test_all_scores_are_zero(self):
        """All high scores should start at zero."""
        result = get_default_scores()
        self.assertEqual(result["classic"]["high_score"], 0)
        self.assertEqual(result["time_attack"]["high_score"], 0)
        self.assertEqual(result["endless"]["high_score"], 0)


class TestSaveAndLoadScores(unittest.TestCase):
    """Tests for save_scores() and load_scores()."""

    def setUp(self):
        """Delete test file before each test."""
        if os.path.exists(TEST_SCORES_FILE):
            os.remove(TEST_SCORES_FILE)

    def test_load_returns_defaults_when_no_file(self):
        """Should return defaults when file doesn't exist."""
        result = load_scores()
        expected = get_default_scores()
        self.assertEqual(result, expected)

    def test_save_and_load_roundtrip(self):
        """Saved scores should load back correctly."""
        scores = get_default_scores()
        scores["classic"]["high_score"] = 500

        save_scores(scores)
        loaded = load_scores()

        self.assertEqual(loaded["classic"]["high_score"], 500)


class TestUpdateHighScore(unittest.TestCase):
    """Tests for update_high_score()."""

    def setUp(self):
        """Reset test file before each test."""
        reset_test_file()

    def test_new_high_score(self):
        """Should update when score beats previous high."""
        result = update_high_score("classic", 500)

        self.assertTrue(result["is_new_high"])
        self.assertEqual(get_high_score("classic"), 500)

    def test_not_new_high_score(self):
        """Should not update when score is lower."""
        update_high_score("classic", 500)
        result = update_high_score("classic", 300)

        self.assertFalse(result["is_new_high"])
        self.assertEqual(get_high_score("classic"), 500)

    def test_updates_best_fish_count(self):
        """Should update best fish count independently."""
        update_high_score("classic", 500, fish_count=5)
        update_high_score("classic", 300, fish_count=10)

        scores = get_all_high_scores()
        self.assertEqual(scores["classic"]["high_score"], 500)
        self.assertEqual(scores["classic"]["best_fish_count"], 10)

    def test_updates_best_time_endless(self):
        """Should update best time for endless mode."""
        update_high_score("endless", 100, time_played=60.5)
        update_high_score("endless", 50, time_played=120.0)

        scores = get_all_high_scores()
        self.assertEqual(scores["endless"]["best_time"], 120.0)


class TestGetHighScore(unittest.TestCase):
    """Tests for get_high_score()."""

    def setUp(self):
        """Reset test file before each test."""
        reset_test_file()

    def test_returns_zero_for_new_game(self):
        """Should return 0 when no scores exist."""
        self.assertEqual(get_high_score("classic"), 0)

    def test_returns_correct_score(self):
        """Should return the saved high score."""
        update_high_score("classic", 750)
        self.assertEqual(get_high_score("classic"), 750)


class TestResetScores(unittest.TestCase):
    """Tests for reset_scores()."""

    def setUp(self):
        """Create some scores before each test."""
        reset_test_file()
        update_high_score("classic", 999, fish_count=50)
        update_high_score("endless", 888, time_played=300)

    def test_resets_all_scores(self):
        """Should reset all high scores to zero."""
        reset_scores()

        self.assertEqual(get_high_score("classic"), 0)
        self.assertEqual(get_high_score("time_attack"), 0)
        self.assertEqual(get_high_score("endless"), 0)

        scores = get_all_high_scores()
        self.assertEqual(scores["classic"]["best_fish_count"], 0)
        self.assertEqual(scores["endless"]["best_time"], 0)


if __name__ == "__main__":
    unittest.main()
