"""
Background Package for Fish-O-Mania.

This package contains all background visual elements including animated
water effects (waves, ripples, bubbles), decorative elements (seaweed,
rocks), and terrain (sand layers).

Classes:
    Ripple: Expanding circle animation on water surface.
    Seaweed: Swaying underwater plant.
    Rock: Static decorative rock.
    Bubble: Rising bubble with wobble effect.
    Wave: Animated water surface wave.
    SandLayers: Tiled sand terrain at bottom.
    BackgroundManager: Coordinates all background elements.

Usage:
    from background import BackgroundManager

    # Create manager with terrain files
    bg_manager = BackgroundManager(use_terrain_files=True)

    # In game loop
    bg_manager.update()
    bg_manager.draw(screen)

    # Individual classes can also be imported
    from background import Ripple, Bubble, Wave
"""

from background.ripple import Ripple
from background.seaweed import Seaweed
from background.rock import Rock
from background.bubble import Bubble
from background.wave import Wave
from background.sand_layers import SandLayers
from background.background_manager import BackgroundManager

# Define what gets exported with "from background import *"
__all__ = [
    'Ripple',
    'Seaweed',
    'Rock',
    'Bubble',
    'Wave',
    'SandLayers',
    'BackgroundManager',
]