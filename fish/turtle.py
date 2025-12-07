"""
Turtle Fish Class for Fish-O-Mania.

The rarest and most valuable fish to catch.
"""

from fish.animated_fish import AnimatedFish


class Turtle(AnimatedFish):
    """Rare, valuable turtle."""

    def __init__(self, x, y, moving_right=True):
        speed = 0.5 if moving_right else -0.5

        super().__init__(
            sprite_sheet_path="graphics/turtle.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=x,
            y=y,
            speed_x=speed,
            fish_type="Turtle",
            death_animation_path="graphics/turtle_death.png"
        )
        self.value = 150
        self.rarity = "rare"
