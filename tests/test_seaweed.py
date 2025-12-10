# Tavish, Debbie, Zac, Aradhya
"""
Unit Tests for Background Module.

This module contains tests for all background visual elements:
- SeaWeed Class

"""

import unittest
import pygame

# Initialize pygame for tests
pygame.init()

# Import background classes
from background.seaweed import Seaweed
from mechanics.constants import SCREEN_HEIGHT


# SEAWEED CLASS TESTS

class TestSeaweed(unittest.TestCase):
    """Tests for the Seaweed class."""

    def test_initialization(self):
        """Test that seaweed initializes with correct values."""
        seaweed = Seaweed(100)
        self.assertEqual(seaweed.x, 100)
        self.assertEqual(seaweed.base_y, SCREEN_HEIGHT - 2)
        self.assertEqual(seaweed.segments, 8)
        self.assertEqual(seaweed.time, 0)

    def test_initialization_random_height(self):
        """Test that seaweed has randomized height in valid range."""
        for i in range(10):
            seaweed = Seaweed(0)
            self.assertGreaterEqual(seaweed.height, 80)
            self.assertLessEqual(seaweed.height, 150)

    def test_initialization_random_sway_amount(self):
        """Test that seaweed has randomized sway_amount in valid range."""
        for i in range(10):
            seaweed = Seaweed(0)
            self.assertGreaterEqual(seaweed.sway_amount, 10)
            self.assertLessEqual(seaweed.sway_amount, 20)

    def test_update_increments_time(self):
        """Test that update increments the time counter."""
        seaweed = Seaweed(100)
        initial_time = seaweed.time
        seaweed.update()
        self.assertGreater(seaweed.time, initial_time)

    def test_color_is_forest_green(self):
        """Test that seaweed color is forest green."""
        seaweed = Seaweed(100)
        self.assertEqual(seaweed.color, (34, 139, 34))
