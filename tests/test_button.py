"""
Debbie Tavish Zac and Aradhya

Testing for the class Button

"""
import pygame
import unittest
from ui.button import Button

pygame.init()
pygame.display.set_mode((800, 600), pygame.HIDDEN)

class TestButton(unittest.TestCase):
    # Test the Button class
    def setUp(self):
        self.button = Button(
            x=100,
            y=100,
            width=200,
            height=50,
            text="Test Button",
            enabled=True
        )

    def test_initialization(self):
        # Test if the button initializes with correct attributes.
        self.assertEqual(self.button.x, 100)
        self.assertEqual(self.button.y, 100)
        self.assertEqual(self.button.width, 200)
        self.assertEqual(self.button.height, 50)
        self.assertEqual(self.button.text, "Test Button")
        self.assertTrue(self.button.enabled)

    def test_update_hovered_state(self):
        # Test if the button updates its hovered state correctly.
        mouse_pos = (150, 120)  # <-- Inside the button
        self.button.update(mouse_pos)
        self.assertTrue(self.button.hovered)

        mouse_pos = (50, 50)  # <-- Outside the button
        self.button.update(mouse_pos)
        self.assertFalse(self.button.hovered)

    def test_button_rect(self):
        # Test if the button rectangle is correct.
        rect = pygame.Rect(self.button.x, self.button.y, self.button.width, self.button.height)
        self.assertEqual(rect, pygame.Rect(100, 100, 200, 50))

    def test_draw_button(self):
        # Test if the button draws without errors.
        surface = pygame.Surface((400, 300))
        try:
            self.button.draw(surface)
        except Exception as e:
            self.fail(f"Button.draw() raised an exception: {e}")

    def test_disabled_button_draw(self):
        # Test drawing a disabled button.
        self.button.enabled = False
        surface = pygame.Surface((400, 300))
        try:
            self.button.draw(surface)
        except Exception as e:
            self.fail(f"Button.draw() for disabled button raised an exception: {e}")
    
    def test_enabled_button_state(self):
        # Test the enabled state of the button.
        self.button.enabled = False
        mouse_pos = (150, 120)  # <-- Inside the button
        self.button.update(mouse_pos)
        self.assertFalse(self.button.hovered)  # Should not be hovered if disabled

if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()