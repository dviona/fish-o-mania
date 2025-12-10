"""
Debbie Tavish Zac and Aradhya


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
from ui import MenuScreen


class TestMenuScreen(unittest.TestCase):

    def test_menu_loads(self):
        # Checks if Menu initializes and draws without crashing
        menu = MenuScreen()
        surface = pygame.Surface((800, 600))
        menu.draw(surface)

    def test_move_selection(self):
        # Check if moving selection up/down doesn't crash
        menu = MenuScreen()
        menu.move_selection(1)
        menu.move_selection(-1)

    def test_handle_click(self):
        # Check if handle click doesn't crash with any position
        menu = MenuScreen()
        surface = pygame.Surface((800, 600))
        pos = (100, 100)
        menu.handle_click(pos)

    def test_update(self):
        # Update method runs without crashing
        menu = MenuScreen()
        menu.update()

    def test_high_scores_toggle(self):
        # Showing high scores toggles without crash
        menu = MenuScreen()
        menu.showing_high_scores = True
        menu.showing_high_scores = False


if __name__ == "__main__":
    unittest.main(exit=False)
    pygame.quit()
