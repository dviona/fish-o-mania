"""
IMPORTANT: Always run the game from the root directory so as not to run
into directory issues! That is, main_menu.py should be the main file to run!

Main Entry Point for Fish-O-Mania

This module serves as the main entry point for the game,
handling the game loop and launching different game modes

Run the game with:
    python main.py

Functions:
    main: Main entry point and game loop
"""

import pygame
import sys
from mechanics.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from ui import MenuScreen

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fish-O-Mania")
clock = pygame.time.Clock()


def main():
    """Main entry point and game loop"""
    menu = MenuScreen()
    running = True

    while running:
        mouse_clicked = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_clicked = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if menu.showing_high_scores:
                        menu.showing_high_scores = False
                    else:
                        running = False

                elif not menu.transitioning:
                    if menu.showing_high_scores:
                        # Close high scores on Enter or Escape
                        if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                            menu.showing_high_scores = False
                    else:
                        # Keyboard navigation
                        if event.key == pygame.K_UP:
                            menu.move_selection(-1)
                        elif event.key == pygame.K_DOWN:
                            menu.move_selection(1)
                        elif event.key == pygame.K_RETURN:
                            action = menu.select_current()
                            if action in ["classic", "time_attack", "endless"]:
                                pygame.mixer.music.stop()
                                menu.start_transition(action)
                            elif action == "high_scores":
                                menu.showing_high_scores = True
                            elif action == "quit":
                                running = False

        # Handle mouse clicks
        if mouse_clicked and not menu.transitioning:
            if not menu.showing_high_scores:
                action = menu.handle_click(pygame.mouse.get_pos())
                if action in ["classic", "time_attack", "endless"]:
                    pygame.mixer.music.stop()
                    menu.start_transition(action)
                elif action == "high_scores":
                    menu.showing_high_scores = True
                elif action == "quit":
                    running = False

        # Update menu
        result = menu.update()

        # Launch game modes after transition
        if result == "classic":
            print("Launching Classic Mode...")
            pygame.display.set_caption("Fish-O-Mania: Classic Mode")
            from modes.mode_classic import main as classic_main
            classic_main()
            pygame.display.set_caption("Fish-O-Mania")
            menu = MenuScreen()

        elif result == "time_attack":
            print("Launching Time Attack...")
            pygame.display.set_caption("Fish-O-Mania: Time Attack")
            from modes.mode_time_attack import main as time_attack_main
            time_attack_main()
            pygame.display.set_caption("Fish-O-Mania")
            menu = MenuScreen()

        elif result == "endless":
            print("Launching Endless Mode...")
            pygame.display.set_caption("Fish-O-Mania: Endless Mode")
            from modes.mode_endless import main as endless_main
            endless_main()
            pygame.display.set_caption("Fish-O-Mania")
            menu = MenuScreen()

        # Draw menu
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
