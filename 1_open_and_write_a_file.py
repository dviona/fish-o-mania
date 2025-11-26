import wave

# rb for read in binary
obj = wave.open("assets/music_collection/first_lyrics.WAV","rb")
print("number of chnnels", obj.getnchannels())
# sample width means how many bytes are there in a frame
print("sample width", obj.getsampwidth())
print("frame rate", obj.getframerate())
print("number of frames", obj.getnframes())
print("para", obj.getparams())

t_audio = obj.getnframes()/obj.getframerate()
# -1 will read all the frames
frames = obj.readframes(-1)
print(type(frames), type(frames[0]))

#length of frames equals number of channels * sample width * readframes
print(len(frames)/4)

# write in a new file
obj_new = wave.open("patricl_new.wav", "wb")
obj_new.setnchannels(2)
obj_new.setsampwidth(2)
obj_new.setframerate(44100)
obj_new.writeframes(frames)
obj_new.close()
