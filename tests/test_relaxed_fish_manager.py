"""
Unit tests for RelaxedFishManager class
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

from fish.relaxed_fish_manager import RelaxedFishManager
from fish.fish_manager import FishManager


class TestRelaxedFishManager(unittest.TestCase):
    """Tests for RelaxedFishManager class."""

    def test_relaxed_fish_manager_inherits_from_fish_manager(self):
        """Test that RelaxedFishManager is a subclass of FishManager."""
        self.assertTrue(issubclass(RelaxedFishManager, FishManager))

    def test_remove_fish_returns_penalty_as_false(self):
        """Test that remove_fish never returns penalty=True."""
        manager = RelaxedFishManager()
        fish = manager.spawn_fish("danger")
        result = manager.remove_fish(fish)
        self.assertFalse(result["penalty"])

    def test_remove_fish_returns_game_over_as_false(self):
        """Test that remove_fish never returns game_over=True."""
        manager = RelaxedFishManager()
        fish = manager.spawn_fish("danger")
        result = manager.remove_fish(fish)
        self.assertFalse(result["game_over"])

    def test_remove_fish_plays_catch_sound(self):
        """Test that catch sound plays when fish is removed."""
        manager = RelaxedFishManager()
        fish = manager.spawn_fish("shark")
        # Sound will play - we verify no exception is raised
        result = manager.remove_fish(fish)
        self.assertIsNotNone(result)

    def test_remove_fish_marks_fish_as_caught(self):
        """Test that remove_fish sets is_caught and caught to True."""
        manager = RelaxedFishManager()
        fish = manager.spawn_fish("turtle")
        manager.remove_fish(fish)
        self.assertTrue(fish.is_caught)
        self.assertTrue(fish.caught)

    def test_remove_fish_adds_to_recent_catches(self):
        """Test that caught fish is added to recent_catches list."""
        manager = RelaxedFishManager()
        manager.recent_catches = []
        fish = manager.spawn_fish("octopus")
        manager.remove_fish(fish)
        self.assertEqual(len(manager.recent_catches), 1)
        self.assertEqual(manager.recent_catches[0]["type"], "Octopus")

    def test_remove_fish_creates_death_animation(self):
        """Test that death animation is added to death_animations group."""
        manager = RelaxedFishManager()
        initial_count = len(manager.death_animations)
        fish = manager.spawn_fish("shark")
        manager.remove_fish(fish)
        self.assertGreater(len(manager.death_animations), initial_count)

    def test_remove_fish_already_processed_returns_value_zero(self):
        """Test that already processed fish returns value=0."""
        manager = RelaxedFishManager()
        fish = manager.spawn_fish("turtle")
        fish.death_animation_created = True
        result = manager.remove_fish(fish)
        self.assertEqual(result["value"], 0)


if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()
