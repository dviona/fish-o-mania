"""
Unit Tests for Background Module.

This module contains tests for all background visual elements:
- Sand Layers Class

"""

import unittest
import pygame

# Initialize pygame for tests
pygame.init()

# Import background classes
from background.sand_layers import SandLayers
from mechanics.constants import SCREEN_WIDTH, SCREEN_HEIGHT


# SAND LAYERS CLASS TESTS
class TestSandLayers(unittest.TestCase):
    """Tests for the SandLayers class."""

    def test_initialization_without_terrain(self):
        """Test that sand layers initializes without terrain files."""
        sand = SandLayers(use_terrain_files=False)
        self.assertEqual(sand.base_layers, [])
        self.assertIsNone(sand.top_layer)

    def test_draw_does_not_crash_without_layers(self):
        """Test that draw works even without loaded layers."""
        sand = SandLayers(use_terrain_files=False)
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        sand.draw(surface)
