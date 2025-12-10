"""
Tavish, Debbie, Zac, Aradhya

Testing for Endless Mode
"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame

# Initialize pygame BEFORE imports that need it
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.display.set_mode((800, 600))

import unittest
from modes.mode_endless import (
    format_time,
    draw_pause_overlay,
    draw_water_background,
    draw_game_over_screen,
)


class TestEndlessMode(unittest.TestCase):

    # Check of the time format is correct
    def test_format_time(self):
        self.assertEqual(format_time(0), "00:00")
        self.assertEqual(format_time(59), "00:59")
        self.assertEqual(format_time(60), "01:00")
        self.assertEqual(format_time(125), "02:05")

    # Check if the background pause loads correctly
    def test_draw_pause_overlay(self):
        surface = pygame.Surface((800, 600))
        try:
            draw_pause_overlay(surface)
        except Exception as e:
            self.fail(f"draw_pause_overlay crashed: {e}")

    # Check if the background water loads correctly
    def test_draw_water_background(self):
        surface = pygame.Surface((800, 600))
        try:
            draw_water_background(surface)
        except Exception as e:
            self.fail(f"draw_water_background crashed: {e}")

    # Check if esc key is working
    def test_escape_key(self):
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_ESCAPE}))
        events = pygame.event.get()

        keys = [e.key for e in events if e.type == pygame.KEYDOWN]
        self.assertIn(pygame.K_ESCAPE, keys)

    # Check if game over screen draws correctly
    def test_draw_game_over_screen(self):
        surface = pygame.Surface((800, 600))
        try:
            draw_game_over_screen(
                surface,
                score=100,
                fish_caught_count=5,
                time_played=123,
                high_score_result={"is_new_high": False}
            )
        except Exception as e:
            self.fail(f"draw_game_over_screen crashed: {e}")


if __name__ == "__main__":
    unittest.main(exit=False)
    pygame.quit()
