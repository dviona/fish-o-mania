import pygame

class CastingRod:
    def __init__(self, rod_max_length, rod_speed):
        self.rod_max_length = rod_max_length
        self.rod_speed = rod_speed
        self.rod_length = 0
        self.is_casting = False

    def toggle_cast(self):
        # Toggle the casting state
        self.is_casting = not self.is_casting

    def update(self, hook_rect, fish_manager, bubble_sound):
        # Update the rod length based on casting state
        
        # Casting downward
        if self.is_casting:
            if self.rod_length < self.rod_max_length:
                self.rod_length += self.rod_speed
            else:
                self.is_casting = False  # Auto-switch to reel-up

        # Reeling upward
        else:
            if self.rod_length > 0:
                # Check fish collision
                fish = fish_manager.get_fish_at_position(
                    (hook_rect.centerx, hook_rect.bottom)
                )

                if fish:
                    bubble_sound.play()
                    info = fish.get_info()
                    fish_manager.remove_fish(fish)
                    self.is_casting = False
                    return info  # Return caught fish

                self.rod_length -= self.rod_speed

        return None
