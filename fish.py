"""
This File contains all the fish and fish-related classes.
"""

import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, WATER_SURFACE, WATER_BOTTOM


class AnimatedFish(pygame.sprite.Sprite):
    """
    Base class for all animated fish.
    All specific fish types inherit from this.
    """

    def __init__(self, sprite_sheet_path, frame_width, frame_height,
                 num_frames, x, y, speed_x, fish_type="generic"):
        super().__init__()

        # Fish properties
        self.fish_type = fish_type
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.speed_x = speed_x
        self.speed_y = random.uniform(-0.5, 0.5)

        # Animation
        self.current_frame = 0
        self.frame_counter = 0
        self.frame_delay = random.randint(5, 10)

        # Load sprite sheet
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.frames = self.load_frames()

        # Set initial image and position
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Game attributes
        self.is_catchable = True
        self.value = 10
        self.rarity = "common"

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
            frame = pygame.transform.scale(frame,
                                          (self.frame_width * 2,
                                           self.frame_height * 2))
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


class GoldenTrout(AnimatedFish):
    """Rare, valuable golden trout."""

    def __init__(self, x, y):
        super().__init__(
            sprite_sheet_path="graphics/turtle.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=x,
            y=y,
            speed_x=0.5,
            fish_type="Golden Trout"
        )
        self.value = 150
        self.rarity = "rare"


class CommonFish(AnimatedFish):
    """Common fish, easy to catch."""

    def __init__(self, x, y):
        super().__init__(
            sprite_sheet_path="graphics/turtle.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=x,
            y=y,
            speed_x=0.7,
            fish_type="Common Fish"
        )
        self.value = 25
        self.rarity = "common"


class FastFish(AnimatedFish):
    """Fast-moving fish, harder to catch."""

    def __init__(self, x, y):
        super().__init__(
            sprite_sheet_path="graphics/shark.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=x,
            y=y,
            speed_x=0.75,
            fish_type="Speed Fish"
        )
        self.value = 75
        self.rarity = "uncommon"


class LargeFish(AnimatedFish):
    """Large, slow-moving fish."""

    def __init__(self, x, y):
        super().__init__(
            sprite_sheet_path="graphics/octopus.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=x,
            y=y,
            speed_x=0.5,
            fish_type="Large Bass"
        )
        self.value = 100
        self.rarity = "uncommon"

