import pyaudio
import wave
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torchaudio.transforms as T

# Parameters for audio recording
FORMAT = pyaudio.paInt16  # Audio format (16-bit)
CHANNELS = 1              # Number of audio channels
RATE = 44100              # Sample rate
CHUNK = 1024              # Number of frames per buffer
OUTPUT_FILENAME = "output.wav"  # Output file name

# Initialize PyAudio for audio recording
audio = pyaudio.PyAudio()

# Open stream to record audio
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

frames = []

# Record for 5 seconds
for i in range(int(RATE / CHUNK * 4)):  # Record 4 chunks (4 seconds)
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

# --- Begin Transcription --- #

# Load Wav2Vec2 model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

# Load the audio file using torchaudio
waveform, sample_rate = torchaudio.load(OUTPUT_FILENAME)

# Resample to 16kHz if the sample rate is not 16kHz
if sample_rate != 16000:
    resampler = T.Resample(orig_freq=sample_rate, new_freq=16000)
    waveform = resampler(waveform)
    sample_rate = 16000

# Ensure the waveform is 2D (batch_size, num_samples)
waveform = waveform.squeeze()  # Remove extra dimensions if necessary
input_values = processor(waveform, return_tensors="pt", sampling_rate=sample_rate).input_values

# Transcription
logits = model(input_values).logits
predicted_ids = torch.argmax(logits, dim=-1)
transcription = processor.decode(predicted_ids[0])

print("Transcription:", transcription)
