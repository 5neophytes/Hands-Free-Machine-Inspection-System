import sounddevice as sd
from scipy.io.wavfile import write
import os

def capture_audio(filename):
    sample_rate = 44100
    duration = 5
    
    print(f"Recording...You have two seconds to speak...")

    # Record the audio
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()

    print("Recording finished!")

    write(filename, sample_rate, audio_data)

    print(f"Audio file saved as {filename}")

    return filename
