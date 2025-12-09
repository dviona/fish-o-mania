"""
Danger Fish Class for Fish-O-Mania.

Angler/Danger fish - Catching this costs a life in classic mode
In other modes, we can catch this as a normal fish
"""

from fish.animated_fish import AnimatedFish


class DangerFish(AnimatedFish):
    """Danger fish(Angler Fish) - lose a life if caught in classic mode"""

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
