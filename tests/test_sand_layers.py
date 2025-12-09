"""
Unit Tests for Sand Layers Module

This module contains tests for the SandLayers class
"""

import unittest
import pygame

# Initialize pygame and set display mode for image loading
pygame.init()
pygame.display.set_mode((800, 600))

from background.sand_layers import SandLayers


class TestSandLayers(unittest.TestCase):
    """Tests for sandlayers class"""

    def test_init_without_terrain_files(self):
        """Test initialization with use_terrain_files=False"""
        sand = SandLayers(use_terrain_files=False)
        self.assertEqual(sand.base_layers, [])
        self.assertIsNone(sand.top_layer)
        self.assertEqual(sand.top_layer_width, 0)
        self.assertEqual(sand.layer_widths, [])

    def test_init_with_terrain_files(self):
        """Test initialization with terrain files loads correctly"""
        sand = SandLayers()
        self.assertEqual(len(sand.base_layers), 4)
        self.assertEqual(len(sand.layer_widths), 4)
        self.assertIsNotNone(sand.top_layer)
        self.assertGreater(sand.top_layer_width, 0)


    def test_layer_widths_match_layers(self):
        """Test that cached widths match actual layer widths"""
        sand = SandLayers()
        for i, layer in enumerate(sand.base_layers):
            self.assertEqual(sand.layer_widths[i], layer.get_width())

    def test_init_with_custom_directory(self):
        """Test initialization with our directory path"""
        sand = SandLayers(directory="graphics")
        self.assertEqual(len(sand.base_layers), 4)
        self.assertIsNotNone(sand.top_layer)

if __name__ == '__main__':
    unittest.main()
