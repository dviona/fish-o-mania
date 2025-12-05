"""
Unit Tests for Background Module

This module contains tests for all background visual elements:
Bubble
"""

import unittest
import pygame

# Initialize pygame for tests
pygame.init()

# Import background classes
from background.bubble import Bubble
from mechanics.constants import SCREEN_WIDTH, SCREEN_HEIGHT, WATER_SURFACE, WATER_BOTTOM


# Bubble TESTS

class TestBubble(unittest.TestCase):
    """Tests for the Bubble class"""

    def test_initialization(self):
        """Test that bubble initializes with correct values"""
        bubble = Bubble(100, 400)
        self.assertEqual(bubble.x, 100)
        self.assertEqual(bubble.y, 400)
        self.assertTrue(bubble.alive)
        self.assertEqual(bubble.time, 0)

    def test_initialization_random_radius(self):
        """Test that bubble has randomized radius in valid range"""
        for _ in range(10):
            bubble = Bubble(0, 0)
            self.assertGreaterEqual(bubble.radius, 3)
            self.assertLessEqual(bubble.radius, 8)

    def test_initialization_random_speed(self):
        """Test that bubble has randomized speed in valid range"""
        for _ in range(10):
            bubble = Bubble(0, 0)
            self.assertGreaterEqual(bubble.speed, 0.5)
            self.assertLessEqual(bubble.speed, 1.5)

    def test_update_moves_bubble_up(self):
        """Test that update moves the bubble upward"""
        bubble = Bubble(100, 400)
        initial_y = bubble.y
        bubble.update()
        self.assertLess(bubble.y, initial_y)

    def test_update_wobbles_horizontally(self):
        """Test that update causes horizontal wobble"""
        bubble = Bubble(100, 400)
        x_positions = [bubble.x]

        for _ in range(20):
            bubble.update()
            x_positions.append(bubble.x)

        unique_positions = set(x_positions)
        self.assertGreater(len(unique_positions), 1)

    def test_update_increments_time(self):
        """Test that update increments the time counter"""
        bubble = Bubble(100, 400)
        initial_time = bubble.time
        bubble.update()
        self.assertGreater(bubble.time, initial_time)

    def test_bubble_dies_at_water_surface(self):
        """Test bubble becomes not alive at water surface"""
        bubble = Bubble(100, WATER_SURFACE)
        bubble.update()
        self.assertFalse(bubble.alive)

