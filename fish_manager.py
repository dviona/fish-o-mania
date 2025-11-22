"""
This File Manages spawning, updating, and tracking all fish.
"""

import pygame
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, MAX_FISH, SPAWN_DELAY
# Import the fish classes from fish.py
from fish import GoldenTrout, CommonFish, FastFish, LargeFish


class FishManager:
    """
    Manages all fish in the game.
    Handles spawning, updating, and organizing fish into groups.
    """
    
    def __init__(self):
        # Sprite groups for different fish types
        self.all_fish = pygame.sprite.Group()
        self.common_fish = pygame.sprite.Group()
        self.rare_fish = pygame.sprite.Group()
        self.large_fish = pygame.sprite.Group()
        
        # Spawn timing
        self.spawn_timer = 0
        self.spawn_delay = SPAWN_DELAY
    
    def spawn_fish(self, fish_class=None):
        """
        Spawn a new fish.
        Args:
            fish_class: Specific fish type to spawn, or None for random
        """
        if fish_class is None:
            # Generate a random number to determine which fish to spawn
            random_num = random.random()
            # 50% chance for Common Fish type
            if random_num < 0.5:
                fish_class = "common"
            # 30% chance for Fast fish type
            elif random_num < 0.8:
                fish_class = "fast"
            # 15% chance for Large Fish type
            elif random_num < 0.95:
                fish_class = "large"
            # 5% chance for Golden Fish Type
            else:
                fish_class = "golden"
        
        # Determine a random position for the Fish to spawn
        x = random.randint(-50, SCREEN_WIDTH + 50)
        y = random.randint(100, SCREEN_HEIGHT - 50)

        # Create the appropriate fish type (Golden, Common, Fast, or Large)
        try:
            if fish_class == "golden":
                fish = GoldenTrout(x, y)
                self.rare_fish.add(fish)
                
            elif fish_class == "common":
                fish = CommonFish(x, y)
                self.common_fish.add(fish)
                
            elif fish_class == "fast":
                fish = FastFish(x, y)
                self.common_fish.add(fish)
                
            else:
                fish = LargeFish(x, y)
                self.large_fish.add(fish)
            
            self.all_fish.add(fish)
            return fish
            
        except pygame.error as e:
            print(f"Error spawning fish: {e}")
            return None
    
    def update(self):
        """Update all fish and handle auto-spawning."""
        self.all_fish.update()
        
        # Auto-spawn fish
        self.spawn_timer += 2
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            if len(self.all_fish) < MAX_FISH:
                self.spawn_fish()
    
    def draw(self, surface):
        """Draw all fish to the screen."""
        self.all_fish.draw(surface)
    
    def get_fish_at_position(self, pos):
        """
        Get fish at a specific position (for catching).
        
        Args:
            pos: (x, y) tuple of position to check
            
        Returns:
            Fish sprite at that position, or None
        """
        for fish in self.all_fish:
            if fish.rect.collidepoint(pos):
                return fish
        return None
    
    def remove_fish(self, fish):
        """Remove a caught fish from all groups."""
        fish.kill()  # Removes from all sprite groups
    
    def get_stats(self):
        """Get statistics about current fish."""
        return {
            "total": len(self.all_fish),
            "common": len(self.common_fish),
            "rare": len(self.rare_fish),
            "large": len(self.large_fish)
        }
    
    def clear_all(self):
        """Remove all fish (useful for restarting)."""
        self.all_fish.empty()
        self.common_fish.empty()
        self.rare_fish.empty()
        self.large_fish.empty()