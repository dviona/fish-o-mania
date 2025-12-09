"""
Menu Screen module: contains the MenuScreen class for the game's main menu
Handles keyboard and mouse navigation, high scores display,
and animated exit transitions to game modes.
"""

import pygame
from mechanics.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    SKY_BLUE,
    AZURE,
    DEEP_BLUE,
    WATER_SURFACE
)
from background import BackgroundManager
from mechanics.scores import get_all_high_scores
from ui.button import Button


class MenuScreen:
    """
    Main menu

    Attributes:
        background (BackgroundManager): Animated background.
        buttons (list): List of menu Button objects.
        selected_index (int): Currently selected button index.
        showing_high_scores (bool): Whether high scores overlay is shown.
        transitioning (bool): Whether exit transition is playing.
    """

    def __init__(self):
        # Initialize menu screen
        self.background = BackgroundManager(use_terrain_files=True)

        # Load Sounds
        pygame.mixer.music.load("sounds/ambience_menu.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

        # Load or create boat image
        self._load_boat_image()

        # Position settings
        self.boat_x = SCREEN_WIDTH // 2 - 155
        self.boat_y = WATER_SURFACE - 130
        self.title_y = 80

        # Fonts
        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 32)
        self.instruction_font = pygame.font.Font(None, 24)

        # Create menu buttons
        self._create_buttons()

        # Navigation state
        self.selected_index = 0
        self.buttons[self.selected_index].selected = True

        # Screen states
        self.showing_high_scores = False
        self.transitioning = False
        self.transition_speed = 0
        self.transition_target = None
        self.transition_done = False
        self.fade_alpha = 0

    def _load_boat_image(self):
        # Load boat image or create placeholder
        try:
            self.boat_image = pygame.image.load(
                "graphics/boat.png"
            ).convert_alpha()
            self.boat_image = pygame.transform.scale(
                self.boat_image, (310, 260)
            )
        except pygame.error:
            # Create placeholder boat shape
            self.boat_image = pygame.Surface((310, 260), pygame.SRCALPHA)
            pygame.draw.polygon(
                self.boat_image,
                (139, 90, 43),
                [(50, 200), (260, 200), (230, 250), (80, 250)]
            )

    def _create_buttons(self):
        # Create menu buttons
        btn_width = 250
        btn_height = 50
        btn_x = SCREEN_WIDTH // 2 - btn_width // 2
        start_y = SCREEN_HEIGHT // 2 - 80
        spacing = 60

        self.buttons = [
            Button(btn_x, start_y, btn_width, btn_height,
                   "Classic Mode", True),
            Button(btn_x, start_y + spacing, btn_width, btn_height,
                   "Time Attack", True),
            Button(btn_x, start_y + spacing * 2, btn_width, btn_height,
                   "Endless Mode", True),
            Button(btn_x, start_y + spacing * 3, btn_width, btn_height,
                   "High Scores", True),
            Button(btn_x, start_y + spacing * 4, btn_width, btn_height,
                   "Quit", True),
        ]

    def move_selection(self, direction):
        """
        Move keyboard selection up or down.

        Args:
            direction (int): -1 for up, 1 for down.
        """
        # Deselect current button
        self.buttons[self.selected_index].selected = False

        # Find next enabled button
        attempts = 0
        while attempts < len(self.buttons):
            self.selected_index = (
                (self.selected_index + direction) % len(self.buttons)
            )
            if self.buttons[self.selected_index].enabled:
                break
            attempts += 1

        # Select new button
        self.buttons[self.selected_index].selected = True

    def select_current(self):
        """
        Activate the currently selected button.

        Returns:
            str: Action name, or None if button disabled.
        """
        if not self.buttons[self.selected_index].enabled:
            return None

        actions = ["classic", "time_attack", "endless", "high_scores", "quit"]
        return actions[self.selected_index]

    def start_transition(self, target):
        """
        Start the exit transition animation.

        Args:
            target (str): Target game mode to launch after transition.
        """
        self.transitioning = True
        self.transition_target = target
        self.transition_speed = 2

    def update(self):
        """
        Update menu state and animations.

        Returns:
            str: Target mode when transition completes, None otherwise.
        """
        self.background.update()

        if self.transitioning:
            return self._update_transition()
        else:
            # Update button hover states
            mouse_pos = pygame.mouse.get_pos()
            for btn in self.buttons:
                btn.update(mouse_pos)

        return None

    def _update_transition(self):
        """
        Update the exit transition animation.

        Returns:
            str: Target mode when complete, None otherwise.
        """
        # Accelerate transition
        self.transition_speed += 0.5

        # Animate elements off screen
        self.title_y -= self.transition_speed
        self.boat_x += self.transition_speed

        # Move buttons (alternating directions)
        for i, btn in enumerate(self.buttons):
            if i % 2 == 0:
                btn.x -= self.transition_speed * 1.5
            else:
                btn.x += self.transition_speed * 1.5

        # Check if all elements are off screen
        all_offscreen = (
            self.title_y < -100 and
            self.boat_x > SCREEN_WIDTH + 50 and
            all(b.x < -300 or b.x > SCREEN_WIDTH + 50 for b in self.buttons)
        )

        if all_offscreen:
            # Fade to black
            self.fade_alpha += 10
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.transition_done = True
                return self.transition_target

        return None

    def draw_high_scores(self, surface):
        """
        Draw the high scores overlay screen.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
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
        date_font = pygame.font.Font(None, 24)

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

            # Score details
            high_score = scores[mode_key]["high_score"]
            fish_count = scores[mode_key].get("best_fish_count", 0)
            date = scores[mode_key].get("date", "---")

            score_str = f"Score: {high_score}  |  Fish: {fish_count}"

            # Add time for endless mode
            if mode_key == "endless":
                best_time = scores[mode_key].get("best_time", 0)
                mins = int(best_time // 60)
                secs = int(best_time % 60)
                score_str += f"  |  Best Time: {mins:02d}:{secs:02d}"

            score_text = score_font.render(score_str, True, (180, 200, 220))
            score_rect = score_text.get_rect(
                center=(SCREEN_WIDTH // 2, y_pos + 35)
            )
            surface.blit(score_text, score_rect)

            # Date achieved
            if date:
                date_text = date_font.render(
                    f"Set: {date}", True, (120, 140, 160)
                )
                date_rect = date_text.get_rect(
                    center=(SCREEN_WIDTH // 2, y_pos + 60)
                )
                surface.blit(date_text, date_rect)

            y_pos += 110

        # Instructions
        instruction_text = self.instruction_font.render(
            "Press ESC or ENTER to return", True, WHITE
        )
        instruction_rect = instruction_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        )
        surface.blit(instruction_text, instruction_rect)

    def draw(self, surface):
        """
        Draw the main menu.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        # Sky background
        surface.fill(SKY_BLUE)

        # Water gradient
        for y in range(WATER_SURFACE, SCREEN_HEIGHT):
            ratio = (y - WATER_SURFACE) / (SCREEN_HEIGHT - WATER_SURFACE)
            color = tuple(
                int(AZURE[i] + (DEEP_BLUE[i] - AZURE[i]) * ratio)
                for i in range(3)
            )
            pygame.draw.line(surface, color, (0, y), (SCREEN_WIDTH, y))

        # Background elements
        self.background.draw(surface)

        # Boat
        surface.blit(self.boat_image, (self.boat_x, self.boat_y))

        # Title shadow
        shadow = self.title_font.render("Fish-O-Mania", True, (0, 50, 80))
        shadow_rect = shadow.get_rect(
            center=(SCREEN_WIDTH // 2 + 3, self.title_y + 3)
        )
        surface.blit(shadow, shadow_rect)

        # Title
        title = self.title_font.render("Fish-O-Mania", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, self.title_y))
        surface.blit(title, title_rect)

        # Subtitle
        subtitle = self.subtitle_font.render(
            "Cast your line and reel in the fun!",
            True,
            (200, 230, 255)
        )
        subtitle_rect = subtitle.get_rect(
            center=(SCREEN_WIDTH // 2, self.title_y + 50)
        )
        surface.blit(subtitle, subtitle_rect)

        # Buttons
        for btn in self.buttons:
            btn.draw(surface)

        # Navigation instructions (hide during transition)
        if not self.transitioning:
            instructions = self.instruction_font.render(
                "UP/DOWN to navigate, ENTER to select",
                True,
                (180, 200, 220)
            )
            instructions_rect = instructions.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30)
            )
            surface.blit(instructions, instructions_rect)

        # Fade overlay
        if self.fade_alpha > 0:
            fade_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade_surf.fill((0, 0, 0))
            fade_surf.set_alpha(self.fade_alpha)
            surface.blit(fade_surf, (0, 0))

        # High scores overlay (on top of everything)
        if self.showing_high_scores:
            self.draw_high_scores(surface)

    def handle_click(self, mouse_pos):
        """
        Handle mouse click on menu.

        Args:
            mouse_pos (tuple): Mouse position when clicked.

        Returns:
            str: Action name if button clicked, None otherwise.
        """
        actions = ["classic", "time_attack", "endless", "high_scores", "quit"]

        for i, btn in enumerate(self.buttons):
            if btn.is_clicked(mouse_pos, True):
                return actions[i]

        return None
