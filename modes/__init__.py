"""
Game Modes Package for Fish-O-Mania.

This package contains all playable game modes.

Modules:
    mode_classic: Standard mode with lives system.
    mode_time_attack: Race against the clock.
    mode_endless: Relaxed mode with no penalties.

Usage:
    from modes import mode_classic, mode_time_attack, mode_endless

    # Launch a mode
    mode_classic.main()
    mode_time_attack.main()
    mode_endless.main()
"""

from modes import mode_classic
from modes import mode_time_attack
from modes import mode_endless

__all__ = [
    'mode_classic',
    'mode_time_attack',
    'mode_endless',
]