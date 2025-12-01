"""
Main Menu for Fish-O-Mania
"""

import pygame
import sys
import math
import random
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, SKY_BLUE,
                       AZURE, DEEP_BLUE, WATER_SURFACE, WATER_BOTTOM)
from background import BackgroundManager


# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fish-O-Mania")
clock = pygame.time.Clock()


class Button:
    """Simple menu button with hover effect."""

    def __init__(self, x, y, width, height, text, enabled=True):
        self.base_x = x
        self.base_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.enabled = enabled
        self.hovered = False

        # Colors
        self.normal_color = (0, 105, 148)
        self.hover_color = (0, 140, 190)
        self.disabled_color = (80, 80, 100)
        self.border_color = WHITE

        self.font = pygame.font.Font(None, 36)

    def update(self, mouse_pos):
        """Update hover state."""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hovered = rect.collidepoint(mouse_pos) and self.enabled

    def draw(self, surface):
        """Draw the button."""
        if not self.enabled:
            bg_color = self.disabled_color
            text_color = (150, 150, 150)
        elif self.hovered:
            bg_color = self.hover_color
            text_color = WHITE
        else:
            bg_color = self.normal_color
            text_color = WHITE

        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, bg_color, rect, border_radius=10)
        pygame.draw.rect(surface, self.border_color, rect, 3, border_radius=10)

        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

        if not self.enabled:
            small_font = pygame.font.Font(None, 20)
            soon_text = small_font.render("Coming Soon", True, (200, 200, 100))
            soon_rect = soon_text.get_rect(center=(rect.centerx, rect.bottom + 12))
            surface.blit(soon_text, soon_rect)

    def is_clicked(self, mouse_pos, mouse_clicked):
        """Check if clicked."""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return self.enabled and rect.collidepoint(mouse_pos) and mouse_clicked


class MainMenu:
    """Simple main menu."""

    def __init__(self):
        self.background = BackgroundManager(use_terrain_files=True)

        # Load boat
        try:
            self.boat_image = pygame.image.load("graphics/boat.png").convert_alpha()
            self.boat_image = pygame.transform.scale(self.boat_image, (310, 260))
        except pygame.error:
            self.boat_image = pygame.Surface((310, 260), pygame.SRCALPHA)
            pygame.draw.polygon(self.boat_image, (139, 90, 43),
                              [(50, 200), (260, 200), (230, 250), (80, 250)])

        # Boat position
        self.boat_x = SCREEN_WIDTH // 2 - 155
        self.boat_y = WATER_SURFACE - 130

        # Title position
        self.title_y = 100

        # Fonts
        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 32)

        # Buttons
        btn_w, btn_h = 250, 50
        btn_x = SCREEN_WIDTH // 2 - btn_w // 2
        start_y = SCREEN_HEIGHT // 2 + 20
        spacing = 70

        self.buttons = [
            Button(btn_x, start_y, btn_w, btn_h, "Classic Mode", True),
            Button(btn_x, start_y + spacing, btn_w, btn_h, "Time Attack", False),
            Button(btn_x, start_y + spacing * 2, btn_w, btn_h, "Endless Mode", False),
            Button(btn_x, start_y + spacing * 3, btn_w, btn_h, "Settings", False),
            Button(btn_x, start_y + spacing * 4, btn_w, btn_h, "Quit", True),
        ]

        # Transition state
        self.transitioning = False
        self.transition_speed = 0
        self.transition_target = None
        self.transition_done = False
        self.fade_alpha = 0

    def start_transition(self, target):
        """Start the exit transition."""
        self.transitioning = True
        self.transition_target = target
        self.transition_speed = 2

    def update(self):
        """Update menu."""
        self.background.update()

        if self.transitioning:
            # Accelerate
            self.transition_speed += 0.5

            # Move title up
            self.title_y -= self.transition_speed

            # Move boat right
            self.boat_x += self.transition_speed

            # Move buttons - alternate left/right
            for i, btn in enumerate(self.buttons):
                if i % 2 == 0:
                    btn.x -= self.transition_speed * 1.5
                else:
                    btn.x += self.transition_speed * 1.5

            # Check if everything is off screen
            if (self.title_y < -100 and
                self.boat_x > SCREEN_WIDTH + 50 and
                all(b.x < -300 or b.x > SCREEN_WIDTH + 50 for b in self.buttons)):
                # Start fading to black
                self.fade_alpha += 10
                if self.fade_alpha >= 255:
                    self.fade_alpha = 255
                    self.transition_done = True
                    return self.transition_target
        else:
            # Update button hover states
            mouse_pos = pygame.mouse.get_pos()
            for btn in self.buttons:
                btn.update(mouse_pos)

        return None

    def draw(self, surface):
        """Draw menu."""
        # Sky
        surface.fill(SKY_BLUE)

        # Water gradient
        for y in range(WATER_SURFACE, SCREEN_HEIGHT):
            ratio = (y - WATER_SURFACE) / (SCREEN_HEIGHT - WATER_SURFACE)
            color = tuple(int(AZURE[i] + (DEEP_BLUE[i] - AZURE[i]) * ratio)
                         for i in range(3))
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))

        # Background elements
        self.background.draw(surface)

        # Boat
        surface.blit(self.boat_image, (self.boat_x, self.boat_y))

        # Title shadow
        shadow = self.title_font.render("Fish-O-Mania", True, (0, 50, 80))
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, self.title_y + 3))
        surface.blit(shadow, shadow_rect)

        # Title
        title = self.title_font.render("Fish-O-Mania", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, self.title_y))
        surface.blit(title, title_rect)

        # Subtitle
        subtitle = self.subtitle_font.render("Cast your line and reel in the fun!",
                                             True, (200, 230, 255))
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, self.title_y + 50))
        surface.blit(subtitle, subtitle_rect)

        # Buttons
        for btn in self.buttons:
            btn.draw(surface)

        # Fade overlay
        if self.fade_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.fade_alpha)
            surface.blit(fade_surf, (0, 0))

    def handle_click(self, mouse_pos):
        """Handle click."""
        for i, btn in enumerate(self.buttons):
            if btn.is_clicked(mouse_pos, True):
                if i == 0:
                    return "classic"
                elif i == 4:
                    return "quit"
        return None


def main():
    """Main menu loop."""
    menu = MainMenu()
    running = True

    while running:
        mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_clicked = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Handle clicks
        if mouse_clicked and not menu.transitioning:
            action = menu.handle_click(pygame.mouse.get_pos())
            if action == "classic":
                menu.start_transition("classic")
            elif action == "quit":
                running = False

        # Update
        result = menu.update()

        if result == "classic":
            print("Launching Classic Mode...")
            pygame.display.set_caption("Fish-O-Mania: Classic Mode")

            from classic_tavish import main as classic_main
            classic_main()

            pygame.display.set_caption("Fish-O-Mania")
            menu = MainMenu()

        # Draw
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()