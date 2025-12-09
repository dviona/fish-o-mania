"""
Animated Fish Base Class

This module contains the base AnimatedFish class that all fish types inherit from
"""

import pygame
import random
from mechanics.constants import SCREEN_WIDTH, WATER_SURFACE, WATER_BOTTOM
from fish.death_animation import DeathAnimation


class AnimatedFish(pygame.sprite.Sprite):
    """
    Base class for all animated fish

    Handles sprite sheet loading, animation, movement, and
    screen boundary behavior. All specific fish types inherit from this

    Attributes:
        fish_type (str): Name of the fish type
        speed_x (float): Horizontal movement speed
        speed_y (float): Vertical movement speed
        value (int): Points awarded when caught
        rarity (str): Rarity classification
    """

    # Cooldown duration for recently released dangerous fish (3 seconds)
    # so that the hook does not collide continuously with anglo fish
    release_cooldown = 3000

    def __init__(self, sprite_sheet_path, frame_width, frame_height,
                 num_frames, x, y, speed_x, fish_type="generic",
                 death_animation_path=None):
        """
        Initialize the animated fish.

        Args:
            sprite_sheet_path: path to sprite sheet image
            frame_width: width of each animation frame
            frame_height: height of each animation frame
            num_frames: number of frames in animation
            x: starting X-coordinate
            y: starting Y-coordinate
            speed_x: horizontal movement speed
            fish_type : name of the fish type
            death_animation_path (str): Path to death animation sprite sheet
        """
        # super().__init__() is a Python call that runs the parent class’s constructor (__init__ method)
        # inside a child class, so the parent part of the object gets properly initialized.
        # Any method could be called by super().method(args)
        super().__init__()

        # Fish properties
        self.fish_type = fish_type
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.speed_x = speed_x
        self.speed_y = random.uniform(-0.5, 0.5)

        # Death animation
        self.death_animation_path = death_animation_path
        self.death_animation_created = False

        # Animation control
        self.current_frame = 0
        self.frame_counter = 0
        # frame_delay is number of iterations of game before load_frames moves from one frame to the next one
        # we set frames of delay randomly so that the different types moves at different speed
        self.frame_delay = random.randint(5, 10)

        # Load sprite sheet
        # convert alpha
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

        # Caught/hooked state
        self.caught = False
        self.is_caught = False
        # is_hooked is for generating the pause for anglo fish
        self.is_hooked = False

        # Recently released state,
        self.recently_released = False
        self.release_time = 0

    def _load_frames(self):
        """Extract individual frames from sprite sheet"""
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
        """Add red warning line above the fish frame to differentiate"""
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

    def is_release_cooldown_over(self):
        """Check if the release cooldown has expired"""
        if not self.recently_released:
            return True
        return pygame.time.get_ticks() - self.release_time >= self.release_cooldown

    def start_rising(self):
        """Mark fish as caught and start rising animation"""
        self.caught = True
        self.is_caught = True

    def update(self):
        """Update animation and position"""
        self._update_animation()

        # Check if release cooldown is over
        if self.recently_released and self.is_release_cooldown_over():
            self.recently_released = False

        # If hooked (danger fish during scream period), stay in place
        if self.is_hooked:
            return

        # If caught, fish is removed - death animation handles the visual
        if self.caught:
            return

        self._update_position()

    def _update_animation(self):
        """frame_counter: counts how many game iterations has passed since the last frame change
        frame_delay: Only when the counter reaches that delay does the code advance current_frame and update self.image """
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.image = self.frames[self.current_frame]

    def _update_position(self):
        """Update fish position and handle boundaries"""
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
        Return fish information

        Returns:
            dict: Contains type, value, and rarity
        """
        return {
            "type": self.fish_type,
            "value": self.value,
            "rarity": self.rarity
        }

    def create_death_animation(self):
        """
        Create and return a death animation sprite. Only creates once

        Returns:
            DeathAnimation: The death animation sprite, or None if no path
                or already created
        """
        if self.death_animation_path and not self.death_animation_created:
            self.death_animation_created = True
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
