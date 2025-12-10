"""
Tavish, Debbie

Shark Fish Class for Fish-O-Mania.

Fast-moving fish, harder to catch but worth good points.
"""

from fish.animated_fish import AnimatedFish


class Shark(AnimatedFish):
    """Fast-moving shark, harder to catch."""

    def __init__(self, x, y, moving_right=True):
        speed = 0.75 if moving_right else -0.75

        super().__init__(
            sprite_sheet_path="graphics/shark.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=x,
            y=y,
            speed_x=speed,
            fish_type="Shark",
            death_animation_path="graphics/shark_death.png"
        )
        self.value = 75
        self.rarity = "uncommon"
