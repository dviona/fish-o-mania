"""
IMPORTANT: Always run the game from the root directory so as not to run
into directory issues! That is, main_menu.py should be the main file to run!

Time Attack Mode for Fish-O-Mania.

A fast-paced game mode where players have a limited time to catch as
many fish as possible. Fish move faster than normal, and catching danger
fish costs a life but still awards points.

Functions:
    main: Main game loop for time attack mode.
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
    ROD_SPEED
)
from fish.fast_fish_manager import FastFishManager
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
timer_font = pygame.font.Font(None, 72)

# Time attack settings
GAME_DURATION = 30  # Seconds
INITIAL_FISH_COUNT = 8  # More fish at start


def load_sounds():
    """
    Load and configure all sound effects.

    Returns:
        dict: Dictionary of loaded sound objects.
    """
    sounds = {
        'background_timeattack': pygame.mixer.Sound("sounds/timeattack.mp3"),
        'casting': pygame.mixer.Sound("sounds/casting-whoosh.mp3"),
    }

    sounds['background_timeattack'].set_volume(0.3)
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
    boat_y = WATER_SURFACE - boat_image.get_height() // 2 - 20

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


def draw_pause_overlay(surface, time_remaining):
    """
    Draw the pause screen overlay.

    Args:
        surface (pygame.Surface): Surface to draw on.
        time_remaining (float): Time remaining when paused.
    """
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 50))
    surface.blit(overlay, (0, 0))

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    pause_text = big_font.render("PAUSED", True, WHITE)
    pause_rect = pause_text.get_rect(center=(center_x, center_y - 40))
    surface.blit(pause_text, pause_rect)

    time_text = font.render(
        f"Time Remaining: {int(time_remaining)}s",
        True, (255, 215, 0))
    time_rect = time_text.get_rect(center=(center_x, center_y))
    surface.blit(time_text, time_rect)

    resume_text = font.render("Press P to Resume",
                              True, (200, 200, 255))
    resume_rect = resume_text.get_rect(center=(center_x, center_y + 40))
    surface.blit(resume_text, resume_rect)


def draw_game_over_screen(surface, score,
                          fish_caught_count, high_score_result):
    """
    Draw the time's up overlay with final score.

    Args:
        surface (pygame.Surface): Surface to draw on.
        score (int): Final score achieved.
        fish_caught_count (int): Number of fish caught.
        high_score_result (dict): Result from update_high_score.
    """
    current_high = get_high_score("time_attack")

    # Overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))

    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2

    # Title
    title_text = big_font.render("TIME'S UP!",
                                 True, (255, 215, 0))
    title_rect = title_text.get_rect(center=(center_x, center_y - 120))
    surface.blit(title_text, title_rect)

    # New high score notification
    if high_score_result["is_new_high"]:
        new_high_text = big_font.render("NEW HIGH SCORE!",
                                        True, (255, 215, 0))
        new_high_rect = new_high_text.get_rect(
            center=(center_x, center_y - 80))
        surface.blit(new_high_text, new_high_rect)

    # Final score
    score_text = big_font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(center_x, center_y - 40))
    surface.blit(score_text, score_rect)

    # Fish count
    count_text = big_font.render(
        f"Fish Caught: {fish_caught_count}",
        True,
        WHITE
    )
    count_rect = count_text.get_rect(center=(center_x, center_y))
    surface.blit(count_text, count_rect)

    # High score
    high_text = font.render(f"High Score: {current_high}",
                            True, (200, 200, 200))
    high_rect = high_text.get_rect(center=(center_x, center_y + 80))
    surface.blit(high_text, high_rect)

    # Instructions
    restart_text = font.render(
        "Press ENTER to Play Again", True, (255, 215, 0))
    restart_rect = restart_text.get_rect(center=(center_x, center_y + 120))
    surface.blit(restart_text, restart_rect)

    quit_text = font.render("Press ESC to Quit", True, WHITE)
    quit_rect = quit_text.get_rect(center=(center_x, center_y + 150))
    surface.blit(quit_text, quit_rect)


def handle_danger_fish_catch(casting_manager, fish_manager):
    """
    Handle catching a danger fish immediately (no scream mechanic).

    Args:
        casting_manager: The casting rod manager.
        fish_manager: The fish manager.

    Returns:
        dict: Fish info if a danger fish was caught, None otherwise.
    """
    if casting_manager.pending_danger_fish is not None:
        fish = casting_manager.pending_danger_fish
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
        casting_manager.pending_danger_fish = None
        casting_manager.attached_fish = None
        casting_manager.start_cooldown()

        return {
            "type": fish_type,
            "value": fish_value,
            "rarity": fish_rarity,
            "penalty": True
        }
    return None


def main():
    """
    Main game loop for Time Attack Mode.

    Returns:
        int: Final score achieved.
    """
    pygame.init()

    # Load assets
    sounds = load_sounds()
    graphics = load_graphics()
    sounds['background_timeattack'].play(-1)

    # Initialize game state
    running = True
    game_over = False
    paused = False
    pygame.display.set_caption("Fish-O-Mania: Time Attack")

    # Initialize managers
    fish_manager = FastFishManager()
    background_manager = BackgroundManager()
    casting_manager = CastingRod(ROD_MAX_LENGTH, ROD_SPEED)

    # Spawn initial fish (more than classic mode)
    for i in range(INITIAL_FISH_COUNT):
        fish_manager.spawn_fish()

    # Game variables
    score = 0
    caught_fish = []
    fish_caught_count = 0
    boat_x = graphics['boat_x']
    boat_y = graphics['boat_y']
    high_score_result = None

    # Timer
    start_ticks = pygame.time.get_ticks()
    paused_time = 0  # Track total time spent paused
    pause_start = 0  # When current pause started
    time_remaining = GAME_DURATION

    # Fade in effect
    fade_alpha = 255

    # Main game loop
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_SPACE:
                    if not game_over and not paused:
                        casting_manager.toggle_cast()
                        sounds['casting'].play()

                elif event.key == pygame.K_p:
                    if not game_over:
                        if paused:
                            # Resuming - add paused duration to total
                            paused_time += (
                                    pygame.time.get_ticks() - pause_start)
                            paused = False
                        else:
                            # Pausing - record when pause started
                            pause_start = pygame.time.get_ticks()
                            paused = True

                elif event.key == pygame.K_RETURN:
                    if game_over:
                        # Restart game
                        fish_manager.clear_all()
                        casting_manager.reset()
                        score = 0
                        caught_fish = []
                        fish_caught_count = 0
                        for i in range(INITIAL_FISH_COUNT):
                            fish_manager.spawn_fish()
                        game_over = False
                        high_score_result = None
                        start_ticks = pygame.time.get_ticks()
                        paused_time = 0

        # Update game state
        if not game_over and not paused:
            # Update timer (accounting for paused time)
            elapsed = (pygame.time.get_ticks() -
                       start_ticks - paused_time) / 1000
            time_remaining = max(0, GAME_DURATION - elapsed)

            if time_remaining <= 0:
                game_over = True
                high_score_result = update_high_score("time_attack",
                                                      score, fish_caught_count)

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
            rod_x = boat_x + graphics['boat_image'].get_width() - 65
            rod_top_y = boat_y + 160

            # Casting
            result = casting_manager.update(
                graphics['hook_rect'],
                fish_manager,
                sounds['casting']
            )

            if result:
                if result.get('penalty'):
                    # Danger fish caught - handle immediately
                    danger_result = handle_danger_fish_catch(
                        casting_manager, fish_manager)
                    if danger_result:
                        score += danger_result["value"]
                        fish_caught_count += 1
                        caught_fish.append(danger_result)
                        fish_manager.catch_sound.play()
                else:
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

        # Drawing
        draw_water_background(screen)
        background_manager.draw(screen)

        # Boat
        screen.blit(graphics['boat_image'], (boat_x, boat_y))

        # Fishing line
        rod_x = boat_x + graphics['boat_image'].get_width() - 65
        rod_top_y = boat_y + 160
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

        # Timer display (top center)
        timer_color = (255, 100, 100) if time_remaining <= 10 else WHITE
        timer_text = timer_font.render(
            f"{int(time_remaining)}", True, timer_color)
        timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH - 125, 50))
        screen.blit(timer_text, timer_rect)

        # Score and fish count
        score_text = big_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        count_text = font.render(
            f"Fish caught: {fish_caught_count}", True, WHITE)
        screen.blit(count_text, (10, 50))

        # Instructions
        if not game_over and not paused:
            # Mode indicator
            mode_text = font.render(
                "Race against the timer, catch them all!",
                True,
                (200, 255, 200)
            )
            mode_rect = mode_text.get_rect(
                center=(SCREEN_WIDTH // 2, 20))
            screen.blit(mode_text, mode_rect)

            instructions = [
                "SPACE: Cast",
                "P: Pause",
                "ESC: Quit"
            ]
            y_offset = 80
            for instruction in instructions:
                text = font.render(instruction, True, WHITE)
                screen.blit(text, (10, y_offset))
                y_offset += 25

        # Pause overlay
        if paused:
            draw_pause_overlay(screen, time_remaining)

        # Game over screen
        if game_over:
            draw_game_over_screen(screen, score,
                                  fish_caught_count, high_score_result)

        # Draw red flash (still shows but no penalty)
        fish_manager.draw_red_flash(screen)

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
    sounds['background_timeattack'].stop()
    return score


if __name__ == '__main__':
    main()
