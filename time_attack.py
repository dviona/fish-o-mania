"""
Time Attack Mode
"""

import pygame
import sys
from constants import *
from fish_manager import FishManager
from background import BackgroundManager
from casting import CastingRod

pygame.init()

SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
big_font = pygame.font.Font(None, 36)
timer_font = pygame.font.Font(None, 72)

# Sound Effects
bg_sound = pygame.mixer.Sound("sounds/classic.mp3")
bg_sound.set_volume(0.3)

casting_sound = pygame.mixer.Sound("sounds/casting-whoosh.mp3")
casting_sound.set_volume(0.4)

# Boat setup
boat_image = pygame.image.load("graphics/boat.png")
boat_image = pygame.transform.scale(boat_image, (310, 260))
boat_x = SCREEN_WIDTH // 2 - boat_image.get_width() // 2 - 300
boat_y = WATER_SURFACE - boat_image.get_height() // 2 - 52

# Fishing hook
fishing_hook_img = pygame.image.load("graphics/fishing_hook.png")
fishing_hook_img = pygame.transform.scale(fishing_hook_img, (30, 30))
hook_rect = fishing_hook_img.get_rect()

# Time attack settings
GAME_DURATION = 60  # 60 seconds
FISH_SPEED_MULTIPLIER = 1.8  # Fish move faster


class FastFishManager(FishManager):
    """Fish manager with faster fish for time attack mode."""

    def spawn_fish(self, fish_class=None):
        """Spawn faster fish."""
        fish = super().spawn_fish(fish_class)
        if fish:
            # Make fish faster
            fish.speed_x *= FISH_SPEED_MULTIPLIER
            fish.speed_y *= FISH_SPEED_MULTIPLIER
        return fish


def main():
    pygame.init()
    bg_sound.play(-1)

    running = True
    pygame.display.set_caption("Fish-O-Mania: Time Attack")

    fish_manager = FastFishManager()
    background_manager = BackgroundManager(use_terrain_files=True)
    casting_manager = CastingRod(rod_max_length, rod_speed)

    # Spawn more fish initially
    for i in range(8):
        fish_manager.spawn_fish()

    score = 0
    caught_fish = []
    fish_caught_count = 0

    global boat_x
    game_over = False
    fade_alpha = 255

    # Timer
    start_ticks = pygame.time.get_ticks()
    time_remaining = GAME_DURATION

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if not game_over:
                        casting_manager.toggle_cast()
                        casting_sound.play()
                elif event.key == pygame.K_RETURN:
                    if game_over:
                        # Restart
                        fish_manager.clear_all()
                        score = 0
                        caught_fish = []
                        fish_caught_count = 0
                        for i in range(8):
                            fish_manager.spawn_fish()
                        game_over = False
                        start_ticks = pygame.time.get_ticks()

        if not game_over:
            # Update timer
            elapsed = (pygame.time.get_ticks() - start_ticks) / 1000
            time_remaining = max(0, GAME_DURATION - elapsed)

            if time_remaining <= 0:
                game_over = True

            fish_manager.update()
            background_manager.update()

            # Boat movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                boat_x -= BOAT_SPEED
            if keys[pygame.K_RIGHT]:
                boat_x += BOAT_SPEED
            boat_x = max(0, min(boat_x, SCREEN_WIDTH - boat_image.get_width()))

            # Hook position
            rod_x = boat_x + boat_image.get_width() - 83
            rod_top_y = boat_y + 175

            # Casting logic - ignore penalties in time attack
            result = casting_manager.update(hook_rect, fish_manager, casting_sound)
            if result:
                score += result["value"]
                fish_caught_count += 1
                caught_fish.append(result)

            hook_x = rod_x
            hook_y = rod_top_y + casting_manager.rod_length
            hook_rect.x = hook_x - fishing_hook_img.get_width() // 2
            hook_rect.y = hook_y

        # DRAWING
        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, DEEP_BLUE,
                         (0, WATER_SURFACE, SCREEN_WIDTH,
                          SCREEN_HEIGHT - WATER_SURFACE))

        for y in range(WATER_SURFACE, SCREEN_HEIGHT):
            ratio = (y - WATER_SURFACE) / (SCREEN_HEIGHT - WATER_SURFACE)
            color = tuple(int(AZURE[i] + (DEEP_BLUE[i] - AZURE[i]) * ratio)
                          for i in range(3))
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

        background_manager.draw(screen)
        screen.blit(boat_image, (boat_x, boat_y))
        pygame.draw.line(screen, WHITE, (rod_x - 5, rod_top_y),
                         (hook_x - 5, hook_y), 2)
        screen.blit(fishing_hook_img, hook_rect)
        fish_manager.draw(screen)

        # Timer display (top center)
        timer_color = (255, 100, 100) if time_remaining <= 10 else WHITE
        timer_text = timer_font.render(f"{int(time_remaining)}", True, timer_color)
        timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(timer_text, timer_rect)

        # Score and fish count
        score_text = big_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        count_text = font.render(f"Fish caught: {fish_caught_count}", True, WHITE)
        screen.blit(count_text, (10, 50))

        if not game_over:
            instructions = font.render("SPACE to cast | No lives - just catch!", True, WHITE)
            screen.blit(instructions, (10, 80))

        # Game over screen
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            title_text = big_font.render("TIME'S UP!", True, (255, 215, 0))
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
            screen.blit(title_text, title_rect)

            score_text = big_font.render(f"Final Score: {score}", True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            screen.blit(score_text, score_rect)

            count_text = big_font.render(f"Fish Caught: {fish_caught_count}", True, WHITE)
            count_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(count_text, count_rect)

            restart_text = font.render("Press ENTER to Play Again", True, (255, 215, 0))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
            screen.blit(restart_text, restart_rect)

            quit_text = font.render("Press ESC to Quit", True, WHITE)
            quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            screen.blit(quit_text, quit_rect)

        # Fade in
        if fade_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(fade_alpha)
            screen.blit(fade_surf, (0, 0))
            fade_alpha -= 8

        pygame.display.flip()
        clock.tick(FPS)

    bg_sound.stop()
    return score


if __name__ == '__main__':
    main()