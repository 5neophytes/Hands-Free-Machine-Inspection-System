from pathlib import Path
from openai import OpenAI

# Your API key
api_key = 'sk-proj-MugzvB91E6HoJee02kdwT3BlbkFJTQFtSA9C99xnXXVq5sXI'

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# List of questions
questions_extracted = [
    "What is the tire pressure for the left front tire? Please start speaking after 5 seconds",
    "What is the tire pressure for the right front tire? Please start speaking after 5 seconds",
    "What is the condition of the left front tire? (Good, Ok, Needs Replacement) Please hold up your fingers in 3 seconds",
    "What is the condition of the right front tire? (Good, Ok, Needs Replacement) Please hold up your fingers in 3 seconds",
    "What is the tire pressure for the left rear tire? Please start speaking after 5 seconds",
    "What is the tire pressure for the right rear tire? Please start speaking after 5 seconds",
    "What is the condition of the left rear tire? (Good, Ok, Needs Replacement) Please hold up your fingers in 3 seconds",
    "What is the condition of the right rear tire? (Good, Ok, Needs Replacement) Please hold up your fingers in 3 seconds",
    "Provide an overall summary of the tires (up to 1000 characters). Please start speaking after 5 seconds",
    "What is the make of the battery? (e.g., CAT, ABC, XYZ). Please start speaking after 5 seconds",
    "What is the battery replacement date? Please start speaking after 5 seconds",
    "What is the battery voltage? (e.g., 12V, 13V) Please start speaking after 5 seconds",
    "What is the battery water level? (Good, Ok, Low) Please hold up your fingers in 3 seconds",
    "Is there any damage to the battery? (Y/N). Please start speaking after 5 seconds",
    "Is there any leak or rust in the battery? (Y/N) Please start speaking after 5 seconds",
    "Provide an overall summary of the battery (up to 1000 characters). Please start speaking after 5 seconds",
    "Is there any rust, dent, or damage to the exterior? (Y/N). Please start speaking after 5 seconds",
    "Is there any oil leak in the suspension? (Y/N)",
    "Provide an overall summary of the exterior (up to 1000 characters). Please start speaking after 5 seconds",
    "What is the brake fluid level? (Good, Ok, Low) Please hold up your fingers in 3 seconds",
    "What is the condition of the front brakes? (Good, Ok, Needs Replacement) Please hold up your fingers in 3 seconds",
    "What is the condition of the rear brakes? (Good, Ok, Needs Replacement) Please hold up your fingers in 3 seconds",
    "What is the condition of the emergency brake? (Good, Ok, Low) Please hold up your fingers in 3 seconds",
    "Provide an overall summary of the brakes (up to 1000 characters). Please start speaking after 5 seconds",
    "Is there any rust, dent, or damage to the engine? (Y/N). Please start speaking after 5 seconds",
    "What is the condition of the engine oil? (Good, Bad) Please start speaking after 5 seconds",
    "What is the color of the engine oil? (Clean, Brown, Black, etc.) Please hold up your fingers in 3 seconds",
    "What is the condition of the brake fluid? (Good, Bad) Please start speaking after 5 seconds",
    "What is the color of the brake fluid? (Clean, Brown, Black, etc.) Please hold up your fingers in 3 seconds",
    "Is there any oil leak in the engine? Please start speaking after 5 seconds",
    "Provide an overall summary of the engine (up to 1000 characters). Please start speaking after 5 seconds",
    "Is there any feedback from the customer? Please start speaking after 5 seconds"
]

# Directory to save the audio files
output_dir = Path("C:/Users/nagpa/Desktop/inspectionApplication/inspectionApplication/audios_output")
output_dir.mkdir(parents=True, exist_ok=True)

def save_text_to_speech(question, index):
    print(f"Processing question {index + 1}/{len(questions_extracted)}: {question}")
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=question
    )
    audio_file_path = output_dir / f"question_{index + 1}.wav"
    response.stream_to_file(audio_file_path)
    response.ast
    print(f"Saved question {index + 1} as {audio_file_path}")

for index, question in enumerate(questions_extracted):
    save_text_to_speech(question, index)

print("All questions have been converted to speech and saved as audio files.")
