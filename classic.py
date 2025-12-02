"""
    This is the Classic Mode for the game
"""
# Importing the different libraries and methods
import pygame
import sys
from constants import *
from fish_manager import FishManager
from background import BackgroundManager
from casting import CastingRod

# Initialize pygame
pygame.init()


# Main parameters for the scene
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 36)

# Sound Effects
bg_sound = pygame.mixer.Sound("sounds/classic.mp3")
bg_sound.set_volume(0.3)

casting_sound = pygame.mixer.Sound("sounds/casting-whoosh.mp3")
casting_sound.set_volume(0.4)

bubble_sound = pygame.mixer.Sound("sounds/bubble.mp3")
bubble_sound.set_volume(0.5)

game_over_sound = pygame.mixer.Sound("sounds/game_over.mp3")
game_over_sound.set_volume(0.5)

# Defining parameters for the boat
boat_image = pygame.image.load("graphics/boat.png")
boat_image = pygame.transform.scale(boat_image, (310, 260))
boat_x = SCREEN_WIDTH // 2 - boat_image.get_width() // 2 - 300
boat_y = WATER_SURFACE - boat_image.get_height() // 2 - 52

# Defining parameters for the fishing hook
fishing_hook_img = pygame.image.load("graphics/fishing_hook.png")
fishing_hook_img = pygame.transform.scale(fishing_hook_img, (30, 30))
hook_rect = fishing_hook_img.get_rect()

"""
    Main game loop where all features will be defined and called
"""


def main():
    # Initialize Pygame
    pygame.init()
    bg_sound.play(-1)

    # 'running' boolean detects if game is running
    running = True
    pygame.display.set_caption("Fish-O-Mania: Classic Mode")

    # Call the function that allows to control fish and background animations
    fish_manager = FishManager()
    background_manager = BackgroundManager(use_terrain_files=True)
    casting_manager = CastingRod(rod_max_length, rod_speed)

    # Spawn initial fishes
    for i in range(START_FISHES):
        fish_manager.spawn_fish()

    # Defining the Scoreboard and Fish Net variables
    score = 0
    caught_fish = []

    # Defining global casting variables
    global boat_x, is_casting, rod_length

    # Add game_over flag before the while loop
    game_over = False

    # Fade in from black
    fade_alpha = 255

    # Main Game
    while running:
        # Event Handling Section - Monitor keypresses, mouse movements etc
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Monitor for any key-presses
            elif event.type == pygame.KEYDOWN:
                # Exit if 'esc' button pressed
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Press SPACE to restart if game over, or cast rod if playing
                elif event.key == pygame.K_SPACE:
                    if not game_over:

                        casting_manager.toggle_cast()
                        casting_sound.play()

                # Press Enter to restart the game
                elif event.key == pygame.K_RETURN:
                    if game_over:
                        # Restart the game
                        fish_manager.clear_all()
                        score = 0
                        caught_fish = []
                        for i in range(START_FISHES):
                            fish_manager.spawn_fish()
                        game_over = False
                        #rod_length = 0
                        #is_casting = False

        # Only update game elements if not game over
        if not game_over:
            # Update the fish and background animations
            fish_manager.update()
            background_manager.update()

            # Move boat left/right with arrow keys
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                boat_x -= BOAT_SPEED

            if keys[pygame.K_RIGHT]:
                boat_x += BOAT_SPEED

            # So the character doesn't disappear off-screen
            boat_x = max(0, min(boat_x, SCREEN_WIDTH - boat_image.get_width()))

            # Where the hook is attached on the rod
            rod_x = boat_x + boat_image.get_width() - 83
            rod_top_y = boat_y + 175

            # Casting Rod Logic
            caught = casting_manager.update(hook_rect, fish_manager, bubble_sound)
            if caught:
                # Only add score if not a penalty fish
                if not caught['penalty']:
                    score += caught["value"]
                    print(f"Caught: {caught['type']} (+{caught['value']} points)")
                else:
                    print(f"Danger fish! Lives: {fish_manager.lives_manager.get_current_lives()}")

                caught_fish.append(caught)

                # Check if game over
                if caught['game_over']:
                    print("GAME OVER!")
                    game_over = True
                    game_over_sound.play()

            # Final hook position
            hook_x = rod_x
            hook_y = rod_top_y + casting_manager.rod_length

            # Define hook rect for clicking
            hook_rect.x = hook_x - fishing_hook_img.get_width() // 2
            hook_rect.y = hook_y

        # DRAWING SECTION (always draw, even when paused)
        # Sky Backdrops
        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, DEEP_BLUE,
                         (0, WATER_SURFACE, SCREEN_WIDTH,
                          SCREEN_HEIGHT - WATER_SURFACE))
        pygame.draw.line(screen, WHITE, (0, WATER_SURFACE),
                         (SCREEN_WIDTH, WATER_SURFACE), 2)

        # Water background with gradient effect
        for y in range(WATER_SURFACE, SCREEN_HEIGHT):
            ratio = (y - WATER_SURFACE) / (SCREEN_HEIGHT - WATER_SURFACE)
            color = tuple(int(AZURE[i] + (DEEP_BLUE[i] - AZURE[i]) * ratio)
                          for i in range(3))
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

        # Draw background elements
        background_manager.draw(screen)

        # Put boat on top of the water line
        screen.blit(boat_image, (boat_x, boat_y))

        # Draw fishing line
        pygame.draw.line(screen, WHITE, (rod_x - 5, rod_top_y),
                         (hook_x - 5, hook_y), 2)

        # Display fishing hook
        screen.blit(fishing_hook_img, hook_rect)

        # Fish
        fish_manager.draw(screen)

        # Get Fish Stats
        stats = fish_manager.get_stats()

        # Display Score
        score_text = big_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Fish count
        count_text = font.render(f"Fish in water: {stats['total']}", True, WHITE)
        screen.blit(count_text, (10, 50))

        # In Game Instructions (only show if not game over)
        if not game_over:
            instructions = [
                "Press SPACE to cast and catch fish!",
                "ESC: Quit"
            ]
            y_offset = 80
            for instruction in instructions:
                text = font.render(instruction, True, WHITE)
                screen.blit(text, (10, y_offset))
                y_offset += 25


        # Display game over screen
        if game_over:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            # Game over text
            game_over_text = big_font.render("GAME OVER!", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(game_over_text, game_over_rect)

            # Final score
            final_score_text = big_font.render(f"Final Score: {score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
            screen.blit(final_score_text, final_score_rect)

            # Restart instruction
            restart_text = font.render("Press Enter to Restart", True, (255, 215, 0))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
            screen.blit(restart_text, restart_rect)

            quit_text = font.render("Press ESC to Quit", True, WHITE)
            quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
            screen.blit(quit_text, quit_rect)

        # Draw red flash effect if penalty occurred
        fish_manager.draw_red_flash(screen)

        # Fade in from black at start
        if fade_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(fade_alpha)
            screen.blit(fade_surf, (0, 0))
            fade_alpha -= 8

        # Update the entire screen to show the changes
        pygame.display.flip()
        clock.tick(FPS)
    return score

if __name__ == '__main__':
    main()