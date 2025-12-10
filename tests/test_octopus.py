"""
Debbie Tavish Zac and Aradhya

Unit tests for Octopus class
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

from fish.octopus import Octopus


class TestOctopus(unittest.TestCase):
    """Tests for Octopus class."""

    def test_octopus_value_is_100(self):
        """Test that Octopus has a point value of 100."""
        octopus = Octopus(100, 200)
        self.assertEqual(octopus.value, 100)

    def test_octopus_rarity_is_uncommon(self):
        """Test that Octopus has uncommon rarity."""
        octopus = Octopus(100, 200)
        self.assertEqual(octopus.rarity, "uncommon")

    def test_octopus_fish_type_is_octopus(self):
        """Test that fish_type is set to 'Octopus'."""
        octopus = Octopus(100, 200)
        self.assertEqual(octopus.fish_type, "Octopus")

    def test_octopus_speed_when_moving_right(self):
        """Test that Octopus speed is 0.5 when moving right."""
        octopus = Octopus(100, 200, moving_right=True)
        self.assertEqual(octopus.speed_x, 0.5)

    def test_octopus_speed_when_moving_left(self):
        """Test that Octopus speed is -0.5 when moving left."""
        octopus = Octopus(100, 200, moving_right=False)
        self.assertEqual(octopus.speed_x, -0.5)

    def test_octopus_default_direction_is_right(self):
        """Test that Octopus defaults to moving right when direction not specified."""
        octopus = Octopus(100, 200)
        self.assertEqual(octopus.speed_x, 0.5)


if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()
