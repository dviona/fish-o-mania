"""
IMPORTANT: Always run the game from the root directory so as not to run
into directory issues! That is, main_menu.py should be the main file to run!

Endless Mode for Fish-O-Mania.

A relaxing game_copy mode with no lives or timer. Players can fish at their
own pace without any penalties. Perfect for casual play and practicing.

Classes:
    RelaxedFishManager: Fish manager without penalty system.

Functions:
    format_time: Formats seconds into MM:SS string.
    main: Main game_copy loop for endless mode.
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
from fish.fish_manager import FishManager
from fish.relaxed_fish_manager import RelaxedFishManager
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


def format_time(seconds):
    """
    Format seconds into MM:SS display string.

    Args:
        seconds (float): Time in seconds.

    Returns:
        str: Formatted time string (e.g., "05:30").
    """
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def load_sounds():
    """
    Load and configure all sound effects.

    Returns:
        dict: Dictionary of loaded sound objects.
    """
    sounds = {
        'background_endless': pygame.mixer.Sound("sounds/endless.mp3"),
        'casting': pygame.mixer.Sound("sounds/casting-whoosh.mp3"),
    }

    # Slightly quieter for relaxing mode
    sounds['background_endless'].set_volume(0.25)
    sounds['casting'].set_volume(0.4)

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
    surface.fill(SKY_BLUE)
    pygame.draw.rect(
        surface,
        DEEP_BLUE,
        (0, WATER_SURFACE, SCREEN_WIDTH, SCREEN_HEIGHT - WATER_SURFACE)
    )

    for y in range(WATER_SURFACE, SCREEN_HEIGHT):
        ratio = (y - WATER_SURFACE) / (SCREEN_HEIGHT - WATER_SURFACE)
        color = tuple(
            int(AZURE[i] + (DEEP_BLUE[i] - AZURE[i]) * ratio)
            for i in range(3)
        )
        pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))


def draw_pause_overlay(surface):
    """
    Draw the pause screen overlay.

    Args:
        surface (pygame.Surface): Surface to draw on.
    """
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 50))
    surface.blit(overlay, (0, 0))

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    pause_text = big_font.render("PAUSED", True, WHITE)
    pause_rect = pause_text.get_rect(center=(center_x, center_y - 20))
    surface.blit(pause_text, pause_rect)

    resume_text = font.render("Press P to Resume", True, (200, 200, 255))
    resume_rect = resume_text.get_rect(center=(center_x, center_y + 20))
    surface.blit(resume_text, resume_rect)


def main():
    """
    Main game_copy loop for Endless Mode.

    Returns:
        int: Final score achieved.
    """
    pygame.init()

    # Load assets
    sounds = load_sounds()
    graphics = load_graphics()
    sounds['background_endless'].play(-1)

    # Initialize game_copy state
    running = True
    paused = False
    pygame.display.set_caption("Fish-O-Mania: Endless Mode")

    # Initialize managers
    fish_manager = RelaxedFishManager()
    background_manager = BackgroundManager(use_terrain_files=True)
    casting_manager = CastingRod(ROD_MAX_LENGTH, ROD_SPEED)

    # Spawn initial fish
    for _ in range(START_FISHES):
        fish_manager.spawn_fish()

    # Game variables
    score = 0
    caught_fish = []
    fish_caught_count = 0
    boat_x = graphics['boat_x']
    boat_y = graphics['boat_y']

    # Session timer (display only, no limit)
    start_ticks = pygame.time.get_ticks()

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
                    # Save score before quitting
                    elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
                    update_high_score(
                        "endless", score, fish_caught_count, elapsed
                    )
                    running = False

                elif event.key == pygame.K_SPACE:
                    if not paused:
                        casting_manager.toggle_cast()
                        sounds['casting'].play()

                elif event.key == pygame.K_p:
                    paused = not paused

        # Update game_copy state (when not paused)
        if not paused:
            fish_manager.update()
            background_manager.update()

            # Boat movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                boat_x -= BOAT_SPEED
            if keys[pygame.K_RIGHT]:
                boat_x += BOAT_SPEED

            boat_x = max(
                0,
                min(boat_x, SCREEN_WIDTH - graphics['boat_image'].get_width())
            )

            # Hook position
            rod_x = boat_x + graphics['boat_image'].get_width() - 83
            rod_top_y = boat_y + 175

            # Casting
            result = casting_manager.update(
                graphics['hook_rect'],
                fish_manager,
                sounds['casting']
            )

            if result:
                score += result["value"]
                fish_caught_count += 1
                caught_fish.append(result)

            # Update hook rect
            hook_x = rod_x
            hook_y = rod_top_y + casting_manager.rod_length
            graphics['hook_rect'].x = (
                hook_x - graphics['hook_image'].get_width() // 2
            )
            graphics['hook_rect'].y = hook_y

        # Session time
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000

        # Drawing
        draw_water_background(screen)
        background_manager.draw(screen)

        # Boat
        screen.blit(graphics['boat_image'], (boat_x, boat_y))

        # Fishing line
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

        # Hook
        screen.blit(graphics['hook_image'], graphics['hook_rect'])

        # Fish
        fish_manager.draw(screen)

        # UI - Score and stats
        current_high = get_high_score("endless")

        score_text = big_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        count_text = font.render(f"Fish caught: {fish_caught_count}", True, WHITE)
        screen.blit(count_text, (10, 50))

        time_text = font.render(f"Time: {format_time(elapsed)}", True, WHITE)
        screen.blit(time_text, (10, 75))

        high_text = font.render(
            f"High Score: {current_high}",
            True,
            (200, 200, 200)
        )
        screen.blit(high_text, (10, 100))

        # Mode indicator
        mode_text = font.render(
            "ENDLESS MODE - No lives, just vibes",
            True,
            (200, 255, 200)
        )
        mode_rect = mode_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        screen.blit(mode_text, mode_rect)

        # Instructions
        instructions = [
            "SPACE: Cast",
            "P: Pause",
            "ESC: Save & Quit"
        ]
        y_offset = SCREEN_HEIGHT - 80
        for instruction in instructions:
            text = font.render(instruction, True, WHITE)
            screen.blit(text, (10, y_offset))
            y_offset += 22

        # Pause overlay
        if paused:
            draw_pause_overlay(screen)

        # Fade in
        if fade_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(fade_alpha)
            screen.blit(fade_surf, (0, 0))
            fade_alpha -= 8

        pygame.display.flip()
        clock.tick(FPS)

    # Cleanup
    sounds['background_endless'].stop()
    return score


if __name__ == '__main__':
    main()
