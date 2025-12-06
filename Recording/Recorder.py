import pyaudio
import numpy as np
import time

class RECORDER:
    # fpb equals frames_per_buffer,
    # most common setup
    # FPB = 735, FORMAT = pyaudio.paInt16, CHANNELS = 1, RATE = 16000
    def __init__(self, channels=1, rate=44100, frames_per_buffer=735):
        self.p = pyaudio.PyAudio()
        self.channels = channels
        self.frames_per_buffer = frames_per_buffer
        self.rate = rate
        self.stream = None
        self.frames = []
        self.last_frame = None  # Store the most recent frame

    def start_recording(self):
        if self.stream is None:
            self.stream = self.p.open(format=pyaudio.paInt16,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
            self.frames = []
            self.last_frame = None
            # get the active state of the stream
        if not self.stream.is_active():
            self.stream.start_stream()
        data = self.stream.read(self.frames_per_buffer, exception_on_overflow= False)
        self.frames.append(data)
        self.last_frame = data

    def pause_recording(self):
        if self.stream is not None and self.stream.is_active():
            self.stream.stop_stream()

    def restart_recording(self):
        if self.stream is not None and not self.stream.is_active():
            self.stream.start_stream()

    # this one stops the recorder entirely and clear the stream object
    def close(self):
        if self.stream is not None:
            if self.stream.is_active():
                self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.p.terminate()

    def read_frames(self):
        if self.stream is not None and self.stream.is_active():
            data = self.stream.read(self.frames_per_buffer, exception_on_overflow = False)
            self.frames.append(data)
            self.last_frame = data  # Store as most recent frame
            return data
        return None

    def get_samples(self):
        return b"".join(self.frames)

    def get_peak(self):
        """Get peak amplitude from all accumulated frames."""
        sample_bytes = self.get_samples()
        if not sample_bytes:
            return 0
        audio_data = np.frombuffer(sample_bytes, dtype = np.int16)
        peak = np.max(np.abs(audio_data))
        return peak

    def get_frame_peak(self):
        """Get peak amplitude from only the most recent frame."""
        if self.last_frame is None:
            return 0
        audio_data = np.frombuffer(self.last_frame, dtype=np.int16)
        if len(audio_data) == 0:
            return 0
        peak = np.max(np.abs(audio_data))
        return int(peak)
        
"""
recorder = RECORDER()
start_time= time.time()
recorder.start_recording()
while time.time() - start_time<2.0:
    recorder.read_frames()
recorder.close()
sample = recorder.get_samples()
peak = recorder.get_peak()
print(peak)
"""
