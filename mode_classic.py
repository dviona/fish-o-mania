"""
Classic Mode for Fish-O-Mania.

The standard game_copy mode with a lives system. Players catch fish to earn
points while avoiding danger fish that cost lives. Game ends when all
lives are lost.

Functions:
    main: Main game_copy loop for classic mode.
"""

import pygame
from mechanics.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WHITE,
    SKY_BLUE,
    AZURE,
    DEEP_BLUE,
    WATER_SURFACE,
    BOAT_SPEED,
    ROD_MAX_LENGTH,
    ROD_SPEED,
    START_FISHES
)
from fish_manager import FishManager
from background import BackgroundManager
from mechanics.casting import CastingRod
from mechanics.scores import update_high_score, get_high_score

# Initialize pygame
pygame.init()

# Display setup
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 36)


def load_sounds():
    """
    Load and configure all sound effects.

    Returns:
        dict: Dictionary of loaded sound objects.
    """
    sounds = {
        'background_classic': pygame.mixer.Sound("sounds/classic.mp3"),
        'casting': pygame.mixer.Sound("sounds/casting-whoosh.mp3"),
        'bubble': pygame.mixer.Sound("sounds/bubble.mp3"),
        'game_over': pygame.mixer.Sound("sounds/game_over.mp3")
    }

    # Set volumes
    sounds['background_classic'].set_volume(0.3)
    sounds['casting'].set_volume(0.4)
    sounds['bubble'].set_volume(0.5)
    sounds['game_over'].set_volume(0.5)

    return sounds


def load_graphics():
    """
    Load and configure all graphic assets.

    Returns:
        dict: Dictionary containing loaded images and their rects.
    """
    # Load boat
    boat_image = pygame.image.load("graphics/boat.png")
    boat_image = pygame.transform.scale(boat_image, (310, 260))
    boat_x = SCREEN_WIDTH // 2 - boat_image.get_width() // 2 - 300
    boat_y = WATER_SURFACE - boat_image.get_height() // 2 - 52

    # Load fishing hook
    hook_image = pygame.image.load("graphics/fishing_hook.png")
    hook_image = pygame.transform.scale(hook_image, (30, 30))
    hook_rect = hook_image.get_rect()

    return {
        'boat_image': boat_image,
        'boat_x': boat_x,
        'boat_y': boat_y,
        'hook_image': hook_image,
        'hook_rect': hook_rect
    }


def draw_water_background(surface):
    """
    Draw the sky and water gradient background.

    Args:
        surface (pygame.Surface): Surface to draw on.
    """
    # Sky
    surface.fill(SKY_BLUE)

    # Water area
    pygame.draw.rect(
        surface,
        DEEP_BLUE,
        (0, WATER_SURFACE, SCREEN_WIDTH, SCREEN_HEIGHT - WATER_SURFACE)
    )

    # Water surface line
    pygame.draw.line(
        surface,
        WHITE,
        (0, WATER_SURFACE),
        (SCREEN_WIDTH, WATER_SURFACE),
        2
    )

    # Water gradient
    for y in range(WATER_SURFACE, SCREEN_HEIGHT):
        ratio = (y - WATER_SURFACE) / (SCREEN_HEIGHT - WATER_SURFACE)
        color = tuple(
            int(AZURE[i] + (DEEP_BLUE[i] - AZURE[i]) * ratio)
            for i in range(3)
        )
        pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))


def draw_game_over_screen(surface, score, caught_fish):
    """
    Draw the game_copy over overlay with final score and options.

    Args:
        surface (pygame.Surface): Surface to draw on.
        score (int): Final score achieved.
        caught_fish (list): List of caught fish for statistics.
    """
    # Check for new high score
    result = update_high_score("classic", score, len(caught_fish))
    current_high = get_high_score("classic")

    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Game over title
    game_over_text = big_font.render("GAME OVER!", True, (255, 0, 0))
    game_over_rect = game_over_text.get_rect(
        center=(center_x, center_y - 80)
    )
    surface.blit(game_over_text, game_over_rect)

    # New high score notification
    if result["is_new_high"]:
        new_high_text = big_font.render("NEW HIGH SCORE!", True, (255, 215, 0))
        new_high_rect = new_high_text.get_rect(
            center=(center_x, center_y - 40)
        )
        surface.blit(new_high_text, new_high_rect)

    # Final score
    final_score_text = big_font.render(f"Final Score: {score}", True, WHITE)
    final_score_rect = final_score_text.get_rect(
        center=(center_x, center_y + 10)
    )
    surface.blit(final_score_text, final_score_rect)

    # High score display
    high_score_text = font.render(
        f"High Score: {current_high}",
        True,
        (200, 200, 200)
    )
    high_score_rect = high_score_text.get_rect(
        center=(center_x, center_y + 45)
    )
    surface.blit(high_score_text, high_score_rect)

    # Restart instruction
    restart_text = font.render("Press Enter to Restart", True, (255, 215, 0))
    restart_rect = restart_text.get_rect(center=(center_x, center_y + 85))
    surface.blit(restart_text, restart_rect)

    # Quit instruction
    quit_text = font.render("Press ESC to Quit", True, WHITE)
    quit_rect = quit_text.get_rect(center=(center_x, center_y + 115))
    surface.blit(quit_text, quit_rect)


