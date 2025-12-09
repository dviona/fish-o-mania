"""
Seaweed Module for Fish-O-Mania

This module contains the Seaweed class for animated seaweed
"""

import pygame
import random
import math
from mechanics.constants import SCREEN_HEIGHT


class Seaweed:
    """
    Animated swaying seaweed

    Uses sine wave motion to simulate underwater plant movement,
    with more sway at the top than the base.

    Attributes:
        x (int): X-coordinate of seaweed base
        base_y (int): Y-coordinate of seaweed base (screen bottom)
        height (int): Total height of the seaweed
        segments (int): Number of segments for smooth curve
    """

    def __init__(self, x):
        """
        Initialize seaweed at the specified X position

        Args:
            x (int): X-coordinate for seaweed base
        """
        self.x = x
        self.base_y = SCREEN_HEIGHT - 2
        self.height = random.randint(80, 150)
        self.segments = 8

        # Sway animation parameters
        self.sway_offset = random.uniform(0, math.pi * 2)
        self.sway_speed = random.uniform(0.02, 0.05)
        self.sway_amount = random.randint(10, 20)
        self.time = 0

        # Appearance
        self.color = (34, 139, 34)  # Forest green
        self.width = random.randint(8, 12)

    def update(self):
        """Update seaweed sway animation"""
        self.time += self.sway_speed

    def draw(self, surface):
        """
        Draw the swaying seaweed

        Args:
            surface (pygame.Surface): Surface to draw on
        """
        segment_height = self.height / self.segments
        points = [(self.x, self.base_y)]

        # Calculate position of each segment
        for i in range(1, self.segments + 1):
            # Sway increases with height
            sway_factor = i / self.segments
            sway_angle = self.time + self.sway_offset + i * 0.3
            sway = math.sin(sway_angle) * self.sway_amount * sway_factor

            x = self.x + sway
            y = self.base_y - (segment_height * i)
            points.append((x, y))

        # Draw seaweed as connected line segments
        if len(points) > 1:
            for i in range(len(points) - 1):
                # Width decreases toward top
                width = max(2, self.width - i)
                pygame.draw.line(
                    surface,
                    self.color,
                    points[i],
                    points[i + 1],
                    width
                )
