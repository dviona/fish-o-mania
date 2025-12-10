"""
Debbie Tavish Zac and Aradhya

Testing for class MenuScreen

"""
import pygame
import unittest
from ui.menu_screen import MenuScreen

pygame.init()
pygame.display.set_mode((800, 600), pygame.HIDDEN)

class TestMenuScreen(unittest.TestCase):
    def setUp(self):
        self.menu_screen = MenuScreen()

    def test_initialization(self):
        # Test if MenuScreen initializes with correct attributes
        self.assertEqual(self.menu_screen.selected_index, 0)
        self.assertFalse(self.menu_screen.showing_high_scores)

    def test_move_selection(self):
        # Test moving selection up and down
        initial_index = self.menu_screen.selected_index
        self.menu_screen.move_selection(1)
        self.assertEqual(self.menu_screen.selected_index, (initial_index + 1) % len(self.menu_screen.buttons))
        self.menu_screen.move_selection(-1)
        self.assertEqual(self.menu_screen.selected_index, initial_index)

    def test_show_high_scores_toggle(self):
        # Test toggling high scores display
        self.assertFalse(self.menu_screen.showing_high_scores)
        self.menu_screen.showing_high_scores = True
        self.assertTrue(self.menu_screen.showing_high_scores)
        self.menu_screen.showing_high_scores = False
        self.assertFalse(self.menu_screen.showing_high_scores)

    def test_transitioning_state(self):
        # Test transitioning state
        self.assertFalse(self.menu_screen.transitioning)
        self.menu_screen.transitioning = True
        self.assertTrue(self.menu_screen.transitioning)
        self.menu_screen.transitioning = False
        self.assertFalse(self.menu_screen.transitioning)

    def test_button_count(self):
        # Test the number of buttons created
        self.assertEqual(len(self.menu_screen.buttons), 5)

if __name__ == '__main__':
    unittest.main(exit = False)
    pygame.quit()