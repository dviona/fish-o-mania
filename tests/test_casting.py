"""

Test for casting functionalities.

"""
import unittest
import pygame

pygame.init()

from mechanics.casting import CastingRod

class TestCastingRod(unittest.TestCase):
    """Tests for the CastingRod class."""

    def test_initialization(self):
        """Test that casting rod initializes with correct values."""
        rod = CastingRod(length=10)
        self.assertEqual(rod.length, 10)
        self.assertEqual(rod.material, 'carbon fiber')
        self.assertFalse(rod.is_casting)

    def test_toggle_cast(self):
        """Test toggling between casting and reeling states."""
        rod = CastingRod(length=10)
        rod.toggle_cast()
        self.assertTrue(rod.is_casting)
        rod.toggle_cast()
        self.assertFalse(rod.is_casting)


    def test_update(self):
        """Test updating the rod state."""
        rod = CastingRod(length=10)
        rod.toggle_cast()  # Start casting
        rod.update()
        self.assertEqual(rod.length, 11)  # Length should increase

        rod.toggle_cast()  # Start reeling
        rod.update()
        self.assertEqual(rod.length, 10)  # Length should decrease  

    def test_reset(self):
        """Test resetting the rod to initial state."""
        rod = CastingRod(length=10)
        rod.toggle_cast()
        rod.update()
        rod.reset()
        self.assertEqual(rod.length, 10)
        self.assertFalse(rod.is_casting)  