"""
Debbie Tavish Zac and Aradhya

Unit Tests for Background Module.

This module contains tests for all background visual elements:
- WAVE Class

"""

import unittest
import pygame

# Initialize pygame for tests
pygame.init()

# Import background classes
from background.wave import Wave
from mechanics.constants import SCREEN_WIDTH, WATER_SURFACE


# WAVE CLASS TESTS
class TestWave(unittest.TestCase):
    """Tests for the Wave class."""

    def test_initialization(self):
        """Test that wave initializes with correct values."""
        wave = Wave()
        self.assertEqual(wave.time, 0)
        self.assertEqual(wave.wave_speed, 0.05)
        self.assertEqual(wave.y_position, WATER_SURFACE)
        self.assertEqual(len(wave.layers), 3)

    def test_layer_properties(self):
        """Test that each wave layer has required properties."""
        wave = Wave()
        required_keys = ['speed', 'amplitude', 'frequency', 'offset']

        for layer in wave.layers:
            for key in required_keys:
                self.assertIn(key, layer)

    def test_update_increments_time(self):
        """Test that update increments the time counter."""
        wave = Wave()
        initial_time = wave.time
        wave.update()
        self.assertGreater(wave.time, initial_time)

    def test_get_wave_points_returns_list(self):
        """Test that get_wave_points returns a list of points."""
        wave = Wave()
        points = wave.get_wave_points(0)
        self.assertIsInstance(points, list)
        self.assertGreater(len(points), 0)

    def test_get_wave_points_format(self):
        """Test that wave points are (x, y) tuples."""
        wave = Wave()
        points = wave.get_wave_points(0)

        for point in points:
            self.assertIsInstance(point, tuple)
            self.assertEqual(len(point), 2)

    def test_get_wave_points_spans_screen_width(self):
        """Test that wave points span the entire screen width."""
        wave = Wave()
        points = wave.get_wave_points(0)
        x_coords = [p[0] for p in points]
        self.assertEqual(min(x_coords), 0)
        self.assertGreaterEqual(max(x_coords), SCREEN_WIDTH)

    def test_get_wave_points_different_layers(self):
        """Test that different layers produce different points."""
        wave = Wave()
        points_0 = wave.get_wave_points(0)
        points_1 = wave.get_wave_points(1)

        y_values_0 = [p[1] for p in points_0]
        y_values_1 = [p[1] for p in points_1]

        self.assertNotEqual(y_values_0, y_values_1)
