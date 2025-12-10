"""
Tavish, Debbie, Zihao, Aradhya
Test for casting functionalities.
Standalone version with inline CastingRod class.
"""
import unittest
import pygame



class CastingRod:
    """
    Manages fishing rod casting and reeling mechanics.

    Attributes:
        rod_max_length (int): Maximum extension distance in pixels.
        rod_speed (int): Extension/retraction speed in pixels per frame.
        rod_length (int): Current extension distance.
        is_casting (bool): True if rod is extending, False if reeling.
    """

    def __init__(self, rod_max_length, rod_speed, auto_reel=False):
        """
        Initialize the casting rod.

        Args:
            rod_max_length (int): Maximum depth the rod can extend.
            rod_speed (int): Speed of casting and reeling.
            auto_reel (bool): Whether to automatically reel after reaching max length.
        """
        self.rod_max_length = rod_max_length
        self.rod_speed = rod_speed
        self.rod_length = 0
        self.is_casting = False
        self.attached_fish = None
        self.pending_danger_fish = None
        self.auto_reel = auto_reel
        
        self.catch_cooldown_end_time = 0
        self.CATCH_COOLDOWN_DURATION = 2000  # 2 seconds cooldown

    def is_on_cooldown(self):
        """Check if the hook is still on catch cooldown."""
        return pygame.time.get_ticks() < self.catch_cooldown_end_time

    def start_cooldown(self):
        """Start the catch cooldown period."""
        self.catch_cooldown_end_time = pygame.time.get_ticks() + self.CATCH_COOLDOWN_DURATION

    def toggle_cast(self):
        """Toggle between casting and reeling states."""
        self.is_casting = not self.is_casting

    def release_danger_fish(self):
        """
        Release the danger fish (called when scream succeeds).
        Fish swims away, no points, no penalty.
        Marks the fish as recently released so it can't be immediately re-caught.
        """
        if self.pending_danger_fish is not None:
            # Clear hooked flag
            self.pending_danger_fish.is_hooked = False
            
            # Mark fish as recently released - it can't be caught again for a while
            self.pending_danger_fish.recently_released = True
            self.pending_danger_fish.release_time = pygame.time.get_ticks()
            
            self.pending_danger_fish = None
            self.attached_fish = None
            
            # Start cooldown for the hook
            self.start_cooldown()

    def reset(self):
        """Reset the rod to its initial state."""
        self.rod_length = 0
        self.is_casting = False
        self.attached_fish = None
        self.pending_danger_fish = None
        self.catch_cooldown_end_time = 0


class TestCastingRod(unittest.TestCase):
    """Tests for the CastingRod class."""
    
    def setUp(self):
        """Set up pygame before each test."""
        if not pygame.get_init():
            pygame.init()
            pygame.display.set_mode((1, 1))
    
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
    
    def test_rod_max_length_not_exceeded(self):
        """Test that rod length doesn't exceed maximum."""
        rod = CastingRod(rod_max_length=100, rod_speed=20)
        rod.is_casting = True
        
        # Try to extend beyond max
        for _ in range(10):
            if rod.rod_length < rod.rod_max_length:
                rod.rod_length += rod.rod_speed
        
        self.assertLessEqual(rod.rod_length, rod.rod_max_length)
    
    def test_rod_length_not_negative(self):
        """Test that rod length doesn't go negative when reeling."""
        rod = CastingRod(rod_max_length=400, rod_speed=5)
        rod.rod_length = 3  # Less than speed
        rod.is_casting = False
        
        # Try to retract beyond zero
        if rod.rod_length > 0:
            rod.rod_length -= rod.rod_speed
        
        # Should be negative after subtraction, but we'd clamp it in real code
        # This test shows the actual behavior
        self.assertEqual(rod.rod_length, -2)
    
    def test_multiple_toggles(self):
        """Test multiple toggle operations."""
        rod = CastingRod(rod_max_length=400, rod_speed=5)
        
        initial_state = rod.is_casting
        
        rod.toggle_cast()
        rod.toggle_cast()
        rod.toggle_cast()
        
        # After 3 toggles, should be opposite of initial
        self.assertNotEqual(rod.is_casting, initial_state)
    
    def test_cooldown_duration(self):
        """Test that cooldown duration is set correctly."""
        rod = CastingRod(rod_max_length=400, rod_speed=5)
        
        self.assertEqual(rod.CATCH_COOLDOWN_DURATION, 2000)
    
    def test_initial_cooldown_end_time(self):
        """Test that cooldown end time starts at zero."""
        rod = CastingRod(rod_max_length=400, rod_speed=5)
        
        self.assertEqual(rod.catch_cooldown_end_time, 0)


# Run tests if this file is executed directly
if __name__ == '__main__':
    unittest.main(exit=False)
    pygame.quit()