def main():
    """
    Main game_copy loop for Classic Mode.

    Returns:
        int: Final score achieved.
    """
    pygame.init()

    # Load assets
    sounds = load_sounds()
    graphics = load_graphics()
    sounds['background_classic'].play(-1)  # Loop background music

    # Initialize game_copy state
    running = True
    game_over = False
    pygame.display.set_caption("Fish-O-Mania: Classic Mode")

    # Initialize managers
    fish_manager = FishManager()
    background_manager = BackgroundManager(use_terrain_files=True)
    casting_manager = CastingRod(ROD_MAX_LENGTH, ROD_SPEED)

    # Spawn initial fish
    for _ in range(START_FISHES):
        fish_manager.spawn_fish()

    # Game variables
    score = 0
    caught_fish = []
    boat_x = graphics['boat_x']
    boat_y = graphics['boat_y']

    # Fade in effect
    fade_alpha = 255

    # Main game_copy loop
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    if not game_over:
                        casting_manager.toggle_cast()
                        sounds['casting'].play()

                elif event.key == pygame.K_RETURN:
                    if game_over:
                        # Restart game_copy
                        fish_manager.clear_all()
                        score = 0
                        caught_fish = []
                        for _ in range(START_FISHES):
                            fish_manager.spawn_fish()
                        game_over = False

        # Update game_copy state (only when not game_copy over)
        if not game_over:
            fish_manager.update()
            background_manager.update()

            # Boat movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                boat_x -= BOAT_SPEED
            if keys[pygame.K_RIGHT]:
                boat_x += BOAT_SPEED

            # Keep boat on screen
            boat_x = max(
                0,
                min(boat_x, SCREEN_WIDTH - graphics['boat_image'].get_width())
            )

            # Calculate hook position
            rod_x = boat_x + graphics['boat_image'].get_width() - 83
            rod_top_y = boat_y + 175

            # Update casting and check for catches
            caught = casting_manager.update(
                graphics['hook_rect'],
                fish_manager,
                sounds['bubble']
            )

            if caught:
                if not caught['penalty']:
                    score += caught["value"]
                    print(f"Caught: {caught['type']} (+{caught['value']} pts)")
                else:
                    lives = fish_manager.lives_manager.get_current_lives()
                    print(f"Danger fish! Lives: {lives}")

                caught_fish.append(caught)

                if caught['game_over']:
                    print("GAME OVER!")
                    game_over = True
                    sounds['game_over'].play()

            # Update hook rect position
            hook_x = rod_x
            hook_y = rod_top_y + casting_manager.rod_length
            graphics['hook_rect'].x = (
                hook_x - graphics['hook_image'].get_width() // 2
            )
            graphics['hook_rect'].y = hook_y

        # Drawing
        draw_water_background(screen)
        background_manager.draw(screen)

        # Draw boat
        screen.blit(graphics['boat_image'], (boat_x, boat_y))

        # Draw fishing line
        rod_x = boat_x + graphics['boat_image'].get_width() - 83
        rod_top_y = boat_y + 175
        hook_x = rod_x
        hook_y = rod_top_y + casting_manager.rod_length

        pygame.draw.line(
            screen,
            WHITE,
            (rod_x - 5, rod_top_y),
            (hook_x - 5, hook_y),
            2
        )

        # Draw hook
        screen.blit(graphics['hook_image'], graphics['hook_rect'])

        # Draw fish
        fish_manager.draw(screen)

        # Draw UI
        stats = fish_manager.get_stats()

        score_text = big_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        count_text = font.render(f"Fish in water: {stats['total']}", True, WHITE)
        screen.blit(count_text, (10, 50))

        # Instructions (only when playing)
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

        # Draw game_copy over screen
        if game_over:
            draw_game_over_screen(screen, score, caught_fish)

        # Draw red flash effect
        fish_manager.draw_red_flash(screen)

        # Fade in effect
        if fade_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(fade_alpha)
            screen.blit(fade_surf, (0, 0))
            fade_alpha -= 8

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    # Cleanup
    sounds['background_classic'].stop()
    return score


if __name__ == '__main__':
    main()
