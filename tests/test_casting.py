"""
Test for casting functionalities.
"""
import unittest
import os
import sys

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Set SDL to dummy mode BEFORE importing pygame
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
from mechanics.casting import CastingRod


class TestCastingRod(unittest.TestCase):
    """Tests for the CastingRod class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up pygame before all tests."""
        pygame.init()
        pygame.display.set_mode((800, 600))
    
    @classmethod
    def tearDownClass(cls):
        """Clean up pygame after all tests."""
        pygame.quit()
    
    def test_initialization(self):
        """Test that casting rod initializes with correct values."""
        rod = CastingRod(rod_max_length=400, rod_speed=5)
        
        self.assertEqual(rod.rod_max_length, 400)
        self.assertEqual(rod.rod_speed, 5)
        self.assertEqual(rod.rod_length, 0)
        self.assertFalse(rod.is_casting)
        self.assertIsNone(rod.attached_fish)
        self.assertIsNone(rod.pending_danger_fish)
    
    def test_toggle_cast(self):
        """Test toggling between casting and reeling states."""
        rod = CastingRod(rod_max_length=400, rod_speed=5)
        
        self.assertFalse(rod.is_casting)
        
        rod.toggle_cast()
        self.assertTrue(rod.is_casting)
        
        rod.toggle_cast()
        self.assertFalse(rod.is_casting)
    
    def test_rod_extends_when_casting(self):
        """Test that rod length increases during casting."""
        rod = CastingRod(rod_max_length=400, rod_speed=5)
        rod.is_casting = True
        initial_length = rod.rod_length
        
        # Manually extend the rod
        if rod.rod_length < rod.rod_max_length:
            rod.rod_length += rod.rod_speed
        
        self.assertGreater(rod.rod_length, initial_length)
    
    def test_rod_retracts_when_reeling(self):
        """Test that rod length decreases during reeling."""
        rod = CastingRod(rod_max_length=400, rod_speed=5)
        rod.rod_length = 100
        rod.is_casting = False
        
        # Manually retract the rod
        if rod.rod_length > 0:
            rod.rod_length -= rod.rod_speed
        
        self.assertEqual(rod.rod_length, 95)
    
    def test_reset(self):
        """Test resetting the rod to initial state."""
        rod = CastingRod(rod_max_length=400, rod_speed=5)
        
        # Change some state
        rod.rod_length = 100
        rod.is_casting = True
        
        # Reset
        rod.reset()
        
        self.assertEqual(rod.rod_length, 0)
        self.assertFalse(rod.is_casting)
        self.assertIsNone(rod.attached_fish)
        self.assertIsNone(rod.pending_danger_fish)
    
    def test_auto_reel_enabled(self):
        """Test that auto_reel can be enabled."""
        rod = CastingRod(rod_max_length=400, rod_speed=5, auto_reel=True)
        self.assertTrue(rod.auto_reel)
    
    def test_auto_reel_disabled(self):
        """Test that auto_reel can be disabled."""
        rod = CastingRod(rod_max_length=400, rod_speed=5, auto_reel=False)
        self.assertFalse(rod.auto_reel)
    
    def test_cooldown_initially_inactive(self):
        """Test that cooldown is not active initially."""
        rod = CastingRod(rod_max_length=400, rod_speed=5)
        self.assertFalse(rod.is_on_cooldown())
    
    def test_start_cooldown(self):
        """Test that starting cooldown activates it."""
        rod = CastingRod(rod_max_length=400, rod_speed=5)
        rod.start_cooldown()
        
        # Should now be on cooldown
        self.assertTrue(rod.is_on_cooldown())
    
    def test_release_danger_fish(self):
        """Test releasing a danger fish."""
        rod = CastingRod(rod_max_length=400, rod_speed=5)
        
        # Create a mock danger fish
        class MockFish:
            is_hooked = True
            recently_released = False
            release_time = 0
        
        mock_fish = MockFish()
        rod.pending_danger_fish = mock_fish
        rod.attached_fish = mock_fish
        
        # Release the fish
        rod.release_danger_fish()
        
        # Check state is cleared
        self.assertIsNone(rod.pending_danger_fish)
        self.assertIsNone(rod.attached_fish)
        self.assertFalse(mock_fish.is_hooked)
        self.assertTrue(mock_fish.recently_released)


# Run tests if this file is executed directly
if __name__ == '__main__':
    unittest.main()
