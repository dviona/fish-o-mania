"""
Testing for DeathAnimation Class

"""

import pygame
import unittest
from fish.death_animation import DeathAnimation

pygame.init()
pygame.display.set_mode((800, 600), pygame.HIDDEN)

class TestDeathAnimation(unittest.TestCase):

    def setUp(self):
        self.anim = DeathAnimation(
            x=100,
            y=200,
            sprite_sheet_path="graphics/danger_fish_death.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            is_danger_fish=True
        )

    def test_initial_attributes(self):
        # Check if the attributes are correct
        self.assertEqual(self.anim.frame_width, 48)
        self.assertEqual(self.anim.frame_height, 48)
        self.assertEqual(self.anim.num_frames, 6)
        self.assertFalse(self.anim.finished)
        self.assertEqual(self.anim.current_frame, 0)

    def test_position(self):
        # Check for the position of the animation
        self.assertEqual(self.anim.rect.center, (100, 200))

    def test_frames_loaded(self):
        # Check if the animation have the correct amount of frames
        self.assertEqual(len(self.anim.frames), 6)

    def test_update_moves_up(self):
        # Check if each updated animation floars up by 6 pixels
        old_y = self.anim.rect.y
        self.anim.update()
        self.assertEqual(self.anim.rect.y, old_y - 6)

    def test_frame_advance(self):
        # Check if each frame advances after updating animation
        for _ in range(self.anim.frame_delay):
            self.anim.update()
        self.assertEqual(self.anim.current_frame, 1)

if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()
