"""
IMPORTANT: Always run the game from the root directory so as not to run
into directory issues! That is, main_menu.py should be the main file to run!

Classic Mode for Fish-O-Mania.

The standard game mode with a lives system. Players catch fish to earn
points while avoiding danger fish that cost lives. Game ends when all
lives are lost.

Functions:
    main: Main game loop for classic mode.
"""

import pygame
import random
from mechanics.Recorder import RECORDER
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
    START_FISHES,
)
from fish.fish_manager import FishManager
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

# Funny release messages # keep only one
RELEASE_MESSAGES = [
    "The fish chooses life today."
]


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


def draw_pause_overlay(surface):
    """
    Draw the pause screen overlay when a danger fish is caught.

    Args:
        surface (pygame.Surface): Surface to draw on.
    """
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # set transparency
    overlay.set_alpha(150)
    # fill the screen with a color
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


def draw_release_message(surface, message):
    """
    Draw the funny fish release message

    Args:
        surface (pygame.Surface): Surface to draw on
        message (str): The release message to display
    """
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((0, 100, 0))
    surface.blit(overlay, (0, 0))

    msg_text = big_font.render(message, True, (0, 255, 0))
    msg_rect = msg_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    surface.blit(msg_text, msg_rect)

    sub_text = font.render("No life lost! Keep fishing!", True, WHITE)
    sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    surface.blit(sub_text, sub_rect)


def draw_game_over_screen(surface, score, fish_caught_count, high_score_result):
    """
    Draw the game over overlay with final score and options

    Args:
        surface (pygame.Surface): Surface to draw on
        score (int): Final score achieved
        fish_caught_count (int): Number of fish caught
        high_score_result (dict): Result from update_high_score
    """
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
        center=(center_x, center_y - 100)
    )
    surface.blit(game_over_text, game_over_rect)

    # New high score notification
    if high_score_result and high_score_result["is_new_high"]:
        new_high_text = big_font.render("NEW HIGH SCORE!", True, (255, 215, 0))
        new_high_rect = new_high_text.get_rect(
            center=(center_x, center_y - 60)
        )
        surface.blit(new_high_text, new_high_rect)

    # Final score
    final_score_text = big_font.render(f"Final Score: {score}", True, WHITE)
    final_score_rect = final_score_text.get_rect(
        center=(center_x, center_y - 20)
    )
    surface.blit(final_score_text, final_score_rect)

    # Fish count
    count_text = big_font.render(f"Fish Caught: {fish_caught_count}", True, WHITE)
    count_rect = count_text.get_rect(center=(center_x, center_y + 20))
    surface.blit(count_text, count_rect)

    # High score display
    high_score_text = font.render(
        f"High Score: {current_high}",
        True,
        (200, 200, 200)
    )
    high_score_rect = high_score_text.get_rect(
        center=(center_x, center_y + 60)
    )
    surface.blit(high_score_text, high_score_rect)

    # Restart instruction
    restart_text = font.render("Press Enter to Restart", True, (255, 215, 0))
    restart_rect = restart_text.get_rect(center=(center_x, center_y + 100))
    surface.blit(restart_text, restart_rect)

    # Quit instruction
    quit_text = font.render("Press ESC to Quit", True, WHITE)
    quit_rect = quit_text.get_rect(center=(center_x, center_y + 130))
    surface.blit(quit_text, quit_rect)


