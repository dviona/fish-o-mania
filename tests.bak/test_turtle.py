"""
Debbie Tavish Zac and Aradhya

Unit tests for Turtle class
"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

# Initialize pygame BEFORE imports that need it
pygame.init()
pygame.mixer.init()
pygame.display.set_mode((800, 600))

import unittest
from fish.turtle import Turtle


class TestTurtle(unittest.TestCase):
    """Tests for Turtle class."""

    def test_turtle_value_is_150(self):
        """Test that Turtle has a point value of 150."""
        turtle = Turtle(100, 200)
        self.assertEqual(turtle.value, 150)

    def test_turtle_rarity_is_rare(self):
        """Test that Turtle has rare rarity."""
        turtle = Turtle(100, 200)
        self.assertEqual(turtle.rarity, "rare")

    def test_turtle_fish_type_is_turtle(self):
        """Test that fish_type is set to 'Turtle'."""
        turtle = Turtle(100, 200)
        self.assertEqual(turtle.fish_type, "Turtle")

    def test_turtle_speed_when_moving_right(self):
        """Test that Turtle speed is 0.5 when moving right."""
        turtle = Turtle(100, 200, moving_right=True)
        self.assertEqual(turtle.speed_x, 0.5)

    def test_turtle_speed_when_moving_left(self):
        """Test that Turtle speed is -0.5 when moving left."""
        turtle = Turtle(100, 200, moving_right=False)
        self.assertEqual(turtle.speed_x, -0.5)

    def test_turtle_default_direction_is_right(self):
        """Test that Turtle defaults to moving right when direction not specified."""
        turtle = Turtle(100, 200)
        self.assertEqual(turtle.speed_x, 0.5)


if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()
