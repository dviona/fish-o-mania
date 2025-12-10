# Tavish, Zac, Debbie
"""
This File Manages spawning, updating, and tracking all fish.
"""

import pygame
import random
from mechanics.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    MAX_FISH,
    SPAWN_DELAY,
    WATER_SURFACE,
    WATER_BOTTOM,
)
from mechanics.lives_manager import LivesManager
# Import the fish classes
from fish.turtle import Turtle
from fish.shark import Shark
from fish.octopus import Octopus
from fish.danger_fish import DangerFish


class FishManager:
    """
    Manages all fish in the game.
    Handles spawning, updating, and organizing fish into groups.
    """

    def __init__(self):
        # Sprite groups for different fish types
        self.all_fish = pygame.sprite.Group()
        self.danger_fish = pygame.sprite.Group()
        self.rare_fish = pygame.sprite.Group()
        self.large_fish = pygame.sprite.Group()

        # Death animations group
        self.death_animations = pygame.sprite.Group()

        # Sound effects - Good Catches
        self.catch_sound = pygame.mixer.Sound("sounds/bubble.mp3")
        self.catch_sound.set_volume(0.5)
        # Sound effects - Bad Catches
        self.penalty_sound = pygame.mixer.Sound("sounds/dead.mp3")
        self.penalty_sound.set_volume(0.5)

        # Lives manager
        self.lives_manager = LivesManager(
            max_lives=3,
            live_icon_path="graphics/fish_orange_outline.png",
            dead_icon_path="graphics/fish_orange_skeleton_outline.png",
        )

        # Red flash effect for penalty
        self.red_flash_timer = 0
        self.red_flash_duration = 30  # Frames (0.5 seconds at 60 FPS)

        # Recent catches (store animated sprites)
        # List of {type, value, frames, current_frame, frame_counter}
        self.recent_catches = []
        self.max_recent_catches = 3

        # Load fish sprite animations for display
        self.fish_animations = self._load_fish_animations()

        # Spawn timing
        self.spawn_timer = 0
        self.spawn_delay = SPAWN_DELAY

    def _load_fish_animations(self):
        """Load all frames of each fish type for animated display."""
        animations = {}
        fish_data = {
            "Turtle": {"path": "graphics/turtle.png", "frames": 6},
            "Danger Fish": {"path": "graphics/danger_fish.png", "frames": 6},
            "Shark": {"path": "graphics/shark.png", "frames": 6},
            "Octopus": {"path": "graphics/octopus.png", "frames": 6},
        }

        for fish_type, data in fish_data.items():
            try:
                # Load sprite sheet
                sprite_sheet = pygame.image.load(data["path"]).convert_alpha()
                frames = []

                # Extract all frames (48x48 each)
                for i in range(data["frames"]):
                    x = i * 48
                    frame = pygame.Surface((48, 48), pygame.SRCALPHA)
                    frame.blit(sprite_sheet, (0, 0), (x, 0, 48, 48))
                    # Scale to display size (64x64)
                    frame = pygame.transform.scale(frame, (64, 64))
                    frames.append(frame)

                animations[fish_type] = frames
                print(f"Loaded {len(frames)} frames for {fish_type}")
            except pygame.error as e:
                print(f"Error loading animation for {fish_type}: {e}")
                # Create placeholder
                placeholder = pygame.Surface((64, 64), pygame.SRCALPHA)
                pygame.draw.circle(placeholder, (100, 100, 100),
                                   (32, 32), 28)
                animations[fish_type] = [placeholder]

        return animations

    def spawn_fish(self, fish_class=None):
        """
        Spawn a new fish.

        Args:
            fish_class: Specific fish type to spawn, or None for random.
        """
        if fish_class is None:
            # Generate a random number to determine which fish to spawn
            random_num = random.random()
            # 30% chance for Danger Fish type
            if random_num < 0.3:
                fish_class = "danger"
            # 30% chance for Shark type
            elif random_num < 0.6:
                fish_class = "shark"
            # 25% chance for Octopus type
            elif random_num < 0.85:
                fish_class = "octopus"
            # 15% chance for Turtle Type
            else:
                fish_class = "turtle"

        # Determine a random position for the Fish to spawn
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(WATER_SURFACE + 20, WATER_BOTTOM - 20)

        # Create the appropriate fish type
        # (Turtle, Danger Fish, Shark, or Octopus)
        try:
            if fish_class == "turtle":
                fish = Turtle(x, y)
                self.rare_fish.add(fish)

            elif fish_class == "danger":
                fish = DangerFish(x, y)
                self.danger_fish.add(fish)

            elif fish_class == "shark":
                fish = Shark(x, y)
                self.danger_fish.add(fish)

            else:  # octopus
                fish = Octopus(x, y)
                self.large_fish.add(fish)

            self.all_fish.add(fish)
            return fish

        except pygame.error as e:
            print(f"Error spawning fish: {e}")
            return None

    def update(self):
        """Update all fish and handle auto-spawning."""
        self.all_fish.update()
        self.death_animations.update()

        # Update red flash timer
        if self.red_flash_timer > 0:
            self.red_flash_timer -= 1

        # Update recent catches animations
        for catch in self.recent_catches:
            catch["frame_counter"] += 1
            if catch["frame_counter"] >= catch["frame_delay"]:
                catch["frame_counter"] = 0
                # Get number of frames for this fish type
                if catch["type"] in self.fish_animations:
                    num_frames = len(self.fish_animations[catch["type"]])
                    catch["current_frame"] = (
                            (catch["current_frame"] + 1) % num_frames)

        # Auto-spawn fish
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            if len(self.all_fish) < MAX_FISH:
                self.spawn_fish()

    def draw(self, surface):
        """Draw all fish, death animations, lives display,
                and recent catches to the screen."""
        self.all_fish.draw(surface)
        self.death_animations.draw(surface)

        # Draw lives display in top-right corner
        # Calculate position:
        # screen_width - (3 lives * 70 spacing) - 10 padding
        lives_x = SCREEN_WIDTH - (self.lives_manager.max_lives * 70) - 10
        self.lives_manager.draw(surface, x=lives_x, y=10)

        # Draw recent catches below lives (aligned with same spacing)
        self.draw_recent_catches(surface, lives_x)

    def draw_recent_catches(self, surface, start_x):
        """Draw recent catches as animated sprites
                    with values below lives display"""
        if not self.recent_catches:
            return

        # Position below the lives (lives are at y=10 with 64px height)
        start_y = 84  # 10 (lives y) + 64 (icon height) + 10 (gap)

        # Use same spacing as lives (70px)
        spacing = 70

        # Create font for values
        font = pygame.font.Font(None, 24)

        for i, catch in enumerate(self.recent_catches):
            x_pos = start_x + (i * spacing)

            # Draw animated fish sprite
            if catch["type"] in self.fish_animations:
                frames = self.fish_animations[catch["type"]]
                current_frame = catch["current_frame"]
                if current_frame < len(frames):
                    sprite = frames[current_frame]
                    surface.blit(sprite, (x_pos, start_y))

            # Draw value below sprite (centered under the icon)
            value_text = font.render(f"+{catch['value']}",
                                     True, (255, 215, 0))
            value_rect = value_text.get_rect(center=(x_pos + 32, start_y + 72))
            surface.blit(value_text, value_rect)

    def draw_red_flash(self, surface):
        """Draw red flash overlay when penalty occurs."""
        if self.red_flash_timer > 0:
            # Create red overlay with fading alpha
            alpha = int((self.red_flash_timer / self.red_flash_duration) * 100)
            red_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            red_overlay.set_alpha(alpha)
            red_overlay.fill((255, 0, 0))
            surface.blit(red_overlay, (0, 0))

    def get_fish_at_position(self, pos):
        """
        Get fish at a specific position (for catching).
        Skips fish that are already hooked, caught, recently released,
        or have death animation created.

        Args:
            pos: (x, y) tuple of position to check

        Returns:
            Fish sprite at that position, or None
        """
        for fish in self.all_fish:
            # Skip fish that are already processed
            if getattr(fish, 'is_hooked', False):
                continue
            if getattr(fish, 'is_caught', False):
                continue
            if getattr(fish, 'caught', False):
                continue
            if getattr(fish, 'death_animation_created', False):
                continue
            # Skip recently released fish
            if getattr(fish, 'recently_released', False):
                if not fish.is_release_cooldown_over():
                    continue
            if fish.rect.collidepoint(pos):
                return fish
        return None

    def remove_fish(self, fish):
        """
        Remove a caught fish and create its death animation.
        For non-danger fish only. Danger fish are handled by casting module.

        Args:
            fish: The fish sprite that was caught.

        Returns:
            dict: Information about the caught fish and game state.
        """
        # Check if already processed
        if getattr(fish, 'death_animation_created', False):
            return {
                "type": fish.fish_type,
                "value": 0,
                "rarity": fish.rarity,
                "penalty": False,
                "game_over": self.lives_manager.is_game_over(),
            }

        # Mark fish as caught
        fish.is_caught = True
        fish.caught = True

        # Get fish info before removing
        info = fish.get_info()

        print(f"Caught: {info['type']} (+{info['value']} points)")
        self.catch_sound.play()

        # Add to recent catches with animation data
        catch_data = {
            "type": info["type"],
            "value": info["value"],
            "rarity": info["rarity"],
            "current_frame": 0,
            "frame_counter": 0,
            "frame_delay": 8,  # Frames to wait before advancing animation
        }
        self.recent_catches.append(catch_data)

        # Keep only last 3 catches
        if len(self.recent_catches) > self.max_recent_catches:
            self.recent_catches.pop(0)

        # Create death animation before removing fish
        death_anim = fish.create_death_animation()
        if death_anim:
            self.death_animations.add(death_anim)

        # Remove fish from all groups
        fish.kill()

        # Return info with penalty flag and game over status
        return {
            **info,
            "penalty": False,
            "game_over": self.lives_manager.is_game_over(),
        }

    def get_stats(self):
        """Get statistics about current fish and game state."""
        return {
            "total": len(self.all_fish),
            "danger": len(self.danger_fish),
            "rare": len(self.rare_fish),
            "large": len(self.large_fish),
            "lives": self.lives_manager.get_current_lives(),
            "game_over": self.lives_manager.is_game_over(),
        }

    def clear_all(self):
        """Remove all fish (useful for restarting)."""
        self.all_fish.empty()
        self.danger_fish.empty()
        self.rare_fish.empty()
        self.large_fish.empty()
        self.death_animations.empty()
        self.lives_manager.reset()
        self.recent_catches = []  # Clear recent catches on restart
