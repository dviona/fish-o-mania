import pyaudio
import wave
import numpy as np

def detect():
    
    FRAMES_PER_BUFFER = 3200
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()
    stream = p.open(
                    format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = FRAMES_PER_BUFFER
                    )
    print("the sea waits for your rage")
    seconds = 5
    frames = []
    for i in range(0, int(RATE / FRAMES_PER_BUFFER * seconds)):
        data = stream.read(FRAMES_PER_BUFFER, exception_on_overflow = False)
        frames.append(data)


    stream.stop_stream()
    stream.close()
    p.terminate()
    # save the documents in a file
    obj = wave.open("test.wav", "wb")
    obj.setnchannels(CHANNELS)
    obj.setsampwidth(p.get_sample_size(FORMAT))
    obj.setframerate(RATE)
    obj.writeframes(b"".join(frames))
    obj.close()

    obj = wave.open("test.wav", "rb")
    signal_wave = obj.readframes(-1)
    signal_array = np.frombuffer(signal_wave, dtype=np.int16)
    peak = np.max(np.abs(signal_array))
    obj.close()
    print(peak)
    if peak > 10000:
        return True

print(detect())

    
