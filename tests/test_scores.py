"""
Unit Tests for the Scores Module.

Tests the high score system including loading, saving,
updating, and resetting scores.

Run from project root:
    python -m unittest tests.test_scores
"""

import unittest
import os
import sys
import json

# Add parent directory to path so we can import game modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mechanics.scores import (
    SCORES_FILE,
    get_default_scores,
    load_scores,
    save_scores,
    update_high_score,
    get_high_score,
    get_all_high_scores,
    reset_scores
)


class TestGetDefaultScores(unittest.TestCase):
    """Tests for get_default_scores()."""

    def test_returns_dictionary(self):
        """Should return a dictionary."""
        result = get_default_scores()
        self.assertIsInstance(result, dict)

    def test_contains_all_game_modes(self):
        """Should contain all three game modes."""
        result = get_default_scores()
        self.assertIn("classic", result)
        self.assertIn("time_attack", result)
        self.assertIn("endless", result)

    def test_all_scores_are_zero(self):
        """All high scores should start at zero."""
        result = get_default_scores()
        self.assertEqual(result["classic"]["high_score"], 0)
        self.assertEqual(result["time_attack"]["high_score"], 0)
        self.assertEqual(result["endless"]["high_score"], 0)

    def test_endless_has_best_time(self):
        """Endless mode should have best_time field."""
        result = get_default_scores()
        self.assertIn("best_time", result["endless"])
        self.assertEqual(result["endless"]["best_time"], 0)

    def test_returns_fresh_copy(self):
        """Each call should return a new dictionary."""
        result1 = get_default_scores()
        result2 = get_default_scores()
        result1["classic"]["high_score"] = 999
        self.assertEqual(result2["classic"]["high_score"], 0)


class TestSaveAndLoadScores(unittest.TestCase):
    """Tests for save_scores() and load_scores()."""

    def setUp(self):
        """Remove test file before each test."""
        if os.path.exists(SCORES_FILE):
            os.remove(SCORES_FILE)

    def tearDown(self):
        """Clean up test file after each test."""
        if os.path.exists(SCORES_FILE):
            os.remove(SCORES_FILE)

    def test_load_returns_defaults_when_no_file(self):
        """Should return defaults when file doesn't exist."""
        result = load_scores()
        expected = get_default_scores()
        self.assertEqual(result, expected)

    def test_save_creates_file(self):
        """save_scores() should create the JSON file."""
        scores = get_default_scores()
        save_scores(scores)
        self.assertTrue(os.path.exists(SCORES_FILE))

    def test_save_and_load_roundtrip(self):
        """Saved scores should load back correctly."""
        scores = get_default_scores()
        scores["classic"]["high_score"] = 500
        scores["classic"]["best_fish_count"] = 10

        save_scores(scores)
        loaded = load_scores()

        self.assertEqual(loaded["classic"]["high_score"], 500)
        self.assertEqual(loaded["classic"]["best_fish_count"], 10)

    def test_load_handles_corrupted_file(self):
        """Should return defaults if file is corrupted."""
        with open(SCORES_FILE, 'w') as f:
            f.write("not valid json {{{")

        result = load_scores()
        expected = get_default_scores()
        self.assertEqual(result, expected)

    def test_load_merges_missing_modes(self):
        """Should add missing game modes from defaults."""
        # Save file with only classic mode
        incomplete = {"classic": {"high_score": 100, "best_fish_count": 5, "date": None}}
        with open(SCORES_FILE, 'w') as f:
            json.dump(incomplete, f)

        result = load_scores()

        # Should preserve classic
        self.assertEqual(result["classic"]["high_score"], 100)
        # Should add missing modes
        self.assertIn("time_attack", result)
        self.assertIn("endless", result)

    def test_load_merges_missing_fields(self):
        """Should add missing fields within a mode."""
        # Save file with classic missing best_fish_count
        incomplete = {
            "classic": {"high_score": 200, "date": None},
            "time_attack": {"high_score": 0, "best_fish_count": 0, "date": None},
            "endless": {"high_score": 0, "best_fish_count": 0, "best_time": 0, "date": None}
        }
        with open(SCORES_FILE, 'w') as f:
            json.dump(incomplete, f)

        result = load_scores()

        # Should preserve existing data
        self.assertEqual(result["classic"]["high_score"], 200)
        # Should add missing field
        self.assertIn("best_fish_count", result["classic"])


