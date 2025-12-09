"""
Ripple Module

This module contains the Ripple class for animated water surface effects
"""

import pygame
import random


class Ripple:
    """
    Animated water ripple effect

    Creates an expanding circular ripple that fades out over time,
    simulating disturbance on the water surface

    Attributes:
        x (float): X-coordinate of ripple center
        y (float): Y-coordinate of ripple center
        radius (float): Current radius of the ripple
        max_radius (int): Maximum radius before disappearing
        alpha (int): Current transparency (255 = opaque, 0 = invisible)
        alive (bool): Whether the ripple should continue animating
    """

    def __init__(self, x, y):
        """
        Initialize a ripple at the specified position

        Args:
            x (float): X-coordinate for ripple center
            y (float): Y-coordinate for ripple center
        """
        self.x = x
        self.y = y
        self.radius = 0
        self.max_radius = random.randint(30, 80)
        self.alpha = 255
        self.growth_rate = random.uniform(0.5, 1.0)
        self.fade_rate = 8
        self.alive = True

    def update(self):
        """Update ripple animation (expand and fade)."""
        self.radius += self.growth_rate
        self.alpha -= self.fade_rate

        if self.alpha <= 0 or self.radius >= self.max_radius:
            self.alive = False

    def draw(self, surface):
        """
        Draw the ripple on the given surface.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        if not self.alive or self.alpha <= 0:
            return

        # Create transparent surface for ripple
        ripple_surf = pygame.Surface(
            (self.max_radius * 2, self.max_radius * 2),
            pygame.SRCALPHA
        )

        # Draw ripple circle
        color = (255, 255, 255, max(0, int(self.alpha)))
        pygame.draw.circle(
            ripple_surf,
            color,
            (self.max_radius, self.max_radius),
            int(self.radius),
            2  # Ring thickness
        )

        surface.blit(
            ripple_surf,
            (self.x - self.max_radius, self.y - self.max_radius)
        )