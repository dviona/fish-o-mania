"""
Animated Fish Base Class for Fish-O-Mania.

This module contains the base AnimatedFish class and DeathAnimation class
that all fish types inherit from.
"""

import pygame
import random
from mechanics.constants import SCREEN_WIDTH, WATER_SURFACE, WATER_BOTTOM


class DeathAnimation(pygame.sprite.Sprite):
    """Death animation that plays when a fish is caught."""

    def __init__(self, x, y, sprite_sheet_path, frame_width, frame_height,
                 num_frames, is_danger_fish=False):
        super().__init__()

        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.is_danger_fish = is_danger_fish

        # Animation control
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = 5
        self.finished = False

        # Load sprite sheet
        try:
            self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
            self.frames = self._load_frames()
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
        except pygame.error as e:
            print(f"Error loading death animation: {e}")
            self.finished = True
            dummy_size = (frame_width * 2, frame_height * 2)
            self.image = pygame.Surface(dummy_size, pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

    def _load_frames(self):
        """Extract individual frames from sprite sheet."""
        frames = []
        for i in range(self.num_frames):
            x = i * self.frame_width
            frame = pygame.Surface((self.frame_width, self.frame_height),
                                   pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0),
                       (x, 0, self.frame_width, self.frame_height))

            # Scale up 2x
            scaled_size = (self.frame_width * 2, self.frame_height * 2)
            frame = pygame.transform.scale(frame, scaled_size)

            # Add red line above if danger fish
            if self.is_danger_fish:
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
        """Update animation frame."""
        if not self.finished:
            self.frame_counter += 1
            self.rect.y -= 6

            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                self.current_frame += 1

                if self.current_frame >= self.num_frames:
                    self.finished = True
                    self.kill()
                else:
                    self.image = self.frames[self.current_frame]


class AnimatedFish(pygame.sprite.Sprite):
    """
    Base class for all animated fish.
    All specific fish types inherit from this.
    """

    def __init__(self, sprite_sheet_path, frame_width, frame_height,
                 num_frames, x, y, speed_x, fish_type="generic",
                 death_animation_path=None):
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

        # Animation
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
            frame = pygame.Surface((self.frame_width, self.frame_height),
                                   pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0),
                       (x, 0, self.frame_width, self.frame_height))

            # Scale up 2x
            scaled_size = (self.frame_width * 2, self.frame_height * 2)
            frame = pygame.transform.scale(frame, scaled_size)

            # Add red line above if danger fish
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
        # Animate
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.image = self.frames[self.current_frame]

        # Move
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Wrap around screen
        if self.speed_x > 0 and self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        elif self.speed_x < 0 and self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH

        # Keep in water bounds
        if self.rect.top < WATER_SURFACE:
            self.rect.top = WATER_SURFACE
            self.speed_y = abs(self.speed_y)
        elif self.rect.bottom > WATER_BOTTOM:
            self.rect.bottom = WATER_BOTTOM
            self.speed_y = -abs(self.speed_y)

    def get_info(self):
        """Return fish information."""
        return {
            "type": self.fish_type,
            "value": self.value,
            "rarity": self.rarity
        }

    def create_death_animation(self):
        """Create and return a death animation sprite."""
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
