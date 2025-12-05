"""
Death Animation Class for Fish-O-Mania.

Handles the animation that plays when a fish is caught.
"""

import pygame


class DeathAnimation(pygame.sprite.Sprite):
    """Death animation that plays when a fish is caught."""

    def __init__(self, x, y, sprite_sheet_path, frame_width, frame_height,
                 num_frames, is_danger_fish=False):
        """
        Initialize the death animation.

        Args:
            x (int): X-coordinate for animation center.
            y (int): Y-coordinate for animation center.
            sprite_sheet_path (str): Path to sprite sheet image.
            frame_width (int): Width of each frame.
            frame_height (int): Height of each frame.
            num_frames (int): Number of frames in animation.
            is_danger_fish (bool): Whether to add red warning line.
        """
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
            if self.is_danger_fish:
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
        """Update animation frame."""
        if self.finished:
            return

        self.frame_counter += 1
        self.rect.y -= 6  # Float upward

        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.current_frame += 1

            if self.current_frame >= self.num_frames:
                self.finished = True
                self.kill()
            else:
                self.image = self.frames[self.current_frame]
