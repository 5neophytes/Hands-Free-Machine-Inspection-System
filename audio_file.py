import sounddevice as sd
from scipy.io.wavfile import write
import os

# Define the details to be recorded
inspection_details = {
    "Tire Pressure for Left Front": 0, #pressure for left front is 34 psi
    "Tire Pressure for Right Front": 1, #the tire pressure for right front is 36 psi
    "Tire Condition for Left Front": 2, #good
    "Tire Condition for Right Front": 3, #needs replacement
    "Tire Pressure for Left Rear": 4, #the tire pressure for left rear is 35 psi
    "Tire Pressure for Right Rear": 5, #the tire pressure for right rear is 37 psi
    "Tire Condition for Left Rear": 6, #ok
    "Tire Condition for Right Rear": 7, #good
    "Overall Tire Summary": 8, #all the 4 tire pressures range from 33 to 37 psi which seems to be ok, but can be better
    "Battery Make": 9, #ABC
    "Battery replacement date": 10, #1st august 2024
    "Battery Voltage": 11, #the battery voltage is 5 volts
    "Battery Water level": 12, #low
    "Condition of Battery": 13, #no damage
    "Any Leak / Rust in battery": 14, #no leaks or rust
    "Battery overall Summary": 15, #overall the battery was in a good condition with no leaks no rust and the condition of the battery was good
    "Rust, Dent or Damage to Exterior": 16, #yes, some damage is found
    "Oil leak in Suspension": 17, #no oil leak in suspension
    "Overall Summary": 18, #there is some damage found in the exterior but there is no oil leak in suspension, overall summary is ok
    "Brake Fluid level": 19, #low
    "Brake Condition for Front": 20, #needs replacement
    "Brake Condition for Rear": 21, #good
    "Emergency Brake": 22, #good
    "Brake Overall Summary": 23, #overall brakes are good enough, thank you
    "Rust, Dents or Damage in Engine": 24, #no rust, dents or damage in the engine
    "Engine Oil Condition": 25, #bad
    "Engine Oil Color": 26, #brown
    "Brake Fluid Condition": 27, #good
    "Brake Fluid Color": 28, #black
    "Any oil leak in Engine": 29, #no leaks
    "Engine Overall Summary": 30, #overall engine is good enough with no leaks and brown and black colour
    "Any feedback from Customer": 31 #no feedbacks
}

# Parameters for recording
sample_rate = 44100  # Sample rate in Hz
audio_dir = "inspection_audio_files2"
os.makedirs(audio_dir, exist_ok=True)  # Create directory if it doesn't exist

def record_audio(detail_name, file_name):
    duration = int(input(f"Enter the duration for recording '{detail_name}' in seconds: "))
    print(f"Recording '{detail_name}'...")
    
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    
    file_path = os.path.join(audio_dir, str(file_name) + ".wav")
    write(file_path, sample_rate, audio_data)
    
    print(f"Audio for '{detail_name}' saved as {file_path}\n")

# Loop through the inspection details and record audio for each
for detail_name, file_name in inspection_details.items():
    record_audio(detail_name, file_name)

print("All audio recordings are completed and saved.")
