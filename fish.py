"""
This File contains all the fish and fish-related classes.
"""

import pygame
import random
from mechanics.constants import (SCREEN_WIDTH, SCREEN_HEIGHT, WATER_SURFACE,
                       WATER_BOTTOM)


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
            sprite_path = sprite_sheet_path
            self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            self.frames = self.load_frames()

            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
        except pygame.error as e:
            print(f"Error loading death animation: {e}")
            self.finished = True
            # Create a dummy image to prevent further errors
            dummy_size = (frame_width * 2, frame_height * 2)
            self.image = pygame.Surface(dummy_size, pygame.SRCALPHA)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

    def load_frames(self):
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
                # Create new surface with space above
                new_frame = pygame.Surface((frame.get_width(), frame.get_height() + 6), pygame.SRCALPHA)
                # Draw fish at bottom (offset down)
                new_frame.blit(frame, (0, 6))
                # Draw red line at top
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

            # Move upward
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

        # Determine if fish should be flipped (moving left)
        self.flip_horizontal = (speed_x < 0)

        # Death animation
        self.death_animation_path = death_animation_path

        # Animation
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = random.randint(5, 10)

        # Load sprite sheet
        sprite_path = sprite_sheet_path
        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
        self.frames = self.load_frames()

        # Set initial image and position
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Game attributes
        self.is_catchable = True
        self.value = 10
        self.rarity = "danger"

    def load_frames(self):
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
                # Create new surface with space above
                new_frame = pygame.Surface((frame.get_width(), frame.get_height() + 6), pygame.SRCALPHA)
                # Draw fish at bottom (offset down)
                new_frame.blit(frame, (0, 6))
                # Draw red line at top
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
            # Pass is_danger_fish flag to death animation
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


class Turtle(AnimatedFish):
    """Rare, valuable turtle."""

    def __init__(self, x, y, moving_right=True):
        # Set speed direction based on spawn side
        speed = 0.5 if moving_right else -0.5

        super().__init__(
            sprite_sheet_path="graphics/turtle.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=x,
            y=y,
            speed_x=speed,
            fish_type="Turtle",
            death_animation_path="graphics/turtle_death.png"
        )
        self.value = 150
        self.rarity = "rare"


class DangerFish(AnimatedFish):
    """Danger fish - lose a life if caught."""

    def __init__(self, x, y, moving_right=True):
        # Set speed direction based on spawn side
        speed = 0.7 if moving_right else -0.7

        super().__init__(
            sprite_sheet_path="graphics/danger_fish.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=x,
            y=y,
            speed_x=speed,
            fish_type="Danger Fish",
            death_animation_path="graphics/danger_fish_death.png"
        )
        self.value = 25
        self.rarity = "danger"


class Shark(AnimatedFish):
    """Fast-moving shark, harder to catch."""

    def __init__(self, x, y, moving_right=True):
        # Set speed direction based on spawn side
        speed = 0.75 if moving_right else -0.75

        super().__init__(
            sprite_sheet_path="graphics/shark.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=x,
            y=y,
            speed_x=speed,
            fish_type="Shark",
            death_animation_path="graphics/shark_death.png"
        )
        self.value = 75
        self.rarity = "uncommon"


class Octopus(AnimatedFish):
    """Large, slow-moving octopus."""

    def __init__(self, x, y, moving_right=True):
        # Set speed direction based on spawn side
        speed = 0.5 if moving_right else -0.5

        super().__init__(
            sprite_sheet_path="graphics/octopus.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=x,
            y=y,
            speed_x=speed,
            fish_type="Octopus",
            death_animation_path="graphics/octopus_death.png"
        )
        self.value = 100
        self.rarity = "uncommon"
