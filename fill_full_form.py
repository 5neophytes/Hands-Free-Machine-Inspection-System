import os
import csv
from openai import OpenAI

api_key = 'sk-proj-MugzvB91E6HoJee02kdwT3BlbkFJTQFtSA9C99xnXXVq5sXI'

client = OpenAI(api_key=api_key)

audio_directory = "C:/Users/nagpa/Desktop/cat_hackathon/audios_input"

results = []

audio_files = sorted([f for f in os.listdir(audio_directory) if f.endswith(".m4a")])

def process_audio_file(file_path, extract_number):
    with open(file_path, "rb") as audio_file:
        
        translation = client.audio.translations.create(
            model = "whisper-1",
            file=audio_file
        )
        
        text = translation.text
        
        if extract_number:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": "You are a data extractor. Give me only the numerical value from the given text"},
                    {"role": "user", "content": text}
                ]
            )
            
            return completion.choices[0].message.content.strip()
        else:
            return text

category_indices = {
    "Truck Serial Number": 0,
    "Truck Model": 1,
    "Inspection ID": 2,
    "Inspector Name": 3,
    "Inspection Employee ID": 4,
    "Date & Time of Inspection": 5,
    "Location of Inspection": 6,
    "Geo Coordinates of Inspection": 7,
    "Service Meter Hours": 8,
    "Inspector Signature": 9,
    "Customer Name / Company name": 10,
    "CAT Customer ID": 11,
    "Tire Pressure for Left Front": 12,
    "Tire Pressure for Right Front": 13,
    "Tire Condition for Left Front": 14,
    "Tire Condition for Right Front": 15,
    "Tire Pressure for Left Rear": 16,
    "Tire Pressure for Right Rear": 17,
    "Tire Condition for Left Rear": 18,
    "Tire Condition for Right Rear": 19,
    "Overall Tire Summary": 20,
    "Battery Make": 21,
    "Battery replacement date": 22,
    "Battery Voltage": 23,
    "Battery Water level": 24,
    "Condition of Battery": 25,
    "Any Leak / Rust in battery": 26,
    "Battery overall Summary": 27,
    "Rust, Dent or Damage to Exterior": 28,
    "Oil leak in Suspension": 29,
    "Overall Summary": 30,
    "Brake Fluid level": 31,
    "Brake Condition for Front": 32,
    "Brake Condition for Rear": 33,
    "Emergency Brake": 34,
    "Brake Overall Summary": 35,
    "Rust, Dents or Damage in Engine": 36,
    "Engine Oil Condition": 37,
    "Engine Oil Color": 38,
    "Brake Fluid Condition": 39,
    "Brake Fluid Color": 40,
    "Any oil leak in Engine": 41,
    "Engine Overall Summary": 42,
    "Any feedback from Customer": 43
}

for i in range(0, len(audio_files), len(category_indices)):
    row = [None] * len(category_indices)

    for idx, (category, category_idx) in enumerate(category_indices.items()):
        if i + idx < len(audio_files):
            file_path = os.path.join(audio_directory, audio_files[i + idx])
            if category in ["Inspection ID","Overall Tire Summary", "Battery overall Summary", "Overall Summary", "Engine Overall Summary", "Any feedback from Customer"]:
                row[category_idx] = process_audio_file(file_path, extract_number=False)
            else:
                row[category_idx] = process_audio_file(file_path, extract_number=True)
    
    results.append(row)

csv_file_path = "C:/Users/nagpa/Desktop/cat_hackathon/inspection_report.csv"

with open(csv_file_path, mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(list(category_indices.keys()))
    csv_writer.writerows(results)

print("Inspection data has been extracted and saved to:", csv_file_path)
