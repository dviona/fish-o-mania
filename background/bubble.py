"""
Bubble Module for Fish-O-Mania.

This module contains the Bubble class for rising bubble effects.
"""

import pygame
import random
import math
from mechanics.constants import WATER_SURFACE, WHITE


class Bubble:
    """
    Rising bubble effect with horizontal wobble.

    Simulates air bubbles rising through water with slight
    side-to-side movement.

    Attributes:
        x (float): Current X-coordinate.
        y (float): Current Y-coordinate.
        radius (int): Bubble size in pixels.
        speed (float): Vertical rise speed.
        alive (bool): Whether bubble should continue animating.
    """

    def __init__(self, x, y):
        """
        Initialize a bubble at the specified position.

        Args:
            x (float): X-coordinate for bubble start.
            y (float): Y-coordinate for bubble start.
        """
        self.x = x
        self.y = y
        self.radius = random.randint(3, 8)
        self.speed = random.uniform(0.5, 1.5)

        # Wobble parameters
        self.wobble = random.uniform(-0.3, 0.3)
        self.wobble_offset = random.uniform(0, math.pi * 2)
        self.time = 0

        self.alive = True

    def update(self):
        """Update bubble position (rise and wobble)."""
        self.y -= self.speed
        self.x += math.sin(self.time + self.wobble_offset) * self.wobble
        self.time += 0.1

        # Remove bubble when it reaches the surface
        if self.y < WATER_SURFACE:
            self.alive = False

    def draw(self, surface):
        """
        Draw the bubble with shine effect.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        if not self.alive:
            return

        # Main bubble
        pygame.draw.circle(
            surface,
            (173, 216, 230),  # Light blue
            (int(self.x), int(self.y)),
            self.radius
        )

        # Shine highlight (upper-left)
        shine_x = int(self.x - self.radius // 3)
        shine_y = int(self.y - self.radius // 3)
        pygame.draw.circle(
            surface,
            WHITE,
            (shine_x, shine_y),
            max(1, self.radius // 3)
        )