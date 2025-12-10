"""
Debbie Tavish Zac and Aradhya

Unit tests for Time Attack Mode.
"""
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame

# Initialize pygame BEFORE imports that need it
pygame.init()
pygame.mixer.init()
pygame.display.set_mode((800, 600))

import unittest
from modes.mode_time_attack import (
    GAME_DURATION,
    INITIAL_FISH_COUNT,
    load_sounds,
    load_graphics,
    handle_danger_fish_catch,
)
from fish.fast_fish_manager import FastFishManager
from mechanics.casting import CastingRod


class TestTimeAttackConstants(unittest.TestCase):
    """Tests for Time Attack mode constants."""

    def test_game_duration_is_30(self):
        """Test that GAME_DURATION is 30 seconds."""
        self.assertEqual(GAME_DURATION, 30)

    def test_initial_fish_count_is_8(self):
        """Test that INITIAL_FISH_COUNT is 8."""
        self.assertEqual(INITIAL_FISH_COUNT, 8)


class TestLoadSounds(unittest.TestCase):
    """Tests for load_sounds function."""

    def test_load_sounds_returns_dict_with_required_keys(self):
        """Test that load_sounds returns dictionary with required keys."""
        sounds = load_sounds()
        self.assertIsInstance(sounds, dict)
        self.assertIn('background_timeattack', sounds)
        self.assertIn('casting', sounds)


class TestLoadGraphics(unittest.TestCase):
    """Tests for load_graphics function."""

    def test_load_graphics_returns_dict_with_required_keys(self):
        """Test that load_graphics returns dictionary with required keys."""
        graphics = load_graphics()
        self.assertIsInstance(graphics, dict)
        self.assertIn('boat_image', graphics)
        self.assertIn('boat_x', graphics)
        self.assertIn('boat_y', graphics)
        self.assertIn('hook_image', graphics)
        self.assertIn('hook_rect', graphics)


class TestHandleDangerFishCatch(unittest.TestCase):
    """Tests for handle_danger_fish_catch function."""

    def test_returns_none_when_no_pending_fish(self):
        """Test that function returns None when no danger fish pending."""
        fish_manager = FastFishManager()
        casting_manager = CastingRod(200, 5)
        casting_manager.pending_danger_fish = None

        result = handle_danger_fish_catch(casting_manager, fish_manager)
        self.assertIsNone(result)

    def test_returns_fish_info_with_penalty_true(self):
        """Test that function returns fish info with penalty=True."""
        fish_manager = FastFishManager()
        casting_manager = CastingRod(200, 5)

        # Spawn a danger fish and set it as pending
        fish = fish_manager.spawn_fish("danger")
        casting_manager.pending_danger_fish = fish

        result = handle_danger_fish_catch(casting_manager, fish_manager)
        self.assertIsNotNone(result)
        self.assertTrue(result["penalty"])

    def test_clears_pending_state(self):
        """Test that function clears pending_danger_fish and attached_fish."""
        fish_manager = FastFishManager()
        casting_manager = CastingRod(200, 5)

        fish = fish_manager.spawn_fish("danger")
        casting_manager.pending_danger_fish = fish
        casting_manager.attached_fish = fish

        handle_danger_fish_catch(casting_manager, fish_manager)

        self.assertIsNone(casting_manager.pending_danger_fish)
        self.assertIsNone(casting_manager.attached_fish)

    def test_adds_to_recent_catches(self):
        """Test that caught fish is added to recent_catches."""
        fish_manager = FastFishManager()
        fish_manager.recent_catches = []
        casting_manager = CastingRod(200, 5)

        fish = fish_manager.spawn_fish("danger")
        casting_manager.pending_danger_fish = fish

        handle_danger_fish_catch(casting_manager, fish_manager)

        self.assertEqual(len(fish_manager.recent_catches), 1)


class TestTimerLogic(unittest.TestCase):
    """Tests for timer-related logic."""

    def test_time_remaining_cannot_go_below_zero(self):
        """Test that time_remaining calculation cannot be negative."""
        # Simulate elapsed time greater than GAME_DURATION
        elapsed = 35  # 35 seconds elapsed, but game is only 30 seconds
        time_remaining = max(0, GAME_DURATION - elapsed)
        self.assertEqual(time_remaining, 0)

    def test_game_over_triggers_when_time_exceeds_duration(self):
        """Test that game_over becomes True when elapsed time exceeds GAME_DURATION."""
        # Simulate game state
        game_over = False
        elapsed = 31  # More than 30 seconds
        time_remaining = max(0, GAME_DURATION - elapsed)

        if time_remaining <= 0:
            game_over = True

        self.assertTrue(game_over)


if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()
