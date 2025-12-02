"""
Endless Mode - Relaxing fishing with no lives or timer.
Play at your own pace!
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

# Sound Effects
bg_sound = pygame.mixer.Sound("sounds/classic.mp3")
bg_sound.set_volume(0.25)  # Slightly quieter for relaxing mode

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


class RelaxedFishManager(FishManager):
    """Fish manager without lives system for endless mode."""

    def remove_fish(self, fish):
        """Remove fish without penalty - just catch everything!"""
        info = fish.get_info()

        # Play catch sound for all fish
        self.catch_sound.play()

        # Add to recent catches
        catch_data = {
            'type': info['type'],
            'value': info['value'],
            'rarity': info['rarity'],
            'current_frame': 0,
            'frame_counter': 0,
            'frame_delay': 8
        }
        self.recent_catches.append(catch_data)
        if len(self.recent_catches) > self.max_recent_catches:
            self.recent_catches.pop(0)

        # Create death animation
        death_anim = fish.create_death_animation()
        if death_anim:
            self.death_animations.add(death_anim)

        fish.kill()

        # Return info - no penalty, no game over
        return {
            **info,
            'penalty': False,
            'game_over': False
        }

    def draw(self, surface):
        """Draw fish without lives display."""
        self.all_fish.draw(surface)
        self.death_animations.draw(surface)
        # Don't draw lives - endless mode!
        self.draw_recent_catches(surface, SCREEN_WIDTH - 220)


def format_time(seconds):
    """Format seconds into MM:SS."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def main():
    pygame.init()
    bg_sound.play(-1)

    running = True
    pygame.display.set_caption("Fish-O-Mania: Endless Mode")

    fish_manager = RelaxedFishManager()
    background_manager = BackgroundManager(use_terrain_files=True)
    casting_manager = CastingRod(rod_max_length, rod_speed)

    for i in range(START_FISHES):
        fish_manager.spawn_fish()

    score = 0
    caught_fish = []
    fish_caught_count = 0

    global boat_x
    paused = False
    fade_alpha = 255

    # Session timer (just for display, no limit)
    start_ticks = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if not paused:
                        casting_manager.toggle_cast()
                        casting_sound.play()
                elif event.key == pygame.K_p:
                    paused = not paused

        if not paused:
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

            # Casting logic
            result = casting_manager.update(hook_rect, fish_manager, casting_sound)
            if result:
                score += result["value"]
                fish_caught_count += 1
                caught_fish.append(result)

            hook_x = rod_x
            hook_y = rod_top_y + casting_manager.rod_length
            hook_rect.x = hook_x - fishing_hook_img.get_width() // 2
            hook_rect.y = hook_y

        # Session time
        elapsed = (pygame.time.get_ticks() - start_ticks) / 1000

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

        # UI - Score and stats
        score_text = big_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        count_text = font.render(f"Fish caught: {fish_caught_count}", True, WHITE)
        screen.blit(count_text, (10, 50))

        time_text = font.render(f"Time: {format_time(elapsed)}", True, WHITE)
        screen.blit(time_text, (10, 75))

        # Mode indicator
        mode_text = font.render("ENDLESS MODE - No lives, just vibes", True, (200, 255, 200))
        mode_rect = mode_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        screen.blit(mode_text, mode_rect)

        # Instructions
        instructions = [
            "SPACE: Cast",
            "P: Pause",
            "ESC: Quit"
        ]
        y_offset = SCREEN_HEIGHT - 80
        for instruction in instructions:
            text = font.render(instruction, True, WHITE)
            screen.blit(text, (10, y_offset))
            y_offset += 22

        # Pause overlay
        if paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 50))
            screen.blit(overlay, (0, 0))

            pause_text = big_font.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
            screen.blit(pause_text, pause_rect)

            resume_text = font.render("Press P to Resume", True, (200, 200, 255))
            resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
            screen.blit(resume_text, resume_rect)

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