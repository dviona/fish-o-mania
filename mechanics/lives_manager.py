"""
Tavish, Debbie

This file manages the player's lives system.
"""

import pygame


class LivesManager:
    """Manages player lives and displays them."""

    def __init__(self, max_lives=3,
                 live_icon_path="graphics/fish_orange_outline.png",
                 dead_icon_path="graphics/fish_orange_skeleton_outline.png"):
        """
        Initialize the lives_manager.

        Args:
            max_lives: Maximum number of lives (default 3)
            live_icon_path: Path to the icon for active lives
            dead_icon_path: Path to the icon for lost lives
        """
        self.max_lives = max_lives
        self.current_lives = max_lives
        self.game_over = False
        self.icon_size = 64  # Standard size for all icons

        # Load life icons
        try:
            self.live_icon = pygame.image.load(live_icon_path).convert_alpha()
            # Scale icons to standard size (64x64)
            self.live_icon = (
                pygame.transform.scale(self.live_icon,
                                       (self.icon_size, self.icon_size)))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading live icon: {e}")
            # Create a placeholder green circle
            self.live_icon = pygame.Surface(
                (self.icon_size, self.icon_size), pygame.SRCALPHA)
            pygame.draw.circle(self.live_icon,
                               (0, 255, 0),
                               (self.icon_size//2, self.icon_size//2), 28)

        try:
            self.dead_icon = pygame.image.load(dead_icon_path).convert_alpha()
            self.dead_icon = (
                pygame.transform.scale(self.dead_icon,
                                       (self.icon_size, self.icon_size)))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading dead icon: {e}")
            # Create a placeholder red circle
            self.dead_icon = pygame.Surface(
                (self.icon_size, self.icon_size), pygame.SRCALPHA)
            pygame.draw.circle(self.dead_icon, (255, 0, 0),
                               (self.icon_size//2, self.icon_size//2), 28)

    def lose_life(self):
        """
        Decrease lives by 1.

        Returns:
            bool: True if still alive, False if game over
        """
        if self.current_lives > 0:
            self.current_lives -= 1
            print(f"Life lost! Remaining lives: {self.current_lives}")

            if self.current_lives <= 0:
                self.game_over = True
                return False
        return True

    def reset(self):
        """Reset lives to maximum."""
        self.current_lives = self.max_lives
        self.game_over = False

    def is_game_over(self):
        """Check if game is over."""
        return self.game_over

    def get_current_lives(self):
        """Get current number of lives."""
        return self.current_lives

    def draw(self, surface, x=10, y=10):
        """
        Draw the lives display on screen.

        Args:
            surface: Pygame surface to draw on
            x: X position for the lives display
            y: Y position for the lives display
        """
        spacing = 70  # Space between icons (64px icon + 6px gap)

        # Draw all life icons
        for i in range(self.max_lives):
            icon_x = x + (i * spacing)

            if i < self.current_lives:
                # Draw active life icon
                surface.blit(self.live_icon, (icon_x, y))
            else:
                # Draw dead/lost life icon
                surface.blit(self.dead_icon, (icon_x, y))
