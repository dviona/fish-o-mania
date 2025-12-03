"""
Sand Layers Module for Fish-O-Mania.

This module contains the SandLayers class for terrain rendering.
"""

import pygame
import random
from constants import SCREEN_WIDTH, WATER_BOTTOM


class SandLayers:
    """
    Sand terrain layers at the bottom of the screen.

    Loads and tiles sand texture images horizontally across
    the screen bottom.

    Attributes:
        base_layers (list): Bottom sand layer images.
        top_layer (pygame.Surface): Top outline layer image.
    """

    def __init__(self, layer_files=None, use_terrain_files=False):
        """
        Initialize sand layers from image files.

        Args:
            layer_files (list): List of image file paths.
            use_terrain_files (bool): If True, auto-load terrain files.
        """
        self.base_layers = []
        self.top_layer = None

        if use_terrain_files and not layer_files:
            self._load_terrain_files()

    def _load_terrain_files(self):
        """Load the standard terrain sand files."""
        # Randomly choose a top variation
        top_variant = random.choice(
            ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        )

        # Base layer files (bottom to top)
        base_files = [
            "graphics/terrain_sand_d.png",
            "graphics/terrain_sand_c.png",
            "graphics/terrain_sand_b.png",
            "graphics/terrain_sand_a.png",
        ]

        # Load base layers
        for layer_file in base_files:
            try:
                layer_image = pygame.image.load(layer_file).convert_alpha()
                self.base_layers.append(layer_image)
                print(f"Loaded base sand layer: {layer_file}")
            except pygame.error as e:
                print(f"Error loading sand layer {layer_file}: {e}")

        # Load top outline layer
        top_outline_file = f"graphics/terrain_sand_top_{top_variant}_outline.png"
        try:
            self.top_layer = pygame.image.load(top_outline_file).convert_alpha()
            print(f"Loaded top sand layer: {top_outline_file}")
        except pygame.error as e:
            print(f"Error loading top sand layer: {e}")
            self.top_layer = None

    def draw(self, surface):
        """
        Draw the sand layers tiled across the screen.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        base_y = WATER_BOTTOM

        # Draw base layers (stacked vertically, tiled horizontally)
        for i, layer in enumerate(self.base_layers):
            if layer:
                tile_width = layer.get_width()
                num_tiles = (SCREEN_WIDTH // tile_width) + 2

                for tile_num in range(num_tiles):
                    x_pos = tile_num * tile_width
                    y_pos = base_y + (i * 10)
                    surface.blit(layer, (x_pos, y_pos))

        # Draw top outline layer
        if self.top_layer:
            tile_width = self.top_layer.get_width()
            num_tiles = (SCREEN_WIDTH // tile_width) + 2
            top_y = WATER_BOTTOM - 10

            for tile_num in range(num_tiles):
                x_pos = tile_num * tile_width
                surface.blit(self.top_layer, (x_pos, top_y))