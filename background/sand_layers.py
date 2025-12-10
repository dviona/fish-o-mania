# Tavish, Debbie, Zac, Aradhya
"""
Sand Layers Module for Fish-O-Mania

This module contains the SandLayers class for terrain rendering
"""

import pygame
from mechanics.constants import SCREEN_WIDTH, WATER_BOTTOM

# Configuration
LAYER_VERTICAL_OFFSET = 10
TOP_OUTLINE_FILENAME = "terrain_sand_top_b_outline.png"
DEFAULT_TERRAIN_DIR = "graphics"
BASE_LAYER_FILES = [
    "terrain_sand_d.png",
    "terrain_sand_c.png",
    "terrain_sand_b.png",
    "terrain_sand_a.png",
]


class SandLayers:
    """
    Sand terrain layers at the bottom of the screen

    Loads and tiles sand texture images horizontally across
    the screen bottom

    Attributes:
        base_layers (list): Bottom sand layer images
        top_layer (pygame.Surface): Top outline layer image
    """

    def __init__(self, directory=None, use_terrain_files=True):
        """
        Initialize sand layers from image files

        Args:
            directory (str): Directory path containing sand layer PNGs
            use_terrain_files (bool): If True, auto-load default terrain files
        """
        self.base_layers = []
        self.top_layer = None
        self.top_layer_width = 0

        if directory:
            self._load_from_directory(directory)
        elif use_terrain_files:
            self._load_terrain_files()

        # Cache layer widths for performance
        self.layer_widths = [
            layer.get_width() for layer in self.base_layers
        ]

    def _load_from_directory(self, directory):
        """
        Load all sand layer PNGs from a directory

        Args:
            directory (str): Path to directory containing PNG files
        """
        for filename in BASE_LAYER_FILES:
            filepath = f"{directory}/{filename}"
            try:
                layer = pygame.image.load(filepath).convert_alpha()
                self.base_layers.append(layer)
            except (pygame.error, FileNotFoundError) as e:
                print(f"Error loading layer {filepath}: {e}")

        # Load top outline
        top_filepath = f"{directory}/{TOP_OUTLINE_FILENAME}"
        try:
            self.top_layer = pygame.image.load(top_filepath).convert_alpha()
            self.top_layer_width = self.top_layer.get_width()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading top layer {top_filepath}: {e}")

    def _load_terrain_files(self):
        """Load the standard terrain sand files."""
        self._load_from_directory(DEFAULT_TERRAIN_DIR)

    def draw(self, surface):
        """
        Draw the sand layers tiled across the screen

        Args:
            surface (pygame.Surface): Surface to draw on
        """
        base_y = WATER_BOTTOM

        # Draw base layers (stacked vertically, tiled horizontally)
        for i, layer in enumerate(self.base_layers):
            tile_width = self.layer_widths[i]
            num_tiles = (SCREEN_WIDTH // tile_width) + 2
            y_pos = base_y + (i * LAYER_VERTICAL_OFFSET)

            for tile_num in range(num_tiles):
                x_pos = tile_num * tile_width
                surface.blit(layer, (x_pos, y_pos))

        # Draw top outline layer
        if self.top_layer:
            num_tiles = (SCREEN_WIDTH // self.top_layer_width) + 2
            top_y = WATER_BOTTOM - LAYER_VERTICAL_OFFSET

            for tile_num in range(num_tiles):
                x_pos = tile_num * self.top_layer_width
                surface.blit(self.top_layer, (x_pos, top_y))
