"""
Unit tests for AnimatedFish class.

Tests basic fish behavior like movement, animation, and state changes.
Run with: python -m pytest test_animated_fish.py
or: python test_animated_fish.py
"""

import unittest
import pygame
import os


# Import AnimatedFish from fish.py file in the current directory
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fish import AnimatedFish


class TestAnimatedFish(unittest.TestCase):
    """Test cases for AnimatedFish class."""

    def setUp(self):
        """Set up test fixtures before each test."""
        # Initialize pygame if not already initialized
        if not pygame.get_init():
            pygame.init()
            pygame.display.set_mode((1, 1))  # Minimal display for testing
        
        # Create a temporary sprite sheet image for this test
        self.temp_image_path = "test_fish_temp.png"
        
        # Create a simple 288x48 image (6 frames of 48x48 to match real fish)
        surface = pygame.Surface((288, 48))
        surface.fill((100, 150, 200))  # Light blue background
        
        # Draw simple rectangles to represent fish frames
        for i in range(6):
            x = i * 48
            pygame.draw.rect(surface, (255, 100, 0), (x + 5, 5, 38, 38))
        
        pygame.image.save(surface, self.temp_image_path)
        
        # Create a simple test fish using the temporary image
        self.fish = AnimatedFish(
            sprite_sheet_path=self.temp_image_path,
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=100,
            y=200,
            speed_x=2.0,
            fish_type="Test Fish"
        )

    def tearDown(self):
        """Clean up after each test."""
        # Remove the temporary image file
        if os.path.exists(self.temp_image_path):
            os.remove(self.temp_image_path)

    def test_fish_creation(self):
        """Test that a fish is created with correct initial values."""
        self.assertEqual(self.fish.fish_type, "Test Fish")
        self.assertEqual(self.fish.speed_x, 2.0)
        self.assertEqual(self.fish.value, 10)
        self.assertEqual(self.fish.rarity, "danger")

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
        self.fish.start_rising()
        self.assertTrue(self.fish.caught)
        self.assertTrue(self.fish.is_caught)

    def test_get_info(self):
        """Test that get_info returns correct fish information."""
        info = self.fish.get_info()
        self.assertEqual(info["type"], "Test Fish")
        self.assertEqual(info["value"], 10)
        self.assertEqual(info["rarity"], "danger")

    def test_release_cooldown_initially_false(self):
        """Test that fish doesn't start with release cooldown."""
        self.assertFalse(self.fish.recently_released)
        self.assertTrue(self.fish.is_release_cooldown_over())

    def test_release_cooldown_when_active(self):
        """Test that release cooldown works when activated."""
        self.fish.recently_released = True
        self.fish.release_time = pygame.time.get_ticks()
        self.assertFalse(self.fish.is_release_cooldown_over())

    def test_hooked_state(self):
        """Test that fish can be hooked."""
        self.assertFalse(self.fish.is_hooked)
        self.fish.is_hooked = True
        self.assertTrue(self.fish.is_hooked)

    def test_hooked_fish_does_not_move(self):
        """Test that hooked fish stays in place."""
        self.fish.is_hooked = True
        initial_x = self.fish.rect.x
        initial_y = self.fish.rect.y
        
        for _ in range(10):
            self.fish.update()
        
        self.assertEqual(self.fish.rect.x, initial_x)
        self.assertEqual(self.fish.rect.y, initial_y)

    def test_caught_fish_does_not_move(self):
        """Test that caught fish stays in place."""
        self.fish.caught = True
        initial_x = self.fish.rect.x
        initial_y = self.fish.rect.y
        
        for _ in range(10):
            self.fish.update()
        
        self.assertEqual(self.fish.rect.x, initial_x)
        self.assertEqual(self.fish.rect.y, initial_y)

    def test_animation_frame_advances(self):
        """Test that animation frames cycle through."""
        for _ in range(50):
            self.fish.update()
        
        self.assertTrue(0 <= self.fish.current_frame < 6)

    def test_fish_horizontal_movement(self):
        """Test that fish moves horizontally."""
        initial_x = self.fish.rect.x
        
        for _ in range(10):
            self.fish.update()
        
        self.assertNotEqual(self.fish.rect.x, initial_x)

    def test_fish_type_danger(self):
        """Test creating a danger fish."""
        danger_temp = "danger_test_temp.png"
        surface = pygame.Surface((288, 48))
        surface.fill((255, 0, 0))
        pygame.image.save(surface, danger_temp)
        
        danger_fish = AnimatedFish(
            sprite_sheet_path=danger_temp,
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=100,
            y=200,
            speed_x=2.0,
            fish_type="Danger Fish"
        )
        
        self.assertEqual(danger_fish.fish_type, "Danger Fish")
        
        if os.path.exists(danger_temp):
            os.remove(danger_temp)

    def test_death_animation_path(self):
        """Test that death animation path can be set."""
        fish_with_death = AnimatedFish(
            sprite_sheet_path=self.temp_image_path,
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=100,
            y=200,
            speed_x=2.0,
            fish_type="Test Fish",
            death_animation_path="test_death.png"
        )
        
        self.assertEqual(fish_with_death.death_animation_path, "test_death.png")
        self.assertFalse(fish_with_death.death_animation_created)

    def test_recently_released_clears_after_cooldown(self):
        """Test that recently_released flag clears after update cycles."""
        self.fish.recently_released = True
        self.fish.release_time = pygame.time.get_ticks() - 5000
        
        self.fish.update()
        
        self.assertFalse(self.fish.recently_released)

    def test_negative_speed_moves_left(self):
        """Test that negative speed moves fish left."""
        left_fish = AnimatedFish(
            sprite_sheet_path=self.temp_image_path,
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=500,
            y=200,
            speed_x=-2.0,
            fish_type="Left Fish"
        )
        
        initial_x = left_fish.rect.x
        
        for _ in range(10):
            left_fish.update()
        
        self.assertLess(left_fish.rect.x, initial_x)


# Run tests if this file is executed directly
if __name__ == '__main__':
    # Clean up pygame at the end
    unittest.main(exit=False)
    pygame.quit()
