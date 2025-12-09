"""
Unit tests for Classic Mode.

Tests helper functions and basic game setup for the classic game mode.
Run with: python -m pytest test_mode_classic.py
or: python test_mode_classic.py
"""

import unittest
import os
import sys

# Add parent directory to path so we can import game modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set SDL to dummy mode BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
from modes import mode_classic


class TestModeClassic(unittest.TestCase):
    """Test cases for Classic Mode helper functions."""

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

    def test_release_messages_exist(self):
        """Test that release messages are defined."""
        self.assertIsNotNone(mode_classic.RELEASE_MESSAGES)
        self.assertGreater(len(mode_classic.RELEASE_MESSAGES), 0)
        self.assertIsInstance(mode_classic.RELEASE_MESSAGES[0], str)

    def test_constants_defined(self):
        """Test that important constants are defined."""
        # Check that screen dimensions are positive
        self.assertGreater(mode_classic.SCREEN_WIDTH, 0)
        self.assertGreater(mode_classic.SCREEN_HEIGHT, 0)
        
        # Check FPS is reasonable
        self.assertGreater(mode_classic.FPS, 0)
        self.assertLessEqual(mode_classic.FPS, 120)

    def test_fonts_initialized(self):
        """Test that fonts are properly initialized."""
        self.assertIsNotNone(mode_classic.font)
        self.assertIsNotNone(mode_classic.big_font)

    def test_scream_constants(self):
        """Test that scream-related constants are defined in main function."""
        # These are defined inside main(), so we check they exist as concepts
        # We can't directly test them, but we verify the function exists
        self.assertTrue(callable(mode_classic.main))

    def test_release_messages_not_empty(self):
        """Test that release messages contain actual text."""
        for message in mode_classic.RELEASE_MESSAGES:
            self.assertGreater(len(message), 0)
            self.assertNotEqual(message.strip(), "")

    def test_release_messages_are_strings(self):
        """Test that all release messages are string type."""
        for message in mode_classic.RELEASE_MESSAGES:
            self.assertIsInstance(message, str)

    def test_colors_are_tuples(self):
        """Test that color constants are properly defined as tuples."""
        # Test a few color constants from mode_classic
        self.assertIsInstance(mode_classic.WHITE, tuple)
        self.assertEqual(len(mode_classic.WHITE), 3)
        self.assertIsInstance(mode_classic.SKY_BLUE, tuple)
        self.assertEqual(len(mode_classic.SKY_BLUE), 3)

    def test_water_surface_constant(self):
        """Test that water surface constant is defined and reasonable."""
        self.assertIsInstance(mode_classic.WATER_SURFACE, int)
        self.assertGreater(mode_classic.WATER_SURFACE, 0)
        self.assertLess(mode_classic.WATER_SURFACE, mode_classic.SCREEN_HEIGHT)

    def test_boat_speed_constant(self):
        """Test that boat speed constant is defined."""
        self.assertIsInstance(mode_classic.BOAT_SPEED, (int, float))
        self.assertGreater(mode_classic.BOAT_SPEED, 0)

    def test_rod_constants(self):
        """Test that rod-related constants are defined."""
        self.assertIsInstance(mode_classic.ROD_MAX_LENGTH, int)
        self.assertGreater(mode_classic.ROD_MAX_LENGTH, 0)
        self.assertIsInstance(mode_classic.ROD_SPEED, int)
        self.assertGreater(mode_classic.ROD_SPEED, 0)

    def test_start_fishes_constant(self):
        """Test that start fishes constant is defined."""
        self.assertIsInstance(mode_classic.START_FISHES, int)
        self.assertGreater(mode_classic.START_FISHES, 0)

    def test_azure_color(self):
        """Test that AZURE color is defined."""
        self.assertIsInstance(mode_classic.AZURE, tuple)
        self.assertEqual(len(mode_classic.AZURE), 3)

    def test_deep_blue_color(self):
        """Test that DEEP_BLUE color is defined."""
        self.assertIsInstance(mode_classic.DEEP_BLUE, tuple)
        self.assertEqual(len(mode_classic.DEEP_BLUE), 3)

    def test_screen_resolution(self):
        """Test that screen resolution tuple is defined."""
        self.assertIsInstance(mode_classic.SCREEN_RESOLUTION, tuple)
        self.assertEqual(len(mode_classic.SCREEN_RESOLUTION), 2)
        self.assertEqual(mode_classic.SCREEN_RESOLUTION[0], mode_classic.SCREEN_WIDTH)
        self.assertEqual(mode_classic.SCREEN_RESOLUTION[1], mode_classic.SCREEN_HEIGHT)

    def test_load_sounds_function_exists(self):
        """Test that load_sounds function exists and is callable."""
        self.assertTrue(callable(mode_classic.load_sounds))

    def test_load_graphics_function_exists(self):
        """Test that load_graphics function exists and is callable."""
        self.assertTrue(callable(mode_classic.load_graphics))

    def test_draw_water_background_function_exists(self):
        """Test that draw_water_background function exists and is callable."""
        self.assertTrue(callable(mode_classic.draw_water_background))

    def test_draw_pause_overlay_function_exists(self):
        """Test that draw_pause_overlay function exists and is callable."""
        self.assertTrue(callable(mode_classic.draw_pause_overlay))

    def test_draw_release_message_function_exists(self):
        """Test that draw_release_message function exists and is callable."""
        self.assertTrue(callable(mode_classic.draw_release_message))

    def test_draw_game_over_screen_function_exists(self):
        """Test that draw_game_over_screen function exists and is callable."""
        self.assertTrue(callable(mode_classic.draw_game_over_screen))


# Run tests if this file is executed directly
if __name__ == '__main__':
    unittest.main()
