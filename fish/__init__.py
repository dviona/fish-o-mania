"""
Fish Package for Fish-O-Mania.

This package contains fish classes and fish management.

Classes:
    DeathAnimation: Animation when a fish is caught.
    AnimatedFish: Base class for all fish.
    Turtle: Rare, slow-moving, high-value fish.
    DangerFish: Causes life loss when caught.
    Shark: Fast-moving, medium-value fish.
    Octopus: Slow-moving, high-value fish.
    FishManager: Manages all fish in the game.

Usage:
    from fish import FishManager, Turtle, Shark
"""

from fish.fish import (
    DeathAnimation,
    AnimatedFish,
    Turtle,
    DangerFish,
    Shark,
    Octopus
)
from fish.fish_manager import FishManager
from fish.relaxed_fish_manager import RelaxedFishManager
from fish.fast_fish_manager import FastFishManager

__all__ = [
    'DeathAnimation',
    'AnimatedFish',
    'Turtle',
    'DangerFish',
    'Shark',
    'Octopus',
    'FishManager',
]