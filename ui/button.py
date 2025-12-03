"""
Button Module for Fish-O-Mania.

This module contains the Button class for interactive menu buttons.
"""

import pygame
from mechanics.constants import WHITE


class Button:
    """
    Interactive menu button with hover and selection effects.

    Supports both mouse hover and keyboard navigation highlighting.

    Attributes:
        x (int): Current X-coordinate (may animate).
        y (int): Current Y-coordinate (may animate).
        base_x (int): Original X-coordinate for reset.
        base_y (int): Original Y-coordinate for reset.
        width (int): Button width in pixels.
        height (int): Button height in pixels.
        text (str): Button label text.
        enabled (bool): Whether button is interactive.
        hovered (bool): Mouse hover state.
        selected (bool): Keyboard selection state.
    """

    def __init__(self, x, y, width, height, text, enabled=True):
        """
        Initialize a menu button.

        Args:
            x (int): X-coordinate for button.
            y (int): Y-coordinate for button.
            width (int): Button width.
            height (int): Button height.
            text (str): Button label.
            enabled (bool): Whether button is clickable.
        """
        self.base_x = x
        self.base_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.enabled = enabled
        self.hovered = False
        self.selected = False

        # Color scheme
        self.normal_color = (0, 105, 148)
        self.hover_color = (0, 140, 190)
        self.selected_color = (0, 160, 210)
        self.disabled_color = (80, 80, 100)
        self.border_color = WHITE
        self.selected_border_color = (255, 215, 0)  # Gold

        self.font = pygame.font.Font(None, 36)

    def update(self, mouse_pos):
        """
        Update hover state based on mouse position.

        Args:
            mouse_pos (tuple): Current mouse (x, y) position.
        """
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hovered = rect.collidepoint(mouse_pos) and self.enabled

    def draw(self, surface):
        """
        Draw the button on the given surface.

        Args:
            surface (pygame.Surface): Surface to draw on.
        """
        # Determine colors based on state
        if not self.enabled:
            bg_color = self.disabled_color
            text_color = (150, 150, 150)
            border_color = self.border_color
        elif self.selected or self.hovered:
            bg_color = self.selected_color if self.selected else self.hover_color
            text_color = WHITE
            border_color = (
                self.selected_border_color if self.selected
                else self.border_color
            )
        else:
            bg_color = self.normal_color
            text_color = WHITE
            border_color = self.border_color

        # Draw button rectangle
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, bg_color, rect, border_radius=10)

        # Draw border (thicker when selected)
        border_width = 4 if self.selected else 3
        pygame.draw.rect(
            surface, border_color, rect, border_width, border_radius=10
        )

        # Draw button text
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)

        # Draw "Coming Soon" label for disabled buttons
        if not self.enabled:
            small_font = pygame.font.Font(None, 20)
            soon_text = small_font.render("Coming Soon", True, (200, 200, 100))
            soon_rect = soon_text.get_rect(
                center=(rect.centerx, rect.bottom + 12)
            )
            surface.blit(soon_text, soon_rect)

    def is_clicked(self, mouse_pos, mouse_clicked):
        """
        Check if the button was clicked.

        Args:
            mouse_pos (tuple): Current mouse position.
            mouse_clicked (bool): Whether mouse button was pressed.

        Returns:
            bool: True if button was clicked while enabled.
        """
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return self.enabled and rect.collidepoint(mouse_pos) and mouse_clicked