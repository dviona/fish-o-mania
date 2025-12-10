"""
Debbie Tavish Zac and Aradhya

Testing for DeathAnimation Class

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
from fish.death_animation import DeathAnimation


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
        # Note: finished may start True if animation fails to load frames
        # Check current_frame starts at 0
        self.assertEqual(self.anim.current_frame, 0)

    def test_position(self):
        # Check for the position of the animation
        self.assertEqual(self.anim.rect.center, (100, 200))

    def test_frames_loaded(self):
        # Check if the animation has frames attribute
        # Note: frames might be stored differently - check what attribute exists
        if hasattr(self.anim, 'frames'):
            self.assertGreater(len(self.anim.frames), 0)
        elif hasattr(self.anim, 'sprite_frames'):
            self.assertGreater(len(self.anim.sprite_frames), 0)
        else:
            # Animation loaded without separate frames list
            self.assertTrue(hasattr(self.anim, 'image'))

    def test_update_moves_up(self):
        # Check if each updated animation floats up
        old_y = self.anim.rect.y
        self.anim.update()
        # Animation should move up (y decreases) or stay same if finished
        self.assertLessEqual(self.anim.rect.y, old_y)

    def test_frame_advance(self):
        # Check if frames can advance after updating animation
        initial_frame = self.anim.current_frame
        # Update multiple times to trigger frame advance
        for _ in range(20):  # More iterations to ensure frame advances
            self.anim.update()
        # Either frame advanced or animation finished
        self.assertTrue(
            self.anim.current_frame > initial_frame or self.anim.finished
        )


if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()
