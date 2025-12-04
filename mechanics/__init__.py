"""
Mechanics Package for Fish-O-Mania.

This package contains game mechanics including casting, lives, and scoring.

Modules:
    constants: Game configuration values.
    casting: Fishing rod mechanics.
    lives_manager: Player lives system.
    scores: High score persistence.

Usage:
    from mechanics import CastingRod, LivesManager
    from mechanics.constants import SCREEN_WIDTH, FPS
    from mechanics.scores import update_high_score
"""

from mechanics.casting import CastingRod
from mechanics.lives_manager import LivesManager
from mechanics.scores import (
    get_default_scores,
    load_scores,
    save_scores,
    update_high_score,
    get_high_score,
    get_all_high_scores,
    reset_scores
)

__all__ = [
    'CastingRod',
    'LivesManager',
    'get_default_scores',
    'load_scores',
    'save_scores',
    'update_high_score',
    'get_high_score',
    'get_all_high_scores',
    'reset_scores',
]