def draw_danger_fish_overlay(surface, recorder, scream_progress, angler_pause_start_time, ANGLER_PAUSE_DURATION, SCREAM_PEAK_THRESHOLD):
    """
    Draw the danger fish scream overlay with progress bar.

    Args:
        surface (pygame.Surface): Surface to draw on.
        recorder (RECORDER): Audio recorder instance.
        scream_progress (float): Current scream progress (0-100).
        angler_pause_start_time (int): Start time of the pause.
        ANGLER_PAUSE_DURATION (int): Total duration allowed.
        SCREAM_PEAK_THRESHOLD (int): Threshold for detecting screams.
    """
    current_peak = recorder.get_frame_peak()
    is_screaming = current_peak >= SCREAM_PEAK_THRESHOLD
    progress = scream_progress / 100.0

    # Rounded rectangle prompt dimensions
    rect_width = 420
    rect_height = 260
    rect_center_x = SCREEN_WIDTH // 2
    rect_center_y = SCREEN_HEIGHT // 2
    corner_radius = 25

    rect_x = rect_center_x - rect_width // 2
    rect_y = rect_center_y - rect_height // 2

    # Main rectangle background
    main_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
    pygame.draw.rect(surface, (100, 15, 15), main_rect, border_radius=corner_radius)

    # Inner highlight area
    inner_rect = pygame.Rect(rect_x + 10, rect_y + 8, rect_width - 20, rect_height - 30)
    pygame.draw.rect(surface, (140, 30, 30), inner_rect, border_radius=corner_radius - 5)

    # Draw borders
    pygame.draw.rect(surface, (255, 100, 100), main_rect, 3, border_radius=corner_radius)
    inner_border_rect = pygame.Rect(rect_x + 6, rect_y + 6, rect_width - 12, rect_height - 12)
    pygame.draw.rect(surface, (180, 50, 50), inner_border_rect, 2, border_radius=corner_radius - 3)

    # Title with shadow effect
    title_font = pygame.font.Font(None, 34)
    shadow_offset = 2

    title_text = " DANGER FISH! "
    title_shadow = title_font.render(title_text, True, (60, 0, 0))
    title_render = title_font.render(title_text, True, (255, 220, 100))
    title_rect = title_render.get_rect(center=(rect_center_x, rect_center_y - 95))
    surface.blit(title_shadow, (title_rect.x + shadow_offset, title_rect.y + shadow_offset))
    surface.blit(title_render, title_rect)

    # Subtitle
    subtitle_text = "SCREAM TO ESCAPE!"
    subtitle_render = font.render(subtitle_text, True, (255, 180, 180))
    subtitle_rect = subtitle_render.get_rect(center=(rect_center_x, rect_center_y - 65))
    surface.blit(subtitle_render, subtitle_rect)

    # Volume indicator delete the volume indicator
    peak_color = (100, 255, 100) if is_screaming else (200, 200, 200)
    peak_text = font.render(f"Volume: {current_peak:,}", True, peak_color)
    peak_rect = peak_text.get_rect(center=(rect_center_x, rect_center_y - 35))
    # surface.blit(peak_text, peak_rect)

    # Progress bar
    bar_width = 280
    bar_height = 22
    bar_x = rect_center_x - bar_width // 2
    bar_y = rect_center_y - 5

    pygame.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height), border_radius=11)

    if progress > 0:
        fill_width = int(bar_width * progress)
        if fill_width > 0:
            if progress < 0.5:
                bar_color = (255, int(255 * progress * 2), 0)
            else:
                bar_color = (int(255 * (1 - (progress - 0.5) * 2)), 255, 0)
            pygame.draw.rect(surface, bar_color, (bar_x, bar_y, fill_width, bar_height), border_radius=11)

    pygame.draw.rect(surface, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=11)

    # Progress percentage
    progress_color = (100, 255, 100) if progress > 0.7 else (255, 255, 255)
    progress_text = font.render(f"{int(scream_progress)}%", True, progress_color)
    progress_rect = progress_text.get_rect(center=(rect_center_x, bar_y + bar_height + 18))
    surface.blit(progress_text, progress_rect)

    # Hint text
    if not is_screaming:
        hint_text = font.render("Scream louder!", True, (255, 200, 150))
        hint_rect = hint_text.get_rect(center=(rect_center_x, rect_center_y + 55))
        surface.blit(hint_text, hint_rect)

    # Time remaining
    remain_ms = max(0, ANGLER_PAUSE_DURATION - (pygame.time.get_ticks() - angler_pause_start_time))
    remain_s = remain_ms / 1000

    if remain_s <= 2:
        time_color = (255, 80, 80)
    elif remain_s <= 3:
        time_color = (255, 200, 100)
    else:
        time_color = (255, 255, 255)

    # get the time left
    time_text = font.render(f"Time: {remain_s:.1f}s", True, time_color)
    time_rect = time_text.get_rect(center=(rect_center_x, rect_center_y + 85))
    surface.blit(time_text, time_rect)


