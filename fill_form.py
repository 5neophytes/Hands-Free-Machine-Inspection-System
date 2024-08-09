import os
import csv
from openai import OpenAI

api_key =   'sk-proj-MugzvB91E6HoJee02kdwT3BlbkFJTQFtSA9C99xnXXVq5sXI'

client = OpenAI(api_key=api_key)

audio_directory = "C:/Users/satvi/OneDrive/Desktop/code-a-thon/inspection_audio_files2"

results = []

audio_files = sorted([f for f in os.listdir(audio_directory) if f.endswith(".wav")])

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
    "Tire Pressure for Left Front": 0, 
    "Tire Pressure for Right Front": 1, 
    "Tire Condition for Left Front": 2, 
    "Tire Condition for Right Front": 3, 
    "Tire Pressure for Left Rear": 4, 
    "Tire Pressure for Right Rear": 5, 
    "Tire Condition for Left Rear": 6, 
    "Tire Condition for Right Rear": 7, 
    "Overall Tire Summary": 8, 
    "Battery Make": 9, 
    "Battery replacement date": 10, 
    "Battery Voltage": 11, 
    "Battery Water level": 12, 
    "Condition of Battery": 13, 
    "Any Leak / Rust in battery": 14, 
    "Battery overall Summary": 15, 
    "Rust, Dent or Damage to Exterior": 16, 
    "Oil leak in Suspension": 17, 
    "Overall Summary": 18, 
    "Brake Fluid level": 19, 
    "Brake Condition for Front": 20, 
    "Brake Condition for Rear": 21, 
    "Emergency Brake": 22, 
    "Brake Overall Summary": 23, 
    "Rust, Dents or Damage in Engine": 24, 
    "Engine Oil Condition": 25, 
    "Engine Oil Color": 26, 
    "Brake Fluid Condition": 27, 
    "Brake Fluid Color": 28, 
    "Any oil leak in Engine": 29, 
    "Engine Overall Summary": 30, 
    "Any feedback from Customer": 31 
}
count = 0
for i in range(0, len(audio_files), len(category_indices)):
    row = [None] * len(category_indices)

    for idx, (category, category_idx) in enumerate(category_indices.items()):
        if i + idx < len(audio_files):
            file_path = os.path.join(audio_directory, audio_files[i + idx])
            if category in ["Tire Pressure for Left Front","Tire Pressure for Right Front","Tire Pressure for Left Rear","Tire Pressure for Right Rear","Battery Voltage"]:
                row[category_idx] = process_audio_file(file_path, extract_number=True)
                count=count+1
                print(f"Features Completed : ",{count})
            else:
                row[category_idx] = process_audio_file(file_path, extract_number=False)
                count =count+ 1
                print(f"Features Completed : ",{count})
    
    results.append(row)

csv_file_path = "C:/Users/satvi/OneDrive/Desktop/code-a-thon/inspection_report.csv"

with open(csv_file_path, mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(list(category_indices.keys()))
    csv_writer.writerows(results)

print("Inspection data has been extracted and saved to:", csv_file_path)