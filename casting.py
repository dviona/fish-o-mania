"""
Casting Module for Fish-O-Mania.

This module handles the fishing rod casting and reeling mechanics,
including the state machine for cast/reel cycles and fish collision
detection during reeling.

Classes:
    CastingRod: Manages the fishing rod state and behavior.
"""


class CastingRod:
    """
    Manages fishing rod casting and reeling mechanics.

    The rod operates as a simple state machine:
    1. IDLE: Rod at rest, waiting for cast
    2. CASTING: Rod extending downward
    3. REELING: Rod retracting upward, checking for fish

    Attributes:
        rod_max_length (int): Maximum extension distance in pixels.
        rod_speed (int): Extension/retraction speed in pixels per frame.
        rod_length (int): Current extension distance.
        is_casting (bool): True if rod is extending, False if reeling.
    """

    def __init__(self, rod_max_length, rod_speed):
        """
        Initialize the casting rod.

        Args:
            rod_max_length (int): Maximum depth the rod can extend.
            rod_speed (int): Speed of casting and reeling.
        """
        self.rod_max_length = rod_max_length
        self.rod_speed = rod_speed
        self.rod_length = 0
        self.is_casting = False

    def toggle_cast(self):
        """Toggle between casting and reeling states."""
        self.is_casting = not self.is_casting

    def update(self, hook_rect, fish_manager, bubble_sound):
        """
        Update the rod state and check for fish catches.

        Args:
            hook_rect (pygame.Rect): Rectangle representing the hook position.
            fish_manager (FishManager): Manager to check for fish collisions.
            bubble_sound: Sound effect for catching (unused, kept for API).

        Returns:
            dict: Caught fish information, or None if no catch.
        """
        if self.is_casting:
            # Extend the rod downward
            if self.rod_length < self.rod_max_length:
                self.rod_length += self.rod_speed
            else:
                # Auto-switch to reeling when max length reached
                self.is_casting = False
        else:
            # Reel the rod upward
            if self.rod_length > 0:
                # Check for fish collision at hook position
                hook_position = (hook_rect.centerx, hook_rect.bottom)
                fish = fish_manager.get_fish_at_position(hook_position)

                if fish:
                    # Catch the fish
                    result = fish_manager.remove_fish(fish)
                    self.is_casting = False
                    return result

                self.rod_length -= self.rod_speed

        return None

    def reset(self):
        """Reset the rod to its initial state."""
        self.rod_length = 0
        self.is_casting = False