"""
Debbie Tavish Zac and Aradhya

Unit Tests for Time Attack Mode.

This module contains tests for the Time Attack game mode,
including the FastFishManager and game functions.
"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame

# Initialize pygame BEFORE imports that need it
pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.display.set_mode((800, 600))

import unittest

# Import modules to test
from modes.mode_time_attack import (
    load_sounds,
    load_graphics,
    draw_water_background,
    draw_pause_overlay,
    draw_game_over_screen,
    GAME_DURATION,
    INITIAL_FISH_COUNT
)
from fish.fast_fish_manager import FastFishManager, FISH_SPEED_MULTIPLIER
from fish.relaxed_fish_manager import RelaxedFishManager
from mechanics.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WATER_SURFACE,
    SKY_BLUE,
)


# CONSTANTS TESTS

class TestTimeAttackConstants(unittest.TestCase):
    """Tests for Time Attack mode constants"""

    def test_game_duration_is_positive(self):
        """Test that game duration is a positive number"""
        self.assertGreater(GAME_DURATION, 0)

    def test_game_duration_is_reasonable(self):
        """Test that game duration is reasonable (10-120 sec)"""
        self.assertGreaterEqual(GAME_DURATION, 10)
        self.assertLessEqual(GAME_DURATION, 120)

    def test_initial_fish_count_is_positive(self):
        """Test that initial fish count is positive"""
        self.assertGreater(INITIAL_FISH_COUNT, 0)

    def test_fish_speed_multiplier_is_greater_than_one(self):
        """Test that fish speed multiplier increases speed"""
        self.assertGreater(FISH_SPEED_MULTIPLIER, 1.0)


# FAST FISH MANAGER TESTS

class TestFastFishManager(unittest.TestCase):
    """Tests for the FastFishManager class"""

    def test_initialization(self):
        """Test that FastFishManager initializes correctly"""
        manager = FastFishManager()
        self.assertIsInstance(manager, FastFishManager)
        self.assertIsInstance(manager, RelaxedFishManager)

    def test_spawn_fish_returns_fish(self):
        """Test that spawn_fish returns a fish object"""
        manager = FastFishManager()
        fish = manager.spawn_fish()
        self.assertIsNotNone(fish)

    def test_spawn_fish_increases_count(self):
        """Test that spawning fish increases the fish count"""
        manager = FastFishManager()
        initial_count = len(manager.all_fish)
        manager.spawn_fish()
        self.assertEqual(len(manager.all_fish), initial_count + 1)

    def test_spawned_fish_has_multiplied_speed_x(self):
        """Test that spawned fish have increased horizontal speed"""
        manager = FastFishManager()
        fish = manager.spawn_fish()

        # Speed should be multiplied (check absolute value since direction varies)
        self.assertGreaterEqual(abs(fish.speed_x), 0.5 * FISH_SPEED_MULTIPLIER * 0.9)

    def test_spawned_fish_has_multiplied_speed_y(self):
        """Test that spawned fish have increased vertical speed"""
        manager = FastFishManager()
        fish = manager.spawn_fish()

        # Speed_y is randomized, but should be multiplied
        # Original range is -0.5 to 0.5, multiplied by FISH_SPEED_MULTIPLIER
        max_expected = 0.5 * FISH_SPEED_MULTIPLIER
        self.assertLessEqual(abs(fish.speed_y), max_expected + 0.1)

    def test_spawn_multiple_fish(self):
        """Test spawning multiple fish."""
        manager = FastFishManager()
        for i in range(5):
            manager.spawn_fish()
        self.assertEqual(len(manager.all_fish), 5)

    def test_spawn_specific_fish_type_turtle(self):
        """Test spawning a turtle fish type"""
        manager = FastFishManager()
        fish = manager.spawn_fish("turtle")
        self.assertEqual(fish.fish_type, "Turtle")

    def test_spawn_specific_fish_type_danger(self):
        """Test spawning a danger fish type"""
        manager = FastFishManager()
        fish = manager.spawn_fish("danger")
        self.assertEqual(fish.fish_type, "Danger Fish")

    def test_spawn_specific_fish_type_shark(self):
        """Test spawning a shakr fish type"""
        manager = FastFishManager()
        fish = manager.spawn_fish("shark")
        self.assertEqual(fish.fish_type, "Shark")

    def test_spawn_specific_fish_type_octopus(self):
        """Test spawning an octopus fish type"""
        manager = FastFishManager()
        fish = manager.spawn_fish("octopus")
        self.assertEqual(fish.fish_type, "Octopus")

    def test_no_lives_display(self):
        """Test that FastFishManager doesn't use lives system"""
        manager = FastFishManager()
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Should not crash - lives display is skipped
        manager.draw(surface)

    def test_remove_fish_no_penalty(self):
        """Test that removing dagnerfish doesn't cause penalty"""
        manager = FastFishManager()
        fish = manager.spawn_fish("danger")
        result = manager.remove_fish(fish)

        self.assertFalse(result['penalty'])
        self.assertFalse(result['game_over'])

    def test_remove_fish_returns_info(self):
        """Test that remove_fish returns fish information"""
        manager = FastFishManager()
        fish = manager.spawn_fish("turtle")
        result = manager.remove_fish(fish)

        self.assertIn('type', result)
        self.assertIn('value', result)
        self.assertIn('rarity', result)
        self.assertEqual(result['type'], "Turtle")

    def test_clear_all(self):
        """Test that clear_all removes all fish"""
        manager = FastFishManager()
        for i in range(5):
            manager.spawn_fish()

        manager.clear_all()
        self.assertEqual(len(manager.all_fish), 0)

    def test_get_fish_at_position_found(self):
        """Test getting fish at a specific position"""
        manager = FastFishManager()
        fish = manager.spawn_fish()
        position = fish.rect.center

        found_fish = manager.get_fish_at_position(position)
        self.assertEqual(found_fish, fish)

    def test_get_fish_at_position_not_found(self):
        """Test getting fish at empty position returns None"""
        manager = FastFishManager()
        found_fish = manager.get_fish_at_position((-100, -100))
        self.assertIsNone(found_fish)


