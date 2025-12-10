"""
Debbie Tavish Zac
Unit Tests for Background Module

This module contains tests for all background visual elements:
- BackgroundManager
"""

import unittest
import pygame

# Initialize pygame for tests
pygame.init()

# Import background classes
from background.ripple import Ripple
from background.bubble import Bubble
from background.rock import Rock
from background.seaweed import Seaweed
from background.wave import Wave
from background.sand_layers import SandLayers
from background.background_manager import BackgroundManager
from mechanics.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WATER_BOTTOM


# BACKGROUND MANAGER TESTS

class TestBackgroundManager(unittest.TestCase):
    """Tests for the BackgroundManager class"""

    def test_initialization(self):
        """Test that background manager initializes all components"""
        manager = BackgroundManager(use_terrain_files=False)
        self.assertIsInstance(manager.ripples, list)
        self.assertIsInstance(manager.seaweeds, list)
        self.assertIsInstance(manager.rocks, list)
        self.assertIsInstance(manager.bubbles, list)
        self.assertIsInstance(manager.wave, Wave)
        self.assertIsInstance(manager.sand, SandLayers)

    def test_generates_seaweed_min(self):
        """Test that at least 8 seaweed are generated"""
        manager = BackgroundManager(use_terrain_files=False)
        self.assertGreaterEqual(len(manager.seaweeds), 8)

    def test_generates_seaweed_max(self):
        """Test that at most 12 seaweed are generated"""
        manager = BackgroundManager(use_terrain_files=False)
        self.assertLessEqual(len(manager.seaweeds), 12)

    def test_generates_rocks_min(self):
        """Test that at least 5 rocks are generated"""
        manager = BackgroundManager(use_terrain_files=False)
        self.assertGreaterEqual(len(manager.rocks), 5)

    def test_generates_rocks_max(self):
        """Test that at most 10 rocks are generated"""
        manager = BackgroundManager(use_terrain_files=False)
        self.assertLessEqual(len(manager.rocks), 10)

    def test_seaweed_are_seaweed_instances(self):
        """Test that generated seaweed are Seaweed instances"""
        manager = BackgroundManager(use_terrain_files=False)
        for seaweed in manager.seaweeds:
            self.assertIsInstance(seaweed, Seaweed)

    def test_rocks_are_rock_instances(self):
        """Test that generated rocks are Rock instances"""
        manager = BackgroundManager(use_terrain_files=False)
        for rock in manager.rocks:
            self.assertIsInstance(rock, Rock)

    def test_add_ripple(self):
        """Test that add_ripple adds a ripple to the list"""
        manager = BackgroundManager(use_terrain_files=False)
        initial_count = len(manager.ripples)
        manager.add_ripple(100, 200)
        self.assertEqual(len(manager.ripples), initial_count + 1)

    def test_add_ripple_creates_ripple_instance(self):
        """Test that add_ripple creates a Ripple instance"""
        manager = BackgroundManager(use_terrain_files=False)
        manager.add_ripple(100, 200)
        self.assertIsInstance(manager.ripples[-1], Ripple)

    def test_add_ripple_correct_position(self):
        """Test that add_ripple creates ripple at correct position"""
        manager = BackgroundManager(use_terrain_files=False)
        manager.add_ripple(150, 250)
        ripple = manager.ripples[-1]
        self.assertEqual(ripple.x, 150)
        self.assertEqual(ripple.y, 250)


    def test_update_removes_dead_ripples(self):
        """Test that update removes dead ripples"""
        manager = BackgroundManager(use_terrain_files=False)
        manager.add_ripple(100, 200)
        manager.ripples[0].alive = False
        manager.update()

        dead_ripples = [r for r in manager.ripples if not r.alive]
        self.assertEqual(len(dead_ripples), 0)

    def test_update_removes_dead_bubbles(self):
        """Test that update removes dead bubbles"""
        manager = BackgroundManager(use_terrain_files=False)
        manager.bubbles.append(Bubble(100, 200))
        manager.bubbles[0].alive = False
        manager.update()

        dead_bubbles = [b for b in manager.bubbles if not b.alive]
        self.assertEqual(len(dead_bubbles), 0)

    def test_update_spawns_ripples_over_time(self):
        """Test that update eventually spawns random ripples"""
        manager = BackgroundManager(use_terrain_files=False)
        initial_count = len(manager.ripples)

        for i in range(200):
            manager.update()

        self.assertGreaterEqual(len(manager.ripples), initial_count)

    def test_update_spawns_bubbles_over_time(self):
        """Test that update eventually spawns random bubbles"""
        manager = BackgroundManager(use_terrain_files=False)
        initial_count = len(manager.bubbles)

        for _ in range(200):
            manager.update()

        self.assertGreater(len(manager.bubbles), initial_count)


    def test_timers_initialized(self):
        """Test that spawn timers are initialized"""
        manager = BackgroundManager(use_terrain_files=False)
        self.assertEqual(manager.ripple_timer, 0)
        self.assertEqual(manager.bubble_timer, 0)

    def test_rock_positions_x_within_bounds(self):
        """Test that rocks x positions are within screen bounds"""
        manager = BackgroundManager(use_terrain_files=False)
        for rock in manager.rocks:
            self.assertGreaterEqual(rock.x, 0)
            self.assertLessEqual(rock.x, SCREEN_WIDTH - 80)

    def test_rock_positions_y_within_bounds(self):
        """Test that rocks y positions are within water bounds"""
        manager = BackgroundManager(use_terrain_files=False)
        for rock in manager.rocks:
            self.assertGreaterEqual(rock.y, WATER_BOTTOM - 40)
            self.assertLessEqual(rock.y, WATER_BOTTOM)

    def test_seaweed_positions_within_bounds(self):
        """Test that seaweed x positions are within screen bounds"""
        manager = BackgroundManager(use_terrain_files=False)
        for seaweed in manager.seaweeds:
            self.assertGreaterEqual(seaweed.x, 0)
            self.assertLessEqual(seaweed.x, SCREEN_WIDTH)



if __name__ == '__main__':
    unittest.main()
