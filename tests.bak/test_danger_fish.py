"""
Debbie Tavish Zac and Aradhya

Testing for DangerFish Class

"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame

# Initialize pygame BEFORE imports that need it
pygame.init()
pygame.mixer.init()
pygame.display.set_mode((800, 600))

import unittest
from fish.danger_fish import DangerFish
from fish.animated_fish import AnimatedFish


class TestDangerFish(unittest.TestCase):

    def setUp(self):
        # Create objects for each test
        self.fish_right = DangerFish(100, 200, moving_right=True)
        self.fish_left = DangerFish(100, 200, moving_right=False)

    def test_death_animation_path(self):
        self.assertEqual(
            self.fish_right.death_animation_path,
            "graphics/danger_fish_death.png"
        )

    def test_inherits_from_animated_fish(self):
        self.assertIsInstance(self.fish_right, AnimatedFish)

    def test_initial_position(self):
        self.assertEqual(self.fish_right.rect.centerx, 100)
        self.assertEqual(self.fish_right.rect.centery, 200)

    def test_movement_speed_direction(self):
        self.assertGreater(self.fish_right.speed_x, 0)
        self.assertLess(self.fish_left.speed_x, 0)
        self.assertAlmostEqual(abs(self.fish_right.speed_x), 0.7)
        self.assertAlmostEqual(abs(self.fish_left.speed_x), 0.7)

    def test_attributes(self):
        self.assertEqual(self.fish_right.value, 25)
        self.assertEqual(self.fish_right.rarity, "danger")
        self.assertEqual(self.fish_right.fish_type, "Danger Fish")


if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()
