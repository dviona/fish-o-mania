"""
    This is the Classic Mode for the file and push
"""

import pygame, sys

from constants import *
from fish_manager import FishManager

# Initialize pygame
pygame.init()

# Main parameters for the scene
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
screen.fill(SKY_BLUE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 36)


def main():
    """Main game loop."""
    # Initialize Pygame
    pygame.init()
    # Running boolean detects if game is running or it should close
    running = True
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fish-O-Mania: Classic Mode")

    # Call the function FishManager() that allows to control fish behaviours
    fish_manager = FishManager()

    # Spawn initial fish
    for i in range(start_fishes):
        fish_manager.spawn_fish()
    # Defining the Scoreboard and Fish Net variables
    score = 0
    caught_fish = []

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Click on Fish to catch it
                fish = fish_manager.get_fish_at_position(event.pos)
                if fish:
                    info = fish.get_info()
                    score += info["value"]
                    caught_fish.append(info)
                    fish_manager.remove_fish(fish)
                    print(f"Caught: {info['type']} (+{info['value']} points)")

        # Update
        fish_manager.update()

        # Draw
        # Background
        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, DEEP_BLUE,
                         (0, WATER_SURFACE, SCREEN_WIDTH, SCREEN_HEIGHT - WATER_SURFACE))
        pygame.draw.line(screen, WHITE, (0, WATER_SURFACE), (SCREEN_WIDTH, WATER_SURFACE), 2)

        # Fish
        fish_manager.draw(screen)

        # UI
        stats = fish_manager.get_stats()

        # Score
        score_text = big_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Fish count
        count_text = font.render(f"Fish in water: {stats['total']}", True, WHITE)
        screen.blit(count_text, (10, 50))

        # Instructions
        instructions = [
            "Click fish to catch them!",
            "ESC: Quit"
        ]
        y_offset = 80
        for instruction in instructions:
            text = font.render(instruction, True, WHITE)
            screen.blit(text, (10, y_offset))
            y_offset += 25

        # Recent catches
        if caught_fish:
            recent_text = font.render("Recent Catches:", True, WHITE)
            screen.blit(recent_text, (SCREEN_WIDTH - 250, 10))
            for i, catch in enumerate(caught_fish[-5:]):
                catch_text = font.render(
                    f"{catch['type']} (+{catch['value']})",
                    True,
                    (255, 215, 0) if catch['rarity'] == 'rare' else WHITE
                )
                screen.blit(catch_text, (SCREEN_WIDTH - 250, 40 + i * 25))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()