# LOAD SOUNDS TESTS

class TestLoadSounds(unittest.TestCase):
    """Tests for the load_sounds function"""

    def test_load_sounds_returns_dict(self):
        """Test that load_sounds returns a dictionary"""
        sounds = load_sounds()
        self.assertIsInstance(sounds, dict)

    def test_load_sounds_contains_background(self):
        """Test that sounds dict contains background music"""
        sounds = load_sounds()
        self.assertIn('background_timeattack', sounds)

    def test_load_sounds_contains_casting(self):
        """Test that sounds dict contains casting sound"""
        sounds = load_sounds()
        self.assertIn('casting', sounds)

    def test_sounds_are_sound_objects(self):
        """Test that loaded sounds are pygame Sound objects"""
        sounds = load_sounds()
        for key, sound in sounds.items():
            self.assertIsInstance(sound, pygame.mixer.Sound)


# LOAD GRAPHICS TESTS

class TestLoadGraphics(unittest.TestCase):
    """Tests for the load_graphics function"""

    def test_load_graphics_returns_dict(self):
        """Test that load_graphics returns a dictionary"""
        graphics = load_graphics()
        self.assertIsInstance(graphics, dict)

    def test_load_graphics_contains_boat_image(self):
        """Test that graphics dict contains boat image"""
        graphics = load_graphics()
        self.assertIn('boat_image', graphics)

    def test_load_graphics_contains_boat_position(self):
        """Test that graphics dict contains boat position"""
        graphics = load_graphics()
        self.assertIn('boat_x', graphics)
        self.assertIn('boat_y', graphics)

    def test_load_graphics_contains_hook_image(self):
        """Test that graphics dict contains hook image"""
        graphics = load_graphics()
        self.assertIn('hook_image', graphics)

    def test_load_graphics_contains_hook_rect(self):
        """Test that graphics dict contains hook rect"""
        graphics = load_graphics()
        self.assertIn('hook_rect', graphics)

    def test_boat_image_is_surface(self):
        """Test that boat image is a pygame Surface"""
        graphics = load_graphics()
        self.assertIsInstance(graphics['boat_image'], pygame.Surface)

    def test_hook_image_is_surface(self):
        """Test that hook image is a pygame Surface"""
        graphics = load_graphics()
        self.assertIsInstance(graphics['hook_image'], pygame.Surface)

    def test_hook_rect_is_rect(self):
        """Test that hook rect is a pygame Rect"""
        graphics = load_graphics()
        self.assertIsInstance(graphics['hook_rect'], pygame.Rect)

    def test_boat_position_is_on_screen(self):
        """Test that boat starting position is on screen"""
        graphics = load_graphics()
        self.assertGreaterEqual(graphics['boat_x'], -graphics['boat_image'].get_width())
        self.assertLessEqual(graphics['boat_x'], SCREEN_WIDTH)

    def test_boat_y_near_water_surface(self):
        """Test that boat y position is near water surface"""
        graphics = load_graphics()
        self.assertLess(graphics['boat_y'], WATER_SURFACE)


