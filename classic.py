"""
    This is the Classic Mode for the file and push
"""

import pygame, sys, random

pygame.init()

SKY_BLUE = (135, 206, 235)
DEEP_BLUE = (0, 105, 148)
WHITE = (255, 255, 255)

# Screen Resolution
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_RESOLUTION)
pygame.display.set_caption('Classic Mode')
screen.fill(SKY_BLUE)

clock = pygame.time.Clock()
FPS = 60


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Draw the surfaces
        screen.fill(SKY_BLUE)
        pygame.draw.rect(screen, DEEP_BLUE, (0, 200, SCREEN_WIDTH, SCREEN_HEIGHT - 200))
        pygame.draw.line(screen, WHITE, (0, 200), (SCREEN_WIDTH, 200), 2)

        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()