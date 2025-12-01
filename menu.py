"""Aradhya"""

import pygame
import sys
from constants import *
import classic  #main code file


def draw_center_text(surface, text, font, color, y):
    render = font.render(text, True, color)
    x = SCREEN_WIDTH // 2 - render.get_width() // 2
    surface.blit(render, (x, y))


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Fish-O-Mania Menu")

    clock = pygame.time.Clock()

    title_font = pygame.font.Font(None, 70)
    menu_font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 28)

    menu_items = ["Start Game", "High Score", "Settings", "Exit"]
    selected = 0


    high_score = 0 # to-do: need to figure out a way how to store high score. For now, keeping it 0

    # Menu states
    state = "MAIN"     # MAIN or SETTINGS

    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if state == "MAIN":
                    # Up/Down navigation
                    if event.key == pygame.K_UP:
                        selected = (selected - 1) % len(menu_items)

                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(menu_items)

                    # Select option
                    elif event.key == pygame.K_RETURN:
                        option = menu_items[selected]

                        if option == "Start Game":
                            score = classic.main()     # run the game
                            if score > high_score:
                                high_score = score

                        elif option == "High Score":
                            # Just show high score screen
                            state = "HIGHSCORE"

                        elif option == "Settings":
                            state = "SETTINGS"

                        elif option == "Exit":
                        	running = False

                # High Score → return to menu
                elif state == "HIGHSCORE":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        state = "MAIN"

                # Settings → return to menu
                elif state == "SETTINGS":
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        state = "MAIN"



        if not running:
        	break


        screen.fill(SKY_BLUE)

        # Title
        draw_center_text(screen, "Fish-O-Mania", title_font, WHITE, 80)

        # MAIN MENU
        if state == "MAIN":

            y_start = 200
            for i, item in enumerate(menu_items):
                color = (255, 215, 0) if i == selected else WHITE
                draw_center_text(screen, item, menu_font, color, y_start + i * 60)

        # HIGH SCORE SCREEN
        elif state == "HIGHSCORE":
            draw_center_text(screen, "High Score", title_font, WHITE, 170)
            draw_center_text(screen, str(high_score), menu_font, WHITE, 260)
            draw_center_text(screen, "Press ESC to return", small_font, WHITE, 350)

        elif state == "SETTINGS":
            draw_center_text(screen, "Settings", title_font, WHITE, 200)
            draw_center_text(screen, "(Settings will update soon)", small_font, WHITE, 280)
            draw_center_text(screen, "Press ESC to return", small_font, WHITE, 350)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