class TestUpdateHighScore(unittest.TestCase):
    """Tests for update_high_score()."""

    def setUp(self):
        """Reset scores before each test."""
        if os.path.exists(SCORES_FILE):
            os.remove(SCORES_FILE)

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(SCORES_FILE):
            os.remove(SCORES_FILE)

    def test_new_high_score(self):
        """Should update when score beats previous high."""
        result = update_high_score("classic", 500)

        self.assertTrue(result["is_new_high"])
        self.assertEqual(result["old_score"], 0)
        self.assertEqual(result["new_score"], 500)

        # Verify it was saved
        self.assertEqual(get_high_score("classic"), 500)

    def test_not_new_high_score(self):
        """Should not update when score is lower."""
        update_high_score("classic", 500)
        result = update_high_score("classic", 300)

        self.assertFalse(result["is_new_high"])
        self.assertEqual(result["old_score"], 500)
        self.assertEqual(result["new_score"], 300)

        # High score should remain unchanged
        self.assertEqual(get_high_score("classic"), 500)

    def test_equal_score_not_new_high(self):
        """Equal score should not count as new high."""
        update_high_score("classic", 500)
        result = update_high_score("classic", 500)

        self.assertFalse(result["is_new_high"])

    def test_updates_best_fish_count(self):
        """Should update best fish count independently."""
        update_high_score("classic", 500, fish_count=5)
        update_high_score("classic", 300, fish_count=10)

        scores = get_all_high_scores()
        self.assertEqual(scores["classic"]["high_score"], 500)  # Unchanged
        self.assertEqual(scores["classic"]["best_fish_count"], 10)  # Updated

    def test_updates_best_time_endless(self):
        """Should update best time for endless mode."""
        update_high_score("endless", 100, time_played=60.5)
        update_high_score("endless", 50, time_played=120.0)

        scores = get_all_high_scores()
        self.assertEqual(scores["endless"]["best_time"], 120.0)

    def test_ignores_time_for_non_endless(self):
        """Should not track time for classic or time_attack."""
        update_high_score("classic", 100, time_played=999)

        scores = get_all_high_scores()
        # best_time should not exist or be default for classic
        self.assertNotIn("best_time", scores["classic"])

    def test_sets_date_on_new_high(self):
        """Should record date when high score is set."""
        update_high_score("classic", 500)

        scores = get_all_high_scores()
        self.assertIsNotNone(scores["classic"]["date"])


class TestGetHighScore(unittest.TestCase):
    """Tests for get_high_score()."""

    def setUp(self):
        """Reset scores before each test."""
        if os.path.exists(SCORES_FILE):
            os.remove(SCORES_FILE)

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(SCORES_FILE):
            os.remove(SCORES_FILE)

    def test_returns_zero_for_new_game(self):
        """Should return 0 when no scores exist."""
        result = get_high_score("classic")
        self.assertEqual(result, 0)

    def test_returns_correct_score(self):
        """Should return the saved high score."""
        update_high_score("classic", 750)
        result = get_high_score("classic")
        self.assertEqual(result, 750)

    def test_returns_zero_for_invalid_mode(self):
        """Should return 0 for unknown game mode."""
        result = get_high_score("nonexistent_mode")
        self.assertEqual(result, 0)


class TestResetScores(unittest.TestCase):
    """Tests for reset_scores()."""

    def setUp(self):
        """Create some scores before each test."""
        update_high_score("classic", 999, fish_count=50)
        update_high_score("endless", 888, time_played=300)

    def tearDown(self):
        """Clean up after each test."""
        if os.path.exists(SCORES_FILE):
            os.remove(SCORES_FILE)

    def test_resets_all_scores_to_zero(self):
        """Should reset all high scores to zero."""
        reset_scores()

        self.assertEqual(get_high_score("classic"), 0)
        self.assertEqual(get_high_score("time_attack"), 0)
        self.assertEqual(get_high_score("endless"), 0)

    def test_resets_fish_counts(self):
        """Should reset fish counts to zero."""
        reset_scores()

        scores = get_all_high_scores()
        self.assertEqual(scores["classic"]["best_fish_count"], 0)

    def test_resets_best_time(self):
        """Should reset best time to zero."""
        reset_scores()

        scores = get_all_high_scores()
        self.assertEqual(scores["endless"]["best_time"], 0)


if __name__ == "__main__":
    unittest.main()