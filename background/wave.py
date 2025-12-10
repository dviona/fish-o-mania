# Tavish, Debbie, Zac, Aradhya
"""
Wave Module

This module contains the Wave class for animated water waves
"""

import pygame
import math
from mechanics.constants import SCREEN_WIDTH, WATER_SURFACE, WHITE


class Wave:
    """
    Animated water surface wave simulation

    Uses multiple overlapping sine waves to create an animated
    water surface

    Attributes:
        time (float): Animation time counter
        y_position (int): y-coordinate of the wave line
        layers (list): Configuration for multiple wave layers
    """

    def __init__(self):
        """Initialize the wave with multiple layers"""
        self.time = 0
        self.wave_speed = 0.05
        self.y_position = WATER_SURFACE

        # Multiple wave layers for depth effect
        self.layers = [
            {
                'speed': 0.05,
                'amplitude': 8,
                'frequency': 0.02,
                'offset': 0
            },
            {
                'speed': 0.03,
                'amplitude': 5,
                'frequency': 0.015,
                'offset': math.pi
            },
            {
                'speed': 0.02,
                'amplitude': 8,
                'frequency': 0.01,
                'offset': 1.1 * math.pi / 2
            },
        ]

    def update(self):
        """Update wave animation"""
        self.time += self.wave_speed

    def get_wave_points(self, layer_index=0):
        """
        Generate points for a wave curve

        Args:
            layer_index (int): Which wave layer to generate

        Returns:
            list: List of (x, y) tuples forming the wave
        """
        layer = self.layers[layer_index]
        points = []

        # Sample points across screen width
        for x in range(0, SCREEN_WIDTH + 1, 5):
            y = self.y_position + math.sin(
                x * layer['frequency'] +
                self.time * layer['speed'] +
                layer['offset']
            ) * layer['amplitude']
            points.append((x, y))

        return points

    def draw(self, surface):
        """
        Draw the animated waves

        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Draw primary wave
        main_points = self.get_wave_points(0)
        if len(main_points) > 1:
            pygame.draw.lines(surface, WHITE, False, main_points, 3)

        # Draw secondary wave for depth effect
        if len(self.layers) > 1:
            secondary_points = self.get_wave_points(1)
            if len(secondary_points) > 1:
                pygame.draw.lines(
                    surface,
                    (200, 230, 255),  # Lighter blue
                    False,
                    secondary_points,
                    2
                )
