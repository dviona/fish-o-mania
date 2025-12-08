"""
Unit tests for FastFishManager class.
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

from fish.fast_fish_manager import FastFishManager, FISH_SPEED_MULTIPLIER
from fish.relaxed_fish_manager import RelaxedFishManager


class TestFastFishManager(unittest.TestCase):
    """Tests for FastFishManager class."""

    def test_speed_multiplier_constant_equals_three(self):
        """Test that FISH_SPEED_MULTIPLIER equals 3.0."""
        self.assertEqual(FISH_SPEED_MULTIPLIER, 3.0)

    def test_fast_fish_manager_inherits_from_relaxed_fish_manager(self):
        """Test that FastFishManager is a subclass of RelaxedFishManager."""
        self.assertTrue(issubclass(FastFishManager, RelaxedFishManager))

    def test_spawn_fish_returns_fish_object(self):
        """Test that spawn_fish returns a valid fish instance."""
        manager = FastFishManager()
        fish = manager.spawn_fish()
        self.assertIsNotNone(fish)
        self.assertTrue(hasattr(fish, 'speed_x'))
        self.assertTrue(hasattr(fish, 'speed_y'))

    def test_spawned_fish_has_multiplied_speed_x(self):
        """Test that spawned fish has speed_x multiplied by 3."""
        manager = FastFishManager()
        fish = manager.spawn_fish("shark")
        expected_speed = 0.75 * FISH_SPEED_MULTIPLIER
        self.assertEqual(abs(fish.speed_x), expected_speed)

    def test_spawn_fish_with_specific_shark_class(self):
        """Test spawning a specific fish type (Shark) with boosted speed."""
        manager = FastFishManager()
        fish = manager.spawn_fish("shark")
        self.assertEqual(fish.fish_type, "Shark")
        self.assertEqual(abs(fish.speed_x), 2.25)

    def test_spawn_fish_with_specific_turtle_class(self):
        """Test spawning a Turtle with boosted speed."""
        manager = FastFishManager()
        fish = manager.spawn_fish("turtle")
        self.assertEqual(fish.fish_type, "Turtle")
        self.assertEqual(abs(fish.speed_x), 1.5)

    def test_spawn_fish_with_specific_octopus_class(self):
        """Test spawning an Octopus with boosted speed."""
        manager = FastFishManager()
        fish = manager.spawn_fish("octopus")
        self.assertEqual(fish.fish_type, "Octopus")
        self.assertEqual(abs(fish.speed_x), 1.5)


if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()
