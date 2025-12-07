"""
Constants Module for Fish-O-Mania.

This module contains all game configuration constants including screen settings,
colors, water boundaries, and gameplay parameters. Centralizing these values
allows for easy tuning and maintains consistency across all game modules.

Usage:
    from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
"""

# SCREEN SETTINGS

SCREEN_WIDTH = 1200  # Game window width in pixels
SCREEN_HEIGHT = 800  # Game window height in pixels
FPS = 60  # Target frames per second

# COLOR DEFINITIONS (RGB tuples)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (70, 130, 180)  # Sky background color
AZURE = (240, 255, 255)  # Light water color (near surface)
DEEP_BLUE = (0, 105, 148)  # Dark water color (near bottom)
LIGHT_PINK = (255, 182, 193)  # UI accent color
DEEP_PINK = (255, 182, 211)  # UI accent color

# WATER BOUNDARIES

WATER_SURFACE = 200  # Y-coordinate where water surface begins
WATER_BOTTOM = SCREEN_HEIGHT - 50  # Y-coordinate where water bottom is

# FISH SPAWNING SETTINGS

MAX_FISH = 15  # Maximum number of fish allowed in water at once
SPAWN_DELAY = 120  # Frames between automatic fish spawns (2 seconds at 60 FPS)
START_FISHES = 5  # Number of fish spawned at game start

# BOAT AND FISHING ROD SETTINGS

BOAT_SPEED = 8  # Horizontal movement speed of the boat (pixels per frame)
ROD_MAX_LENGTH = 500  # Maximum depth the fishing line can extend (pixels)
ROD_SPEED = 6  # Speed of casting/reeling the fishing line (pixels per frame)

# Legacy lowercase aliases (deprecated, use uppercase versions above)
# rod_max_length = 500
# boat_speed = 8
# rod_length = 0
# rod_speed = 6
