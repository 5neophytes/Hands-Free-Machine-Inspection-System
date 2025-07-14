import sounddevice as sd
from scipy.io.wavfile import write
import os
import time

def capture_audio(filename, sample_rate=44100, duration=10):
    print(f"Recording...You have {duration} seconds to speak...")

    # Record the audio
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()

    print("Recording finished!")

    write(filename, sample_rate, audio_data)

    print(f"Audio file saved as {filename}")

for index in range(1, 33):
    filename = f"question_{index}.wav"
    print(f'Please say the question number {index}')
    capture_audio(filename)
    print('you have a break of 5 seconds')
    time.sleep(5)

