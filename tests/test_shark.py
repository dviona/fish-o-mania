"""
Debbie Tavish Zac and Aradhya

Unit tests for Shark class
"""

import unittest
import pygame
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Initialize pygame once at module level
pygame.init()
pygame.mixer.init()
pygame.display.set_mode((800, 600), pygame.HIDDEN)

from fish.shark import Shark


class TestShark(unittest.TestCase):
    """Tests for Shark class."""

    def test_shark_value_is_75(self):
        """Test that Shark has a point value of 75."""
        shark = Shark(100, 200)
        self.assertEqual(shark.value, 75)

    def test_shark_rarity_is_uncommon(self):
        """Test that Shark has uncommon rarity."""
        shark = Shark(100, 200)
        self.assertEqual(shark.rarity, "uncommon")

    def test_shark_fish_type_is_shark(self):
        """Test that fish_type is set to 'Shark'."""
        shark = Shark(100, 200)
        self.assertEqual(shark.fish_type, "Shark")

    def test_shark_speed_when_moving_right(self):
        """Test that Shark speed is 0.75 when moving right."""
        shark = Shark(100, 200, moving_right=True)
        self.assertEqual(shark.speed_x, 0.75)

    def test_shark_speed_when_moving_left(self):
        """Test that Shark speed is -0.75 when moving left."""
        shark = Shark(100, 200, moving_right=False)
        self.assertEqual(shark.speed_x, -0.75)

    def test_shark_default_direction_is_right(self):
        """Test that Shark defaults to moving right when direction not specified."""
        shark = Shark(100, 200)
        self.assertEqual(shark.speed_x, 0.75)


if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()
