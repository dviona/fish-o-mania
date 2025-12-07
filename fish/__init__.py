"""
Fish Module for Fish-O-Mania.

Contains all fish-related classes including the base AnimatedFish,
DeathAnimation, specific fish types, and fish managers.
"""

from fish.death_animation import DeathAnimation
from fish.animated_fish import AnimatedFish
from fish.turtle import Turtle
from fish.shark import Shark
from fish.octopus import Octopus
from fish.danger_fish import DangerFish
from fish.fish_manager import FishManager
from fish.relaxed_fish_manager import RelaxedFishManager
from fish.fast_fish_manager import FastFishManager