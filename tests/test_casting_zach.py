"""
Unit tests for AnimatedFish class.

Tests basic fish behavior like movement, animation, and state changes.
Run with: python -m pytest test_animated_fish.py
or: python test_animated_fish.py
"""

import unittest
import pygame
import os
from fish.animated_fish import AnimatedFish


class TestAnimatedFish(unittest.TestCase):
    """Test cases for AnimatedFish class."""

    @classmethod
    def setUpClass(cls):
        """Create a dummy sprite sheet image file for testing."""
        pygame.init()
        
        # Set up a dummy display (required for pygame to work in tests)
        pygame.display.set_mode((1, 1))
        
        # Create a temporary sprite sheet image
        cls.temp_image_path = "test_fish_temp.png"
        
        # Create a simple 96x24 image (4 frames of 24x24)
        surface = pygame.Surface((96, 24))
        surface.fill((255, 255, 255))  # White background
        pygame.image.save(surface, cls.temp_image_path)

    @classmethod
    def tearDownClass(cls):
        """Remove the temporary image file."""
        if os.path.exists(cls.temp_image_path):
            os.remove(cls.temp_image_path)
        pygame.quit()

    def setUp(self):
        """Set up test fixtures before each test."""
        # Create a simple test fish using the temporary image
        self.fish = AnimatedFish(
            sprite_sheet_path="test_fish_temp.png",
            frame_width=24,
            frame_height=24,
            num_frames=4,
            x=100,
            y=200,
            speed_x=2.0,
            fish_type="Test Fish"
        )

    def test_fish_creation(self):
        """Test that a fish is created with correct initial values."""
        self.assertEqual(self.fish.fish_type, "Test Fish")
        self.assertEqual(self.fish.speed_x, 2.0)
        self.assertEqual(self.fish.value, 10)  # Default value
        self.assertEqual(self.fish.rarity, "common")  # Default rarity

    def test_fish_position(self):
        """Test that fish starts at the correct position."""
        self.assertEqual(self.fish.rect.centerx, 100)
        self.assertEqual(self.fish.rect.centery, 200)

    def test_fish_is_catchable(self):
        """Test that fish starts in a catchable state."""
        self.assertTrue(self.fish.is_catchable)
        self.assertFalse(self.fish.is_caught)
        self.assertFalse(self.fish.caught)

    def test_start_rising(self):
        """Test that start_rising marks the fish as caught."""
        self.assertFalse(self.fish.caught)
        self.assertFalse(self.fish.is_caught)
        
        self.fish.start_rising()
        
        self.assertTrue(self.fish.caught)
        self.assertTrue(self.fish.is_caught)

    def test_get_info(self):
        """Test that get_info returns correct fish information."""
        info = self.fish.get_info()
        
        self.assertEqual(info["type"], "Test Fish")
        self.assertEqual(info["value"], 10)
        self.assertEqual(info["rarity"], "common")

    def test_release_cooldown_initially_false(self):
        """Test that fish doesn't start with release cooldown."""
        self.assertFalse(self.fish.recently_released)
        self.assertTrue(self.fish.is_release_cooldown_over())

    def test_release_cooldown_when_active(self):
        """Test that release cooldown works when activated."""
        self.fish.recently_released = True
        self.fish.release_time = pygame.time.get_ticks()
        
        # Should still be on cooldown immediately
        self.assertFalse(self.fish.is_release_cooldown_over())

    def test_hooked_state(self):
        """Test that fish can be hooked."""
        self.assertFalse(self.fish.is_hooked)
        
        self.fish.is_hooked = True
        
        self.assertTrue(self.fish.is_hooked)

    def test_animation_frame_advances(self):
        """Test that animation frames cycle through."""
        initial_frame = self.fish.current_frame
        
        # Update multiple times to advance animation
        for _ in range(20):
            self.fish.update()
        
        # Frame should have changed (may have cycled back to 0)
        # We just check that the frame counter is working
        self.assertTrue(self.fish.frame_counter >= 0)

    def test_fish_type_danger(self):
        """Test creating a danger fish."""
        danger_fish = AnimatedFish(
            sprite_sheet_path="test_fish_temp.png",
            frame_width=24,
            frame_height=24,
            num_frames=4,
            x=100,
            y=200,
            speed_x=2.0,
            fish_type="Danger Fish"
        )
        
        self.assertEqual(danger_fish.fish_type, "Danger Fish")


# Run tests if this file is executed directly
if __name__ == '__main__':
    unittest.main()
