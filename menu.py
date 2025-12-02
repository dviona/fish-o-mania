"""Aradhya Menu"""

import pygame
import sys
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, SKY_BLUE,
                       AZURE, DEEP_BLUE, WATER_SURFACE)
from background import BackgroundManager
import classic

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fish-O-Mania Menu")
clock = pygame.time.Clock()


def draw_center_text(surface, text, font, color, y):
    render = font.render(text, True, color)
    x = SCREEN_WIDTH // 2 - render.get_width() // 2
    surface.blit(render, (x, y))


def main():
    title_font = pygame.font.Font(None, 70)
    menu_font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 28)

    menu_items = ["Start Game", "High Score", "Settings", "Exit"]
    selected = 0

    high_score = 0

    # Menu states
    state = "MAIN"

    # Background manager instance
    background = BackgroundManager(use_terrain_files=True)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if state == "MAIN":
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(menu_items)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(menu_items)
                    elif event.key == pygame.K_RETURN:
                        option = menu_items[selected]

                        if option == "Start Game":
                            score = classic.main()
                            if score and score > high_score:
                                high_score = score
                        elif option == "High Score":
                            state = "HIGHSCORE"
                        elif option == "Settings":
                            state = "SETTINGS"
                        elif option == "Exit":
                            running = False

                elif state == "HIGHSCORE":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        state = "MAIN"

                elif state == "SETTINGS":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        state = "MAIN"

        if not running:
            break

        # Update background animations
        background.update()

        # DRAWING SECTION
        # Sky
        screen.fill(SKY_BLUE)

        # Water gradient
        for y in range(WATER_SURFACE, SCREEN_HEIGHT):
            ratio = (y - WATER_SURFACE) / (SCREEN_HEIGHT - WATER_SURFACE)
            color = tuple(int(AZURE[i] + (DEEP_BLUE[i] - AZURE[i]) * ratio)
                          for i in range(3))
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))

        # Draw background elements (seaweed, bubbles, waves, etc.)
        background.draw(screen)

        # Title
        draw_center_text(screen, "Fish-O-Mania", title_font, WHITE, 80)

        # MAIN MENU
        if state == "MAIN":
            y_start = 200
            for i, item in enumerate(menu_items):
                color = (255, 215, 0) if i == selected else WHITE
                draw_center_text(screen, item, menu_font, color, y_start + i * 60)

            # Instructions
            draw_center_text(screen, "Use UP/DOWN arrows and ENTER to select",
                           small_font, (180, 200, 220), SCREEN_HEIGHT - 50)

        # HIGH SCORE SCREEN
        elif state == "HIGHSCORE":
            draw_center_text(screen, "High Score", title_font, WHITE, 170)
            draw_center_text(screen, str(high_score), menu_font, (255, 215, 0), 260)
            draw_center_text(screen, "Press ESC or ENTER to return", small_font, WHITE, 350)

        # SETTINGS SCREEN
        elif state == "SETTINGS":
            draw_center_text(screen, "Settings", title_font, WHITE, 170)
            draw_center_text(screen, "(Coming soon)", small_font, (180, 180, 180), 260)
            draw_center_text(screen, "Press ESC or ENTER to return", small_font, WHITE, 350)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()