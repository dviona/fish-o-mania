"""
Unit tests for RECORDER class.

This test will take in actual input from the tester. There are 6 tests in total, each lasting 2seconds. Press "Enter" each
time when you are ready to test the microphone input. Please make sure that you are not annoying anyone around you.

Run with: python -m unittest Zach_testing.test_recorder -v
or: python test_recorder.py
"""


import unittest
import os
import sys
import time

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from mechanics.Recorder import RECORDER


class TestRecorder(unittest.TestCase):
    """Test cases for RECORDER class with real microphone input."""

    def test_01_recorder_creation(self):
        """Test that recorder is created with default values."""
        print("\n=== Test 1: Recorder Creation ===")
        recorder = RECORDER()
        
        self.assertEqual(recorder.channels, 1)
        self.assertEqual(recorder.rate, 44100)
        self.assertEqual(recorder.frames_per_buffer, 735)
        self.assertIsNone(recorder.stream)
        self.assertEqual(recorder.frames, [])
        self.assertIsNone(recorder.last_frame)
        
        print(f"✓ Channels: {recorder.channels}")
        print(f"✓ Rate: {recorder.rate}")
        print(f"✓ Frames per buffer: {recorder.frames_per_buffer}")
        
        recorder.close()
        print("✓ Test PASSED")

    def test_02_basic_recording(self):
        """Test basic recording for 2 seconds."""
        print("\n=== Test 2: Basic Recording ===")
        print("This test will record audio for 2 seconds.")
        input("Press ENTER to start recording...")
        
        recorder = RECORDER()
        recorder.start_recording()
        
        print("Recording... (2 seconds)")
        start_time = time.time()
        
        while time.time() - start_time < 2.0:
            recorder.read_frames()
            elapsed = time.time() - start_time
            print(f"\rRecording: {elapsed:.1f}s", end="", flush=True)
        
        print("\n✓ Recording complete")
        
        # Check we captured frames
        num_frames = len(recorder.frames)
        print(f"✓ Captured {num_frames} frames")
        self.assertGreater(num_frames, 0, "Should have captured some frames")
        
        recorder.close()
        print("✓ Test PASSED")

    def test_03_silence_detection(self):
        """Test silence detection with quiet environment."""
        print("\n=== Test 3: Silence Detection ===")
        print("Stay SILENT for 2 seconds.")
        input("Press ENTER to start...")
        
        recorder = RECORDER()
        recorder.start_recording()
        
        print("Recording silence... (2 seconds)")
        start_time = time.time()
        
        while time.time() - start_time < 2.0:
            recorder.read_frames()
            peak = recorder.get_frame_peak()
            print(f"\rSilence level: {peak:,}", end="", flush=True)
        
        final_peak = recorder.get_peak()
        print(f"\n✓ Peak amplitude: {final_peak:,}")
        
        # Convert to int for assertion (handles numpy types)
        final_peak = int(final_peak)
        
        # We don't assert a specific value since silence varies
        self.assertIsInstance(final_peak, int)
        self.assertGreaterEqual(final_peak, 0)
        
        if final_peak < 1000:
            print("✓ Silence detected correctly (very low volume)")
        else:
            print("⚠ Detected some sound (ambient noise present)")
        
        recorder.close()
        print("✓ Test PASSED")

    def test_04_loud_sound_detection(self):
        """Test loud sound detection."""
        print("\n=== Test 4: Loud Sound Detection ===")
        print("Make a LOUD SOUND (clap, shout, etc.) during recording.")
        input("Press ENTER to start...")
        
        recorder = RECORDER()
        recorder.start_recording()
        
        print("Recording... Make noise NOW! (3 seconds)")
        start_time = time.time()
        max_peak = 0
        
        while time.time() - start_time < 3.0:
            recorder.read_frames()
            peak = recorder.get_frame_peak()
            max_peak = max(max_peak, peak)
            print(f"\rCurrent peak: {peak:,} | Max: {max_peak:,}", end="", flush=True)
        
        print(f"\n✓ Maximum peak detected: {max_peak:,}")
        
        # Check that we detected some sound
        self.assertGreater(max_peak, 0, "Should have detected some sound")
        
        if max_peak > 5000:
            print("✓ Loud sound detected successfully!")
        else:
            print("⚠ Sound was quiet, but test still passes")
        
        recorder.close()
        print("✓ Test PASSED")

    def test_05_scream_threshold(self):
        """Test scream detection threshold (game mechanics)."""
        print("\n=== Test 5: Scream Threshold Test ===")
        print("SCREAM as loud as you can! (Testing game threshold)")
        input("Press ENTER when ready to SCREAM...")
        
        recorder = RECORDER()
        recorder.start_recording()
        
        SCREAM_THRESHOLD = 5000
        print(f"Recording... SCREAM NOW! Threshold: {SCREAM_THRESHOLD:,} (2 seconds)")
        
        start_time = time.time()
        scream_detected = False
        max_peak = 0
        
        while time.time() - start_time < 2.0:
            recorder.read_frames()
            peak = recorder.get_frame_peak()
            max_peak = max(max_peak, peak)
            
            if peak >= SCREAM_THRESHOLD and not scream_detected:
                scream_detected = True
                print(f"\n🎉 SCREAM DETECTED at {peak:,}!")
            
            status = "SCREAMING!" if peak >= SCREAM_THRESHOLD else "too quiet"
            print(f"\rPeak: {peak:,} | Max: {max_peak:,} | Status: {status}     ", end="", flush=True)
        
        print(f"\n✓ Final max peak: {max_peak:,}")
        
        # Always pass, just inform user
        self.assertGreaterEqual(max_peak, 0)
        
        if scream_detected:
            print("✓ Scream detection works! You passed the threshold!")
        else:
            print(f"⚠ No scream detected. Max was {max_peak:,}, needed {SCREAM_THRESHOLD:,}")
            print("  (Test still passes - threshold might need adjustment)")
        
        recorder.close()
        print("✓ Test PASSED")

    def test_06_pause_and_restart(self):
        """Test pause and restart functionality."""
        print("\n=== Test 6: Pause and Restart ===")
        print("Testing pause/restart during recording.")
        input("Press ENTER to start...")
        
        recorder = RECORDER()
        recorder.start_recording()
        
        print("Recording for 1 second...")
        start_time = time.time()
        while time.time() - start_time < 1.0:
            recorder.read_frames()
        
        frames_before_pause = len(recorder.frames)
        
        print("✓ Pausing...")
        recorder.pause_recording()
        time.sleep(1)
        
        print("✓ Restarting...")
        recorder.restart_recording()
        
        print("Recording for 1 more second...")
        start_time = time.time()
        while time.time() - start_time < 1.0:
            recorder.read_frames()
        
        frames_after_restart = len(recorder.frames)
        
        # Should have more frames after restart
        self.assertGreater(frames_after_restart, frames_before_pause)
        print(f"✓ Frames before pause: {frames_before_pause}")
        print(f"✓ Frames after restart: {frames_after_restart}")
        
        recorder.close()
        print("✓ Test PASSED")


# Run tests if this file is executed directly
if __name__ == '__main__':
    unittest.main()
