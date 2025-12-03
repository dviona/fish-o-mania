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
from scores import get_all_high_scores


# Initialize pygame
pygame.init()

# Sounds
pygame.mixer.music.load("sounds/ambience_menu.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fish-O-Mania")
clock = pygame.time.Clock()


class Button:
    """Simple menu button with hover and selection effect."""

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
        self.selected = False  # For keyboard navigation

        # Colors
        self.normal_color = (0, 105, 148)
        self.hover_color = (0, 140, 190)
        self.selected_color = (0, 160, 210)  # Brighter for keyboard selection
        self.disabled_color = (80, 80, 100)
        self.border_color = WHITE
        self.selected_border_color = (255, 215, 0)  # Gold border when selected

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
            border_color = self.border_color
        elif self.selected or self.hovered:
            bg_color = self.selected_color if self.selected else self.hover_color
            text_color = WHITE
            border_color = self.selected_border_color if self.selected else self.border_color
        else:
            bg_color = self.normal_color
            text_color = WHITE
            border_color = self.border_color

        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, bg_color, rect, border_radius=10)
        border_width = 4 if self.selected else 3
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=10)

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
        self.title_y = 80

        # Fonts
        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.instruction_font = pygame.font.Font(None, 24)

        # Buttons - positioned higher
        btn_w, btn_h = 250, 50
        btn_x = SCREEN_WIDTH // 2 - btn_w // 2
        start_y = SCREEN_HEIGHT // 2 - 80
        spacing = 60

        self.buttons = [
            Button(btn_x, start_y, btn_w, btn_h, "Classic Mode", True),
            Button(btn_x, start_y + spacing, btn_w, btn_h, "Time Attack", True),
            Button(btn_x, start_y + spacing * 2, btn_w, btn_h, "Endless Mode", True),
            Button(btn_x, start_y + spacing * 3, btn_w, btn_h, "High Scores", True),
            Button(btn_x, start_y + spacing * 4, btn_w, btn_h, "Quit", True),
        ]

        # Keyboard navigation
        self.selected_index = 0
        self.buttons[self.selected_index].selected = True

        # High scores screen state
        self.showing_high_scores = False

        # Transition state
        self.transitioning = False
        self.transition_speed = 0
        self.transition_target = None
        self.transition_done = False
        self.fade_alpha = 0

    def move_selection(self, direction):
        """Move keyboard selection up or down."""
        # Deselect current
        self.buttons[self.selected_index].selected = False

        # Move to next enabled button
        attempts = 0
        while attempts < len(self.buttons):
            self.selected_index = (self.selected_index + direction) % len(self.buttons)
            if self.buttons[self.selected_index].enabled:
                break
            attempts += 1

        # Select new
        self.buttons[self.selected_index].selected = True

    def select_current(self):
        """Activate the currently selected button."""
        if self.buttons[self.selected_index].enabled:
            if self.selected_index == 0:
                return "classic"
            elif self.selected_index == 1:
                return "time_attack"
            elif self.selected_index == 2:
                return "endless"
            elif self.selected_index == 3:
                return "high_scores"
            elif self.selected_index == 4:
                return "quit"
        return None

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

    def draw_high_scores(self, surface):
        """Draw the high scores screen."""
        scores = get_all_high_scores()

        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 30, 60))
        surface.blit(overlay, (0, 0))

        # Title
        title = self.title_font.render("High Scores", True, (255, 215, 0))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))
        surface.blit(title, title_rect)

        # Score entries
        y_pos = 160
        mode_font = pygame.font.Font(None, 40)
        score_font = pygame.font.Font(None, 32)

        modes = [
            ("Classic Mode", "classic"),
            ("Time Attack", "time_attack"),
            ("Endless Mode", "endless")
        ]

        for mode_name, mode_key in modes:
            # Mode name
            mode_text = mode_font.render(mode_name, True, WHITE)
            mode_rect = mode_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
            surface.blit(mode_text, mode_rect)

            # Score
            high_score = scores[mode_key]["high_score"]
            fish_count = scores[mode_key].get("best_fish_count", 0)
            date = scores[mode_key].get("date", "---")

            score_str = f"Score: {high_score}  |  Fish: {fish_count}"
            if mode_key == "endless":
                best_time = scores[mode_key].get("best_time", 0)
                mins = int(best_time // 60)
                secs = int(best_time % 60)
                score_str += f"  |  Best Time: {mins:02d}:{secs:02d}"

            score_text = score_font.render(score_str, True, (180, 200, 220))
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 35))
            surface.blit(score_text, score_rect)

            if date:
                date_text = pygame.font.Font(None, 24).render(f"Set: {date}", True, (120, 140, 160))
                date_rect = date_text.get_rect(center=(SCREEN_WIDTH // 2, y_pos + 60))
                surface.blit(date_text, date_rect)

            y_pos += 110

        # Instructions
        instruction_text = self.instruction_font.render("Press ESC or ENTER to return", True, WHITE)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        surface.blit(instruction_text, instruction_rect)

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

        # Instructions (only when not transitioning)
        if not self.transitioning:
            instructions = self.instruction_font.render(
                "UP/DOWN to navigate, ENTER to select", True, WHITE)
            instructions_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 125))
            surface.blit(instructions, instructions_rect)

        # Fade overlay
        if self.fade_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.fade_alpha)
            surface.blit(fade_surf, (0, 0))

        # Draw high scores screen on top if active
        if self.showing_high_scores:
            self.draw_high_scores(surface)

    def handle_click(self, mouse_pos):
        """Handle click."""
        for i, btn in enumerate(self.buttons):
            if btn.is_clicked(mouse_pos, True):
                if i == 0:
                    return "classic"
                elif i == 1:
                    return "time_attack"
                elif i == 2:
                    return "endless"
                elif i == 3:
                    return "high_scores"
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
                    if menu.showing_high_scores:
                        menu.showing_high_scores = False
                    else:
                        running = False
                elif not menu.transitioning:
                    # If showing high scores, close on any key
                    if menu.showing_high_scores:
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
                                menu.start_transition(action)
                            elif action == "high_scores":
                                menu.showing_high_scores = True
                            elif action == "quit":
                                running = False

        # Handle mouse clicks
        if mouse_clicked and not menu.transitioning and not menu.showing_high_scores:
            action = menu.handle_click(pygame.mouse.get_pos())
            if action in ["classic", "time_attack", "endless"]:
                pygame.mixer.music.stop()
                menu.start_transition(action)
            elif action == "high_scores":
                menu.showing_high_scores = True
            elif action == "quit":
                running = False
        

        # Update
        result = menu.update()

        if result == "classic":
            print("Launching Classic Mode...")
            pygame.display.set_caption("Fish-O-Mania: Classic Mode")
            from mode_classic import main as classic_main
            classic_main()
            pygame.display.set_caption("Fish-O-Mania")
            menu = MainMenu()

        elif result == "time_attack":
            print("Launching Time Attack...")
            pygame.display.set_caption("Fish-O-Mania: Time Attack")
            from mode_time_attack import main as time_attack_main
            time_attack_main()
            pygame.display.set_caption("Fish-O-Mania")
            menu = MainMenu()

        elif result == "endless":
            print("Launching Endless Mode...")
            pygame.display.set_caption("Fish-O-Mania: Endless Mode")
            from mode_endless import main as endless_main
            endless_main()
            pygame.display.set_caption("Fish-O-Mania")
            menu = MainMenu()

        # Draw
        menu.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        

    # Cleanup
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