# DRAW WATER BACKGROUND TESTS

class TestDrawWaterBackground(unittest.TestCase):
    """Tests for the draw_water_background function."""

    def test_draw_water_background_fills_surface(self):
        """Test that background drawing modifies the surface"""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.fill((0, 0, 0))

        # Get color before
        color_before = surface.get_at((SCREEN_WIDTH // 2, 50))

        draw_water_background(surface)

        # Get color after - should be different (sky color)
        color_after = surface.get_at((SCREEN_WIDTH // 2, 50))
        self.assertNotEqual(color_before, color_after)

    def test_water_area_exists(self):
        """Test that water area is drawn below surface"""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        draw_water_background(surface)

        # Check a point in the water area - should not be sky blue
        water_color = surface.get_at((SCREEN_WIDTH // 2, WATER_SURFACE + 100))
        self.assertNotEqual((water_color.r, water_color.g, water_color.b), SKY_BLUE)


# DRAW PAUSE OVERLAY TESTS

class TestDrawPauseOverlay(unittest.TestCase):
    """Tests for the draw_pause_overlay function"""

    def test_draw_pause_overlay_modifies_surface(self):
        """Test that pause overlay modifies the surface"""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.fill((100, 100, 100))

        color_before = surface.get_at((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        draw_pause_overlay(surface, 15.0)
        color_after = surface.get_at((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.assertNotEqual(color_before, color_after)


# DRAW GAME OVER SCREEN TESTS

class TestDrawGameOverScreen(unittest.TestCase):
    """Tests for the draw_game_over_screen function"""

    def test_draw_game_over_screen_with_new_high_score(self):
        """Test game over screen with new high score"""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        high_score_result = {"is_new_high": True, "old_score": 50, "new_score": 100}
        draw_game_over_screen(surface, 100, 5, high_score_result)

    def test_draw_game_over_screen_with_zero_score(self):
        """Test game over screen with zero score"""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        high_score_result = {"is_new_high": False, "old_score": 0, "new_score": 0}
        draw_game_over_screen(surface, 0, 0, high_score_result)

    def test_draw_game_over_screen_with_high_score(self):
        """Test game over screen with very high score"""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        high_score_result = {"is_new_high": True, "old_score": 1000, "new_score": 10000}
        draw_game_over_screen(surface, 10000, 100, high_score_result)

    def test_draw_game_over_screen_modifies_surface(self):
        """Test that game over screen modifies the surface"""
        surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        surface.fill((100, 100, 100))

        color_before = surface.get_at((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        high_score_result = {"is_new_high": False, "old_score": 0, "new_score": 100}
        draw_game_over_screen(surface, 100, 5, high_score_result)
        color_after = surface.get_at((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.assertNotEqual(color_before, color_after)


if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()
