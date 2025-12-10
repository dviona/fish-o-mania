"""
Tavish, Debbie

Octopus Fish Class for Fish-O-Mania.

Large, slow-moving creature worth good points.
"""

from fish.animated_fish import AnimatedFish


class Octopus(AnimatedFish):
    """Large, slow-moving octopus."""

    def __init__(self, x, y, moving_right=True):
        speed = 0.5 if moving_right else -0.5

        super().__init__(
            sprite_sheet_path="graphics/octopus.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=x,
            y=y,
            speed_x=speed,
            fish_type="Octopus",
            death_animation_path="graphics/octopus_death.png"
        )
        self.value = 100
        self.rarity = "uncommon"
