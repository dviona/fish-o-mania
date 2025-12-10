"""
Tavish, Debbie, Zihao, Arahdya
Unit tests for AnimatedFish class.

Tests basic fish behavior like movement, animation, and state changes.
Run with: python -m pytest test_animated_fish.py
or: python test_animated_fish.py

Note: This file includes the AnimatedFish class inline for testing purposes.
"""

import unittest
import pygame
import os
import random


class AnimatedFish(pygame.sprite.Sprite):
    """
    Base class for all animated fish.
    All specific fish types inherit from this.
    """

    # Cooldown duration for recently released fish (3 seconds)
    RELEASE_COOLDOWN = 3000

    def __init__(self, sprite_sheet_path, frame_width, frame_height,
                 num_frames, x, y, speed_x, fish_type="generic",
                 death_animation_path=None):
        super().__init__()

        self.fish_type = fish_type
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.speed_x = speed_x
        self.speed_y = random.uniform(-0.5, 0.5)

        self.flip_horizontal = (speed_x < 0)

        self.death_animation_path = death_animation_path
        self.death_animation_created = False

        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = random.randint(5, 10)

        sprite_path = sprite_sheet_path
        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
        self.frames = self.load_frames()

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.is_catchable = True
        self.value = 10
        self.rarity = "danger"

        self.caught = False
        self.is_caught = False
        self.is_hooked = False
        
        # Recently released state (can't be caught again immediately)
        self.recently_released = False
        self.release_time = 0

    def is_release_cooldown_over(self):
        """Check if the release cooldown has expired."""
        if not self.recently_released:
            return True
        return pygame.time.get_ticks() - self.release_time >= self.RELEASE_COOLDOWN

    def start_rising(self):
        self.caught = True
        self.is_caught = True

    def load_frames(self):
        """Extract individual frames from sprite sheet."""
        frames = []
        for i in range(self.num_frames):
            x = i * self.frame_width
            frame = pygame.Surface((self.frame_width, self.frame_height),
                                   pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0),
                       (x, 0, self.frame_width, self.frame_height))

            scaled_size = (self.frame_width * 2, self.frame_height * 2)
            frame = pygame.transform.scale(frame, scaled_size)

            if self.fish_type == "Danger Fish":
                new_frame = pygame.Surface((frame.get_width(), frame.get_height() + 6), pygame.SRCALPHA)
                new_frame.blit(frame, (0, 6))
                line_y = 3
                line_x1 = frame.get_width() // 2 - 15
                line_x2 = frame.get_width() // 2 + 15
                pygame.draw.line(new_frame, (255, 0, 0), (line_x1, line_y), (line_x2, line_y), 2)
                frame = new_frame

            frames.append(frame)

        return frames

    def update(self):
        """Update animation and position."""
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.image = self.frames[self.current_frame]
        
        # Check if release cooldown is over
        if self.recently_released and self.is_release_cooldown_over():
            self.recently_released = False
        
        # If hooked (danger fish during scream period), stay in place
        if self.is_hooked:
            return
        
        # If caught, fish is removed - death animation handles the visual
        if self.caught:
            return
        
        # Normal movement
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def get_info(self):
        """Return fish information."""
        return {
            "type": self.fish_type,
            "value": self.value,
            "rarity": self.rarity
        }


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
