"""
Danger Fish Class for Fish-O-Mania.

The fish to avoid! Catching this costs a life.
"""

from fish.animated_fish import AnimatedFish


class DangerFish(AnimatedFish):
    """Danger fish - lose a life if caught."""

    def __init__(self, x, y, moving_right=True):
        speed = 0.7 if moving_right else -0.7

        super().__init__(
            sprite_sheet_path="graphics/danger_fish.png",
            frame_width=48,
            frame_height=48,
            num_frames=6,
            x=x,
            y=y,
            speed_x=speed,
            fish_type="Danger Fish",
            death_animation_path="graphics/danger_fish_death.png"
        )
        self.value = 25
        self.rarity = "danger"
