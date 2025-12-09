"""
Unit tests for FishManager class.

Tests fish spawning, management, and game state tracking.
Run with: python -m unittest Zach_testing.test_fish_manager -v
or: python test_fish_manager.py
"""

import unittest
import os
import sys

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set SDL to dummy mode BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
from fish.fish_manager import FishManager


class TestFishManager(unittest.TestCase):
    """Test cases for FishManager class."""

    @classmethod
    def setUpClass(cls):
        """Set up pygame before all tests."""
        try:
            pygame.init()
            pygame.display.set_mode((800, 600))
        except Exception as e:
            print(f"Warning: Could not initialize pygame: {e}")

    @classmethod
    def tearDownClass(cls):
        """Clean up pygame after all tests."""
        try:
            pygame.quit()
        except:
            pass

    def setUp(self):
        """Create a fresh FishManager for each test."""
        self.manager = FishManager()

    def tearDown(self):
        """Clean up after each test."""
        self.manager.clear_all()

    def test_manager_creation(self):
        """Test that FishManager is created with correct initial state."""
        self.assertIsNotNone(self.manager.all_fish)
        self.assertIsNotNone(self.manager.danger_fish)
        self.assertIsNotNone(self.manager.rare_fish)
        self.assertIsNotNone(self.manager.large_fish)
        self.assertEqual(len(self.manager.all_fish), 0)
        self.assertEqual(len(self.manager.recent_catches), 0)

    def test_spawn_turtle(self):
        """Test spawning a turtle fish."""
        fish = self.manager.spawn_fish(fish_class="turtle")
        
        self.assertIsNotNone(fish)
        self.assertEqual(len(self.manager.all_fish), 1)
        self.assertEqual(len(self.manager.rare_fish), 1)

    def test_spawn_danger_fish(self):
        """Test spawning a danger fish."""
        fish = self.manager.spawn_fish(fish_class="danger")
        
        self.assertIsNotNone(fish)
        self.assertEqual(len(self.manager.all_fish), 1)
        self.assertEqual(len(self.manager.danger_fish), 1)

    def test_spawn_shark(self):
        """Test spawning a shark."""
        fish = self.manager.spawn_fish(fish_class="shark")
        
        self.assertIsNotNone(fish)
        self.assertEqual(len(self.manager.all_fish), 1)
        self.assertEqual(len(self.manager.danger_fish), 1)

    def test_spawn_octopus(self):
        """Test spawning an octopus."""
        fish = self.manager.spawn_fish(fish_class="octopus")
        
        self.assertIsNotNone(fish)
        self.assertEqual(len(self.manager.all_fish), 1)
        self.assertEqual(len(self.manager.large_fish), 1)

    def test_spawn_multiple_fish(self):
        """Test spawning multiple fish."""
        self.manager.spawn_fish(fish_class="turtle")
        self.manager.spawn_fish(fish_class="danger")
        self.manager.spawn_fish(fish_class="octopus")
        
        self.assertEqual(len(self.manager.all_fish), 3)

    def test_spawn_random_fish(self):
        """Test spawning a random fish (no class specified)."""
        fish = self.manager.spawn_fish()
        
        self.assertIsNotNone(fish)
        self.assertEqual(len(self.manager.all_fish), 1)

    def test_get_stats(self):
        """Test getting game statistics."""
        self.manager.spawn_fish(fish_class="turtle")
        self.manager.spawn_fish(fish_class="danger")
        
        stats = self.manager.get_stats()
        
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["danger"], 1)
        self.assertEqual(stats["rare"], 1)
        self.assertIn("lives", stats)
        self.assertIn("game_over", stats)

    def test_clear_all(self):
        """Test clearing all fish."""
        self.manager.spawn_fish(fish_class="turtle")
        self.manager.spawn_fish(fish_class="danger")
        self.manager.spawn_fish(fish_class="octopus")
        
        self.assertEqual(len(self.manager.all_fish), 3)
        
        self.manager.clear_all()
        
        self.assertEqual(len(self.manager.all_fish), 0)
        self.assertEqual(len(self.manager.danger_fish), 0)
        self.assertEqual(len(self.manager.rare_fish), 0)
        self.assertEqual(len(self.manager.large_fish), 0)
        self.assertEqual(len(self.manager.recent_catches), 0)

    def test_lives_manager_initialized(self):
        """Test that lives manager is properly initialized."""
        self.assertIsNotNone(self.manager.lives_manager)
        self.assertEqual(self.manager.lives_manager.max_lives, 3)
        self.assertEqual(self.manager.lives_manager.get_current_lives(), 3)

    def test_red_flash_timer(self):
        """Test red flash timer initialization."""
        self.assertEqual(self.manager.red_flash_timer, 0)
        self.assertGreater(self.manager.red_flash_duration, 0)

    def test_recent_catches_limit(self):
        """Test that recent catches are limited to max."""
        self.assertEqual(self.manager.max_recent_catches, 3)

    def test_spawn_timer(self):
        """Test spawn timer initialization."""
        self.assertEqual(self.manager.spawn_timer, 0)
        self.assertGreater(self.manager.spawn_delay, 0)

    def test_fish_animations_loaded(self):
        """Test that fish animations are loaded."""
        self.assertIsNotNone(self.manager.fish_animations)
        self.assertIsInstance(self.manager.fish_animations, dict)

    def test_get_fish_at_position_empty(self):
        """Test getting fish at position when no fish exist."""
        fish = self.manager.get_fish_at_position((400, 300))
        self.assertIsNone(fish)

    def test_get_fish_at_position_with_fish(self):
        """Test getting fish at a specific position."""
        spawned_fish = self.manager.spawn_fish(fish_class="turtle")
        
        # Get fish at its position
        fish = self.manager.get_fish_at_position(spawned_fish.rect.center)
        
        self.assertIsNotNone(fish)
        self.assertEqual(fish, spawned_fish)

    def test_remove_fish(self):
        """Test removing a caught fish."""
        fish = self.manager.spawn_fish(fish_class="turtle")
        
        self.assertEqual(len(self.manager.all_fish), 1)
        
        result = self.manager.remove_fish(fish)
        
        self.assertEqual(len(self.manager.all_fish), 0)
        self.assertIsInstance(result, dict)
        self.assertIn("type", result)
        self.assertIn("value", result)
        self.assertIn("penalty", result)
        self.assertFalse(result["penalty"])

    def test_recent_catches_added(self):
        """Test that recent catches are tracked."""
        fish = self.manager.spawn_fish(fish_class="turtle")
        
        self.assertEqual(len(self.manager.recent_catches), 0)
        
        self.manager.remove_fish(fish)
        
        self.assertEqual(len(self.manager.recent_catches), 1)
        catch = self.manager.recent_catches[0]
        self.assertIn("type", catch)
        self.assertIn("value", catch)
        self.assertIn("current_frame", catch)

    def test_recent_catches_max_limit(self):
        """Test that recent catches don't exceed max limit."""
        # Spawn and catch 5 fish
        for i in range(5):
            fish = self.manager.spawn_fish(fish_class="turtle")
            self.manager.remove_fish(fish)
        
        # Should only keep last 3
        self.assertEqual(len(self.manager.recent_catches), 3)


# Run tests if this file is executed directly
if __name__ == '__main__':
    unittest.main()
