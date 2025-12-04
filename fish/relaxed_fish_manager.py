"""
Relaxed Fish Manager Module for Fish-O-Mania.

This module contains the RelaxedFishManager class, a variant of FishManager
without life penalties. Used by game modes that don't need the lives system.
"""

from mechanics.constants import SCREEN_WIDTH
from fish.fish_manager import FishManager


class RelaxedFishManager(FishManager):
    """
    Fish manager variant without life penalties.

    All fish can be caught without consequence, making for a
    relaxed, stress-free fishing experience. Used by Endless Mode
    and Time Attack Mode.
    """

    def remove_fish(self, fish):
        """
        Remove a caught fish without any penalties.

        Unlike the standard FishManager, catching danger fish
        does not cost lives or trigger game over.

        Args:
            fish: The fish sprite that was caught.

        Returns:
            dict: Fish information with penalty=False, game_over=False.
        """
        info = fish.get_info()

        # Play catch sound for all fish
        self.catch_sound.play()

        # Add to recent catches display
        catch_data = {
            'type': info['type'],
            'value': info['value'],
            'rarity': info['rarity'],
            'current_frame': 0,
            'frame_counter': 0,
            'frame_delay': 8
        }
        self.recent_catches.append(catch_data)
        if len(self.recent_catches) > self.max_recent_catches:
            self.recent_catches.pop(0)

        # Create death animation
        death_anim = fish.create_death_animation()
        if death_anim:
            self.death_animations.add(death_anim)

        fish.kill()

        # Return info - never any penalty or game over
        return {
            **info,
            'penalty': False,
            'game_over': False
        }

    def draw(self, surface):
        """
        Draw fish without lives display.

        Overrides parent to skip drawing the lives UI since
        modes using this manager don't use the lives system.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        self.all_fish.draw(surface)
        self.death_animations.draw(surface)
        self.draw_recent_catches(surface, SCREEN_WIDTH - 220)