def main():
    """
    Main game loop for Classic Mode.

    Returns:
        int: Final score achieved.
    """
    pygame.init()

    # Load assets
    sounds = load_sounds()
    graphics = load_graphics()
    sounds['background_classic'].play(-1)  # Loop background music

    # Initialize game state
    running = True
    game_over = False
    paused = False
    pygame.display.set_caption("Fish-O-Mania: Classic Mode")
    spacebar_casting = False # Tracks spacebar casting or scream casting

    # Initialize managers
    fish_manager = FishManager()
    background_manager = BackgroundManager(use_terrain_files=True)
    casting_manager = CastingRod(ROD_MAX_LENGTH, ROD_SPEED)

    # Spawn initial fish
    for i in range(START_FISHES):
        fish_manager.spawn_fish()

    # Game variables
    score = 0
    caught_fish = []
    fish_caught_count = 0
    boat_x = graphics['boat_x']
    boat_y = graphics['boat_y']
    high_score_result = None

    # Scream control variables
    angler_pause_active = False
    angler_pause_start_time = 0
    ANGLER_PAUSE_DURATION = 5000
    SCREAM_PEAK_THRESHOLD = 5000

    # Frame-by-frame scream progress for danger fish (0-100%)
    scream_progress = 0
    SCREAM_INCREMENT = 1  # 1% per frame with scream detected

    # Scream threshold for controlling the hook
    HOOK_SCREAM_THRESHOLD = 15000

    # Release message state
    showing_release_message = False
    release_message_start_time = 0
    RELEASE_MESSAGE_DURATION = 2000
    current_release_message = ""

    # Fade in effect
    fade_alpha = 255

    # Initialize audio recorder
    recorder = RECORDER()
    recorder.start_recording()

    # Main game loop
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_SPACE:
                    if not game_over and not paused and not angler_pause_active and not showing_release_message:
                        spacebar_casting =  not spacebar_casting # If pressed depress and vice versa
                        sounds['casting'].play()

                elif event.key == pygame.K_p:
                    if not game_over and not angler_pause_active and not showing_release_message:
                        paused = not paused

                elif event.key == pygame.K_RETURN:
                    if game_over:
                        # Restart game
                        fish_manager.clear_all()
                        casting_manager.reset()
                        score = 0
                        caught_fish = []
                        fish_caught_count = 0
                        spacebar_casting = False
                        for i in range(START_FISHES):
                            fish_manager.spawn_fish()
                        game_over = False
                        high_score_result = None
                        angler_pause_active = False
                        showing_release_message = False
                        scream_progress = 0
                        recorder.frames = []
                        fade_alpha = 255

        # Check if release message duration is over
        if showing_release_message:
            now = pygame.time.get_ticks()
            if now - release_message_start_time >= RELEASE_MESSAGE_DURATION:
                showing_release_message = False

        # Update game state (only when not game over, not paused, and not in special states)
        if not game_over and not paused and not angler_pause_active and not showing_release_message:
            fish_manager.update()
            background_manager.update()

            recorder.read_frames()

            # Check if screaming
            hook_peak = recorder.get_frame_peak()
            is_screaming = hook_peak >= HOOK_SCREAM_THRESHOLD

            # Dual control: Can use either spacebar or screaming to lower the hook
            # Hook goes down if spacebar pressed to cast OR currently screaming
            # Hook goes up if spacebar toggled to reel AND not screaming

            if spacebar_casting or is_screaming:
                # Screaming/spacebar casting - hook goes down
                casting_manager.is_casting = True
            else:
                # Not screaming - hook goes up
                casting_manager.is_casting = False

            # Auto-reset spacebar toggle when hook reaches bottom or top
            if casting_manager.rod_length >= casting_manager.rod_max_length:
                spacebar_casting = False  # Auto-switch to reel mode
            #elif casting_manager.rod_length <= 0 and not is_screaming:
            #    spacebar_casting = False  # Reset when fully reeled

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
                if caught['penalty']:
                    print("Danger fish hooked! Scream to fill the bar and escape!")
                    angler_pause_active = True
                    angler_pause_start_time = pygame.time.get_ticks()
                    scream_progress = 0
                    recorder.frames = []
                else:
                    score += caught["value"]
                    fish_caught_count += 1
                    print(f"Caught: {caught['type']} (+{caught['value']} pts)")
                    caught_fish.append(caught)

                if caught.get('game_over') and not caught['penalty']:
                    print("GAME OVER!")
                    game_over = True
                    high_score_result = update_high_score("classic", score, fish_caught_count)
                    sounds['game_over'].play()

            # Update hook rect position
            hook_x = rod_x
            hook_y = rod_top_y + casting_manager.rod_length
            graphics['hook_rect'].x = (
                hook_x - graphics['hook_image'].get_width() // 2
            )
            graphics['hook_rect'].y = hook_y

        # Danger fish scream window
        elif angler_pause_active and not game_over:
            recorder.read_frames()
            current_frame_peak = recorder.get_frame_peak()
            now = pygame.time.get_ticks()

            if current_frame_peak >= SCREAM_PEAK_THRESHOLD:
                scream_progress += SCREAM_INCREMENT

                if scream_progress >= 100:
                    print(f"Scream success! Progress reached 100% - Fish escaped!")
                    angler_pause_active = False
                    casting_manager.release_danger_fish()
                    recorder.frames = []
                    scream_progress = 0

                    showing_release_message = True
                    release_message_start_time = pygame.time.get_ticks()
                    current_release_message = random.choice(RELEASE_MESSAGES)

            if angler_pause_active and now - angler_pause_start_time >= ANGLER_PAUSE_DURATION:
                print("Time's up! Fish caught but life lost!")
                angler_pause_active = False
                scream_progress = 0

                catch_result = casting_manager.catch_danger_fish(fish_manager)

                if catch_result:
                    score += catch_result["value"]
                    fish_caught_count += 1
                    print(f"Caught: {catch_result['type']} (+{catch_result['value']} pts)")

                    lives_before = fish_manager.lives_manager.get_current_lives()
                    fish_manager.lives_manager.lose_life()
                    lives_after = fish_manager.lives_manager.get_current_lives()
                    print(f"Lives: {lives_before} -> {lives_after}")

                    caught_fish.append({
                        "type": catch_result["type"],
                        "value": catch_result["value"],
                        "rarity": catch_result["rarity"],
                        "penalty": True,
                        "game_over": lives_after <= 0,
                    })

                    if lives_after <= 0:
                        game_over = True
                        high_score_result = update_high_score("classic", score, fish_caught_count)
                        sounds['game_over'].play()

                recorder.frames = []

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

        # Instructions (only when playing)
        if not game_over and not paused and not angler_pause_active and not showing_release_message:
            instructions = [
                "SPACE / SCREAM: Cast / Reel",
                "Arrow keys: Move boat",
                "P: Pause | ESC: Quit",
            ]
            y_offset = 50
            for instruction in instructions:
                text = font.render(instruction, True, WHITE)
                screen.blit(text, (10, y_offset))
                y_offset += 25

        # Draw pause overlay
        if paused:
            draw_pause_overlay(screen)

        # Draw danger fish overlay
        if angler_pause_active and not game_over:
            draw_danger_fish_overlay(
                screen, recorder, scream_progress,
                angler_pause_start_time, ANGLER_PAUSE_DURATION, SCREAM_PEAK_THRESHOLD
            )

        # Show release message overlay
        if showing_release_message and not game_over:
            draw_release_message(screen, current_release_message)

        # Draw game over screen
        if game_over:
            draw_game_over_screen(screen, score, fish_caught_count, high_score_result)

        # Draw red flash effect
        fish_manager.draw_red_flash(screen)

        # Fade in effect
        if fade_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(fade_alpha)
            screen.blit(fade_surf, (0, 0))
            fade_alpha = max(0, fade_alpha - 8)

        # Update display
        pygame.display.flip()
        clock.tick(FPS)

    # Cleanup
    sounds['background_classic'].stop()
    recorder.close()
    return score


if __name__ == '__main__':
    main()
