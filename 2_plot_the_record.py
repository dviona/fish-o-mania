import wave
import matplotlib.pyplot as plt
import numpy as np

obj = wave.open("assets/music_collection/test.wav","rb")
channels = obj.getnchannels()
sample_freq = obj.getframerate()
n_samples = obj.getnframes()
signal_wave = obj.readframes(-1)
obj.close()

t_audio = n_samples / sample_freq

print(t_audio)

# plot the the frames we just get, datatype is 16 int
signal_array = np.frombuffer(signal_wave, dtype = np.int16)

# make the code defensive for stereo
if channels == 2:
    signal_array = signal_array.reshape(-1,2) # reshape the two channels
    signal_array = signal_array[:, 0] # select only the left channel, select [:, 1] for right channel

peak = np.max(np.abs(signal_array))
print("Peak value:", peak)
# linspace creates arrays with interval num times, time as the x axis, 0 as the start, t_audio as the end, num as how many samples
times = np.linspace(0, t_audio, num = n_samples)



plt.figure(figsize=(15,5))
plt.plot(times, signal_array)
plt.title("Audio Signal")
plt.ylabel("signal wave")
plt.xlabel("Time(s)")
# limit x between 0 and t_audio
plt.xlim(0,t_audio)
plt.show()
