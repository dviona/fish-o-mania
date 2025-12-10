# Tavish, Debbie, Zac
"""
Background Manager Module for Fish-O-Mania

This module contains the BackgroundManager class for background elements
"""

import random
from mechanics.constants import SCREEN_WIDTH, WATER_SURFACE, WATER_BOTTOM
from background.ripple import Ripple
from background.seaweed import Seaweed
from background.rock import Rock
from background.bubble import Bubble
from background.wave import Wave
from background.sand_layers import SandLayers


class BackgroundManager:
    """
    Manages all background elements

    Coordinates updating and drawing of all background elements

    Attributes:
        ripples (list): Active ripple animations
        seaweeds (list): Seaweed decorations
        rocks (list): Rock decorations
        bubbles (list): Active bubble animations
        wave (Wave): Water surface wave
        sand (SandLayers): Sand terrain
    """

    def __init__(self, sand_layer_files=None, use_terrain_files=True):
        """
        Initialize the background manager

        Args:
            sand_layer_files (list): sand layer image paths
            use_terrain_files (bool): If True, load default terrain files
        """
        self.ripples = []
        self.seaweeds = []
        self.rocks = []
        self.bubbles = []
        self.wave = Wave()
        self.sand = SandLayers(sand_layer_files, use_terrain_files)

        # Generate static decorations
        self._generate_seaweed()
        self._generate_rocks()

        # Timers for spawning dynamic elements
        self.ripple_timer = 0
        self.bubble_timer = 0

    def _generate_seaweed(self):
        """Generate seaweed plants at random positions"""
        num_seaweed = random.randint(8, 12)
        for _ in range(num_seaweed):
            x = random.randint(0, SCREEN_WIDTH)
            self.seaweeds.append(Seaweed(x))

    def _generate_rocks(self):
        """Generate rocks at random positions near the bottom"""
        num_rocks = random.randint(5, 10)
        for _ in range(num_rocks):
            x = random.randint(0, SCREEN_WIDTH - 80)
            y = WATER_BOTTOM - random.randint(0, 40)
            self.rocks.append(Rock(x, y))

    def add_ripple(self, x, y):
        """
        Add a ripple at a specific position

        Args:
            x (float): X-coordinate for ripple
            y (float): Y-coordinate for ripple
        """
        self.ripples.append(Ripple(x, y))

    def update(self):
        """Update all background elements"""
        # Update wave animation
        self.wave.update()

        # Update and clean up ripples
        self.ripples = [r for r in self.ripples if r.alive]
        for ripple in self.ripples:
            ripple.update()

        # Spawn random surface ripples
        self.ripple_timer += 1
        if self.ripple_timer > random.randint(30, 90):
            self.ripple_timer = 0
            x = random.randint(50, SCREEN_WIDTH - 50)
            self.add_ripple(x, WATER_SURFACE + 10)

        # Update seaweed animation
        for seaweed in self.seaweeds:
            seaweed.update()

        # Update and clean up bubbles
        self.bubbles = [b for b in self.bubbles if b.alive]
        for bubble in self.bubbles:
            bubble.update()

        # Spawn random bubbles
        self.bubble_timer += 1
        if self.bubble_timer > random.randint(20, 60):
            self.bubble_timer = 0
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(WATER_SURFACE + 50, WATER_BOTTOM - 20)
            self.bubbles.append(Bubble(x, y))

    def draw(self, surface):
        """
        Draw all background elements in proper z-order

        Args:
            surface (pygame.Surface): Surface to draw on
        """
        # Bottom layer: sand
        self.sand.draw(surface)

        # Rocks on top of sand
        for rock in self.rocks:
            rock.draw(surface)

        # Seaweed
        for seaweed in self.seaweeds:
            seaweed.draw(surface)

        # Bubbles
        for bubble in self.bubbles:
            bubble.draw(surface)

        # Water surface wave
        self.wave.draw(surface)

        # Top layer: ripples
        for ripple in self.ripples:
            ripple.draw(surface)
