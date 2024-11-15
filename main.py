import pyaudio
import wave

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
for i in range(int(RATE / CHUNK * 4)):
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


import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Load the audio file
audio_file = "output.wav"

# Open the audio file and use the recognizer to recognize speech
with sr.AudioFile(audio_file) as source:
    print("Listening...")
    audio_data = recognizer.record(source)  # Record the audio data

    # Convert the audio to text using Google's web-based STT engine
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio_data)  # Google Web Speech API
        print(f"Transcription: {text}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")


from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load GPT-2 model
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Set pad_token_id to eos_token_id to avoid warnings
model.config.pad_token_id = model.config.eos_token_id

# Generate response
def generate_response(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    # Use the attention_mask to handle padding properly
    outputs = model.generate(inputs, max_length=50, num_return_sequences=1)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

response = generate_response("User said: " + text)
print("AI Response:", response)
