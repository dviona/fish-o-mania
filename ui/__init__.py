"""
UI Package for Fish-O-Mania.

This package contains user interface components.

Classes:
    Button: Interactive menu button with hover effects.
    MenuScreen: Main menu screen with navigation and transitions.

Usage:
    from ui import Button, MenuScreen

    # Create a button
    btn = Button(100, 100, 200, 50, "Play", enabled=True)

    # Create menu screen
    menu = MenuScreen()
"""

from ui.button import Button
from ui.menu_screen import MenuScreen

__all__ = [
    'Button',
    'MenuScreen',
]