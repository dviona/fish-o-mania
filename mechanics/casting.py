"""
Casting Module for Fish-O-Mania.

This module handles the fishing rod casting and reeling mechanics,
including the state machine for cast/reel cycles and fish collision
detection during reeling.

Classes:
    CastingRod: Manages the fishing rod state and behavior.
"""

import pygame


class CastingRod:
    """
    Manages fishing rod casting and reeling mechanics.

    The rod operates as a simple state machine:
    1. IDLE: Rod at rest, waiting for cast
    2. CASTING: Rod extending downward
    3. REELING: Rod retracting upward, checking for fish

    Additionally handles danger fish mechanics:
    - When a danger fish is hooked, it enters a pending state
    - Player must scream to release it, or it gets caught with penalty

    Attributes:
        rod_max_length (int): Maximum extension distance in pixels.
        rod_speed (int): Extension/retraction speed in pixels per frame.
        rod_length (int): Current extension distance.
        is_casting (bool): True if rod is extending, False if reeling.
        attached_fish: Reference to currently hooked fish.
        pending_danger_fish: Danger fish waiting for scream resolution.
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

        # Danger fish handling
        self.attached_fish = None
        self.pending_danger_fish = None

        # Catch cooldown (prevents immediate re-catch after release)
        self.catch_cooldown_end_time = 0
        self.CATCH_COOLDOWN_DURATION = 2000  # 2 seconds cooldown

    def is_on_cooldown(self):
        """
        Check if the hook is still on catch cooldown.

        Returns:
            bool: True if cooldown is active, False otherwise.
        """
        return pygame.time.get_ticks() < self.catch_cooldown_end_time

    def start_cooldown(self):
        """Start the catch cooldown period."""
        self.catch_cooldown_end_time = pygame.time.get_ticks() + self.CATCH_COOLDOWN_DURATION

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
                  For danger fish, includes 'penalty': True and 'fish_ref'.
        """
        # Don't process new catches while danger fish is pending
        if self.pending_danger_fish is not None:
            return None

        if self.is_casting:
            # Extend the rod downward
            if self.rod_length < self.rod_max_length:
                self.rod_length += self.rod_speed

        else:
            # Reel the rod upward
            if self.rod_length > 0:
                # Check for fish collision (only if not on cooldown)
                if not self.is_on_cooldown():
                    hook_position = (hook_rect.centerx, hook_rect.bottom)
                    fish = fish_manager.get_fish_at_position(hook_position)

                    if fish:
                        is_danger = getattr(fish, 'fish_type', '') == 'Danger Fish'

                        if is_danger:
                            # Hook the danger fish - enters pending state
                            fish.is_hooked = True

                            self.pending_danger_fish = fish
                            self.attached_fish = fish
                            fish_manager.penalty_sound.play()
                            fish_manager.red_flash_timer = fish_manager.red_flash_duration

                            return {
                                "type": fish.fish_type,
                                "value": fish.value,
                                "rarity": fish.rarity,
                                "penalty": True,
                                "game_over": fish_manager.lives_manager.is_game_over(),
                                "fish_ref": fish
                            }
                        else:
                            # Normal fish - catch immediately
                            result = fish_manager.remove_fish(fish)
                            self.is_casting = False
                            return result

                self.rod_length -= self.rod_speed

        return None

    def catch_danger_fish(self, fish_manager):
        """
        Complete the catch of a danger fish (called when scream fails).

        The fish is caught, points are awarded, but a life is lost.

        Args:
            fish_manager (FishManager): Manager to handle fish removal.

        Returns:
            dict: Fish info with type, value, rarity, or None if no pending fish.
        """
        if self.pending_danger_fish is not None:
            fish = self.pending_danger_fish
            fish_value = getattr(fish, 'value', 25)
            fish_type = getattr(fish, 'fish_type', 'Danger Fish')
            fish_rarity = getattr(fish, 'rarity', 'danger')

            # Mark fish as caught
            fish.is_hooked = False
            fish.is_caught = True
            fish.caught = True

            # Create death animation
            death_anim = fish.create_death_animation()
            if death_anim:
                fish_manager.death_animations.add(death_anim)

            # Remove from sprite groups
            fish.kill()

            # Add to recent catches display
            catch_data = {
                "type": fish_type,
                "value": fish_value,
                "rarity": fish_rarity,
                "current_frame": 0,
                "frame_counter": 0,
                "frame_delay": 8,
            }
            fish_manager.recent_catches.append(catch_data)
            if len(fish_manager.recent_catches) > fish_manager.max_recent_catches:
                fish_manager.recent_catches.pop(0)

            # Clear pending state
            self.pending_danger_fish = None
            self.attached_fish = None

            # Start cooldown to prevent immediate re-catch
            self.start_cooldown()

            return {
                "type": fish_type,
                "value": fish_value,
                "rarity": fish_rarity
            }
        return None

    def release_danger_fish(self):
        """
        Release the danger fish (called when scream succeeds).

        Fish swims away, no points awarded, no life lost.
        Marks the fish as recently released so it can't be immediately re-caught.
        """
        if self.pending_danger_fish is not None:
            # Clear hooked flag
            self.pending_danger_fish.is_hooked = False

            # Mark fish as recently released - it can't be caught again for a while
            self.pending_danger_fish.recently_released = True
            self.pending_danger_fish.release_time = pygame.time.get_ticks()

            # Clear pending state
            self.pending_danger_fish = None
            self.attached_fish = None

            # Start cooldown for the hook
            self.start_cooldown()

    def reset(self):
        """Reset the rod to its initial state."""
        self.rod_length = 0
        self.is_casting = False
        self.attached_fish = None
        self.pending_danger_fish = None
        self.catch_cooldown_end_time = 0
