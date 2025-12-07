"""
Audio recording library using PyAudio.

This library provides a simple interface for recording audio input
with support for real-time frame reading and amplitude analysis.

Classes:
    RECORDER: Main class for audio recording operations.

Example:
    >>> from your_library_name import RECORDER
    >>> recorder = RECORDER(channels=1, rate=44100, frames_per_buffer=735)
    >>> recorder.start_recording()
    >>> recorder.read_frames()
    >>> peak = recorder.get_frame_peak()
    >>> recorder.close()

Dependencies:
    - pyaudio
    - numpy
"""

from .Recorder import RECORDER

__all__ = ["RECORDER"]
__version__ = "0.1.0"
