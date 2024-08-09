import os
import csv
from openai import OpenAI

api_key = 'sk-proj-MugzvB91E6HoJee02kdwT3BlbkFJTQFtSA9C99xnXXVq5sXI'
client = OpenAI(api_key=api_key)

audio_directory = "C:/Users/nagpa/Desktop/cat_hackathon/audios_input"

results = []

def process_audio_file(file_path, extract_number):
    with open(file_path, "rb") as audio_file:
        translation = client.audio.translations.create(
            model="whisper-1", 
            file=audio_file
        )
        
        text = translation.text
        
        if extract_number:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": "You are a data extractor. Give me only the numerical psi value from the given text"},
                    {"role": "user", "content": text}
                ]
            )
            
            return completion.choices[0].message.content.strip()
        else:
            return text

# Iterate over each file in the directory
for filename in os.listdir(audio_directory):
    if filename.endswith(".m4a"):
        audio_file_path = os.path.join(audio_directory, filename)
        
        # Process the file three times
        psi_value_1 = process_audio_file(audio_file_path, extract_number=True)
        psi_value_2 = process_audio_file(audio_file_path, extract_number=True)
        summary = process_audio_file(audio_file_path, extract_number=False)
        
        # Append the result to the list
        results.append([filename, psi_value_1, psi_value_2, summary])

# Define the CSV file path
csv_file_path = "C:/Users/nagpa/Desktop/cat_hackathon/psi_values.csv"

# Write the results to a CSV file
with open(csv_file_path, mode="w", newline="") as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Filename", "PSI Value Left", "PSI Value Right", "Summary"])  # Write the header
    csv_writer.writerows(results)  # Write the data

print("PSI values and summaries have been extracted and saved to:", csv_file_path)
