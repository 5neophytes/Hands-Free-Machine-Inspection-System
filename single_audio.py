import sounddevice as sd
from scipy.io.wavfile import write

# Parameters for the recording
sample_rate = 44100  # Sample rate in Hz
duration = int(input("Enter the duration of the recording in seconds: "))  # Duration of recording in seconds

print("Recording...")

# Record the audio
audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
sd.wait()  # Wait until the recording is finished

print("Recording finished!")

# Save the audio file
file_name = input("Enter the name of the output file (without extension): ") + ".wav"
write(file_name, sample_rate, audio_data)

print(f"Audio file saved as {file_name}")