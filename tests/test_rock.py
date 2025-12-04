"""
Unit Tests for Background Module.

This module contains tests for all background visual elements:
- Rock Class

"""

import unittest
import pygame

# Initialize pygame for tests
pygame.init()

# Import background classes
from background.rock import Rock
from mechanics.constants import SCREEN_WIDTH, SCREEN_HEIGHT


# ROCK CLASS TESTS

class TestRock(unittest.TestCase):
    """Tests for the Rock class."""

    def test_initialization(self):
        """Test that rock initializes with correct position."""
        rock = Rock(100, 500)
        self.assertEqual(rock.x, 100)
        self.assertEqual(rock.y, 500)

    def test_initialization_random_width(self):
        """Test that rock has randomized width in valid range."""
        for i in range(10):
            rock = Rock(0, 0)
            self.assertGreaterEqual(rock.width, 30)
            self.assertLessEqual(rock.width, 80)

    def test_initialization_random_height(self):
        """Test that rock has randomized height in valid range."""
        for i in range(10):
            rock = Rock(0, 0)
            self.assertGreaterEqual(rock.height, 20)
            self.assertLessEqual(rock.height, 50)

    def test_initialization_color_variants(self):
        """Test that rock color is one of the valid variants."""
        valid_colors = [
            (105, 105, 105),
            (119, 136, 153),
            (112, 128, 144),
        ]

        for i in range(20):
            rock = Rock(0, 0)
            self.assertIn(rock.color, valid_colors)

    def test_highlight_color_is_lighter(self):
        """Test that highlight color is lighter than base color."""
        rock = Rock(100, 500)
        for i in range(3):
            self.assertGreaterEqual(rock.highlight_color[i], rock.color[i])

    def test_shadow_color_is_darker(self):
        """Test that shadow color is darker than base color."""
        rock = Rock(100, 500)
        for i in range(3):
            self.assertLessEqual(rock.shadow_color[i], rock.color[i])
