"""
Unit Tests for Background Module.

This module contains tests for all background visual elements:
- Ripple Class
"""

import unittest
import pygame

# Initialize pygame for tests
pygame.init()

# Import background classes
from background.ripple import Ripple
from mechanics.constants import SCREEN_WIDTH, SCREEN_HEIGHT


# RIPPLE CLASS TESTS

class TestRipple(unittest.TestCase):
    """Tests for the Ripple class."""

    def test_initialization(self):
        """Test that ripple initializes with correct values."""
        ripple = Ripple(100, 200)
        self.assertEqual(ripple.x, 100)
        self.assertEqual(ripple.y, 200)
        self.assertEqual(ripple.radius, 0)
        self.assertEqual(ripple.alpha, 255)
        self.assertTrue(ripple.alive)

    def test_initialization_random_max_radius(self):
        """Test that ripple has randomized max_radius in valid range."""
        for i in range(10):
            ripple = Ripple(0, 0)
            self.assertGreaterEqual(ripple.max_radius, 30)
            self.assertLessEqual(ripple.max_radius, 80)

    def test_initialization_random_growth_rate(self):
        """Test that ripple has randomized growth_rate in valid range."""
        for i in range(10):
            ripple = Ripple(0, 0)
            self.assertGreaterEqual(ripple.growth_rate, 0.5)
            self.assertLessEqual(ripple.growth_rate, 1.0)

    def test_update_increases_radius(self):
        """Test that update increases the ripple radius."""
        ripple = Ripple(100, 200)
        initial_radius = ripple.radius
        ripple.update()
        self.assertGreater(ripple.radius, initial_radius)

    def test_update_decreases_alpha(self):
        """Test that update decreases the ripple alpha."""
        ripple = Ripple(100, 200)
        initial_alpha = ripple.alpha
        ripple.update()
        self.assertLess(ripple.alpha, initial_alpha)

    def test_ripple_dies_when_alpha_zero(self):
        """Test that ripple becomes not alive when alpha reaches zero."""
        ripple = Ripple(100, 200)
        ripple.alpha = ripple.fade_rate
        ripple.update()
        self.assertFalse(ripple.alive)

    def test_ripple_dies_when_max_radius_reached(self):
        """Test that ripple becomes not alive when max radius reached."""
        ripple = Ripple(100, 200)
        ripple.radius = ripple.max_radius - ripple.growth_rate
        ripple.update()
        self.assertFalse(ripple.alive)
