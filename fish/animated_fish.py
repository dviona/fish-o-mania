"""
Animated Fish Base Class for Fish-O-Mania.

This module contains the base AnimatedFish class that all fish types
inherit from.
"""

import pygame
import random
from mechanics.constants import SCREEN_WIDTH, WATER_SURFACE, WATER_BOTTOM
from fish.death_animation import DeathAnimation


class AnimatedFish(pygame.sprite.Sprite):
    """
    Base class for all animated fish.

    Handles sprite sheet loading, animation, movement, and
    screen boundary behavior. All specific fish types inherit from this.

    Attributes:
        fish_type (str): Name of the fish type.
        speed_x (float): Horizontal movement speed.
        speed_y (float): Vertical movement speed.
        value (int): Points awarded when caught.
        rarity (str): Rarity classification.
    """

    def __init__(self, sprite_sheet_path, frame_width, frame_height,
                 num_frames, x, y, speed_x, fish_type="generic",
                 death_animation_path=None):
        """
        Initialize the animated fish.

        Args:
            sprite_sheet_path (str): Path to sprite sheet image.
            frame_width (int): Width of each animation frame.
            frame_height (int): Height of each animation frame.
            num_frames (int): Number of frames in animation.
            x (int): Starting X-coordinate.
            y (int): Starting Y-coordinate.
            speed_x (float): Horizontal movement speed.
            fish_type (str): Name of the fish type.
            death_animation_path (str): Path to death animation sprite sheet.
        """
        super().__init__()

        # Fish properties
        self.fish_type = fish_type
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.speed_x = speed_x
        self.speed_y = random.uniform(-0.5, 0.5)

        # Direction flag
        self.flip_horizontal = (speed_x < 0)

        # Death animation
        self.death_animation_path = death_animation_path

        # Animation control
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = random.randint(5, 10)

        # Load sprite sheet
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frames = self._load_frames()

        # Set initial image and position
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Game attributes (defaults, overridden by subclasses)
        self.is_catchable = True
        self.value = 10
        self.rarity = "common"

    def _load_frames(self):
        """Extract individual frames from sprite sheet."""
        frames = []
        for i in range(self.num_frames):
            x = i * self.frame_width
            frame = pygame.Surface(
                (self.frame_width, self.frame_height),
                pygame.SRCALPHA
            )
            frame.blit(
                self.sprite_sheet,
                (0, 0),
                (x, 0, self.frame_width, self.frame_height)
            )

            # Scale up 2x
            scaled_size = (self.frame_width * 2, self.frame_height * 2)
            frame = pygame.transform.scale(frame, scaled_size)

            # Add red line above if danger fish
            if self.fish_type == "Danger Fish":
                frame = self._add_danger_indicator(frame)

            frames.append(frame)

        return frames

    def _add_danger_indicator(self, frame):
        """Add red warning line above the fish frame."""
        new_frame = pygame.Surface(
            (frame.get_width(), frame.get_height() + 6),
            pygame.SRCALPHA
        )
        new_frame.blit(frame, (0, 6))

        # Draw red line at top
        line_y = 3
        line_x1 = frame.get_width() // 2 - 15
        line_x2 = frame.get_width() // 2 + 15
        pygame.draw.line(
            new_frame,
            (255, 0, 0),
            (line_x1, line_y),
            (line_x2, line_y),
            2
        )

        return new_frame

    def update(self):
        """Update animation and position."""
        self._update_animation()
        self._update_position()

    def _update_animation(self):
        """Cycle through animation frames."""
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.image = self.frames[self.current_frame]

    def _update_position(self):
        """Update fish position and handle boundaries."""
        # Move
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Wrap around screen horizontally
        if self.speed_x > 0 and self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.speed_x < 0 and self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

        # Bounce off water boundaries vertically
        if self.rect.top < WATER_SURFACE:
            self.rect.top = WATER_SURFACE
            self.speed_y = abs(self.speed_y)
        elif self.rect.bottom > WATER_BOTTOM:
            self.rect.bottom = WATER_BOTTOM
            self.speed_y = -abs(self.speed_y)

    def get_info(self):
        """
        Return fish information.

        Returns:
            dict: Contains type, value, and rarity.
        """
        return {
            "type": self.fish_type,
            "value": self.value,
            "rarity": self.rarity
        }

    def create_death_animation(self):
        """
        Create and return a death animation sprite.

        Returns:
            DeathAnimation: The death animation sprite, or None if no path.
        """
        if self.death_animation_path:
            is_danger = (self.fish_type == "Danger Fish")
            return DeathAnimation(
                self.rect.centerx,
                self.rect.centery,
                self.death_animation_path,
                frame_width=48,
                frame_height=48,
                num_frames=6,
                is_danger_fish=is_danger
            )
        return None