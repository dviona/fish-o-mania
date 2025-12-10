"""
Debbie Tavish Zac and Aradhya

Unit tests for LivesManager class
"""

import unittest
import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize pygame once at module level
pygame.init()
pygame.mixer.init()
pygame.display.set_mode((800, 600), pygame.HIDDEN)

from mechanics.lives_manager import LivesManager


class TestLivesManager(unittest.TestCase):
    """Tests for LivesManager class."""

    def test_default_max_lives_is_3(self):
        """Test that default max_lives is 3."""
        manager = LivesManager()
        self.assertEqual(manager.max_lives, 3)

    def test_current_lives_starts_at_max_lives(self):
        """Test that current_lives starts equal to max_lives."""
        manager = LivesManager()
        self.assertEqual(manager.current_lives, manager.max_lives)

    def test_game_over_starts_as_false(self):
        """Test that game_over is False on initialization."""
        manager = LivesManager()
        self.assertFalse(manager.game_over)

    def test_lose_life_decrements_current_lives(self):
        """Test that lose_life decreases current_lives by 1."""
        manager = LivesManager()
        manager.lose_life()
        self.assertEqual(manager.current_lives, 2)

    def test_lose_life_returns_true_while_lives_remain(self):
        """Test that lose_life returns True when lives still remain."""
        manager = LivesManager()
        result = manager.lose_life()
        self.assertTrue(result)

    def test_lose_life_returns_false_when_last_life_lost(self):
        """Test that lose_life returns False when last life is lost."""
        manager = LivesManager(max_lives=1)
        result = manager.lose_life()
        self.assertFalse(result)

    def test_lose_life_sets_game_over_when_lives_reach_zero(self):
        """Test that game_over becomes True when lives reach zero."""
        manager = LivesManager(max_lives=2)
        manager.lose_life()
        self.assertFalse(manager.game_over)
        manager.lose_life()
        self.assertTrue(manager.game_over)

    def test_reset_restores_current_lives_to_max(self):
        """Test that reset restores current_lives to max_lives."""
        manager = LivesManager()
        manager.lose_life()
        manager.lose_life()
        manager.reset()
        self.assertEqual(manager.current_lives, manager.max_lives)

    def test_reset_clears_game_over_flag(self):
        """Test that reset sets game_over back to False."""
        manager = LivesManager(max_lives=1)
        manager.lose_life()
        self.assertTrue(manager.game_over)
        manager.reset()
        self.assertFalse(manager.game_over)

    def test_is_game_over_returns_correct_state(self):
        """Test that is_game_over returns the game_over flag value."""
        manager = LivesManager()
        self.assertFalse(manager.is_game_over())
        manager.game_over = True
        self.assertTrue(manager.is_game_over())

    def test_get_current_lives_returns_correct_value(self):
        """Test that get_current_lives returns current_lives."""
        manager = LivesManager()
        self.assertEqual(manager.get_current_lives(), 3)
        manager.lose_life()
        self.assertEqual(manager.get_current_lives(), 2)

    def test_custom_max_lives_initialization(self):
        """Test that custom max_lives value is set correctly."""
        manager = LivesManager(max_lives=5)
        self.assertEqual(manager.max_lives, 5)
        self.assertEqual(manager.current_lives, 5)


if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()
