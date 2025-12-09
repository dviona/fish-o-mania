"""
Fast Fish Manager Module for Fish-O-Mania

This module contains the FastFishManager class, a variant of RelaxedFishManager
with faster-moving fish. Used by Time Attack mode
"""

from fish.relaxed_fish_manager import RelaxedFishManager

# Fish move 3x faster than normal
FISH_SPEED_MULTIPLIER = 3.0


class FastFishManager(RelaxedFishManager):
    """
    Fish manager variant with faster-moving fish

    Extends RelaxedFishManager to get no-lives behavior,
    then increases fish movement speed for time attack mode
    """

    def spawn_fish(self, fish_class=None):
        """
        Spawn a fish with increased movement speed

        Args:
            fish_class (str): Specific fish type, or None for random

        Returns:
            AnimatedFish: The spawned fish with boosted speed
        """
        fish = super().spawn_fish(fish_class)
        if fish:
            fish.speed_x *= FISH_SPEED_MULTIPLIER
            fish.speed_y *= FISH_SPEED_MULTIPLIER
        return fish
