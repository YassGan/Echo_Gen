import pyaudio
import wave

# Parameters for recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit)
CHANNELS = 1              # Number of audio channels
RATE = 44100              # Sample rate
CHUNK = 1024              # Number of frames per buffer
OUTPUT_FILENAME = "output.wav"  # Output file name

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream to record audio
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

frames = []

# Record for 5 seconds
for i in range(int(RATE / CHUNK * 8)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording finished.")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded audio as a .wav file
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio file saved as {OUTPUT_FILENAME}")
