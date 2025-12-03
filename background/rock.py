"""
Rock Module for Fish-O-Mania.

This module contains the Rock class for static underwater decorations.
"""

import pygame
import random
import math


class Rock:
    """
    Static rock decoration.

    Draws an elliptical rock with simple shading for depth.

    Attributes:
        x (int): X-coordinate of rock.
        y (int): Y-coordinate of rock.
        width (int): Rock width in pixels.
        height (int): Rock height in pixels.
    """

    def __init__(self, x, y):
        """
        Initialize a rock at the specified position.

        Args:
            x (int): X-coordinate for rock.
            y (int): Y-coordinate for rock.
        """
        self.x = x
        self.y = y
        self.width = random.randint(30, 80)
        self.height = random.randint(20, 50)

        # Color with highlight and shadow variants
        self.color = random.choice([
            (105, 105, 105),  # Dim gray
            (119, 136, 153),  # Light slate gray
            (112, 128, 144),  # Slate gray
        ])
        self.highlight_color = tuple(min(c + 30, 255) for c in self.color)
        self.shadow_color = tuple(max(c - 30, 0) for c in self.color)

    def draw(self, surface):
        """
        Draw the rock with shading.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        # Main rock body
        pygame.draw.ellipse(
            surface,
            self.color,
            (self.x, self.y, self.width, self.height)
        )

        # Highlight (top-left area)
        highlight_rect = (
            self.x + 5,
            self.y + 5,
            self.width // 3,
            self.height // 3
        )
        pygame.draw.ellipse(surface, self.highlight_color, highlight_rect)

        # Shadow arc (bottom-right edge)
        pygame.draw.arc(
            surface,
            self.shadow_color,
            (self.x, self.y, self.width, self.height),
            math.pi,
            math.pi * 1.5,
            3
        )