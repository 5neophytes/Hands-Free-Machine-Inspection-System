from flask import Flask, jsonify, request
from capture_audio import capture_audio
from transcribe import transcribe_audio
import os
from collections import OrderedDict
import image_mapping
import time
from playsound import playsound
import json
import pygame
from openai import OpenAI

api_key = 'sk-proj-MugzvB91E6HoJee02kdwT3BlbkFJTQFtSA9C99xnXXVq5sXI'
client = OpenAI(api_key=api_key)

pygame.mixer.init()

json_file_path = 'C:/Users/nagpa/Desktop/HACKATHON/catathon/src/assets/output.json'

app = Flask(__name__)

# Define the questions
questions = [
    # #"1. What is the tire pressure for the left front tire?", 
    {"question":"Tire Pressure for Left Front", "flag": True},
    # "2. What is the tire pressure for the right front tire?",
    {"question":"Tire Pressure for Right Front", "flag": True},
    # # # "3. What is the condition of the left front tire? (Good, Ok, Needs Replacement)",
    {"question":"Tire Condition for Left Front", "flag": False},
    # "4. What is the condition of the right front tire? (Good, Ok, Needs Replacement)",
    {"question":"Tire Condition for Right Front", "flag": False},
    #"5. What is the tire pressure for the left rear tire?",
    {"question":"▪ Tire Pressure for Left Rear", "flag": True},
    # "6. What is the tire pressure for the right rear tire?",
    # {"question":"Tire Pressure for Right Rear", "flag": True},
    # # # "7. What is the condition of the left rear tire? (Good, Ok, Needs Replacement)",
    # {"question":"Tire Condition for Left Rear –", "flag": False},
    # # # "8. What is the condition of the right rear tire? (Good, Ok, Needs Replacement)",
    # {"question":"Tire Condition for Right Rear", "flag": False},
    # # "9. Provide an overall summary of the tires (up to 1000 characters).",
    # {"question":"Overall Tire Summary", "flag": True},
    # # "10. What is the make of the battery? (e.g., CAT, ABC, XYZ)",
    # {"question":"Battery Make", "flag": True},
    # # "11. What is the battery replacement date?",
    # {"question":"Battery replacement date", "flag": True},
    # # "12. What is the battery voltage? (e.g., 12V, 13V)",
    # {"question":"Battery Voltage", "flag": True},
    # # # "13. What is the battery water level? (Good, Ok, Low)",
    # {"question":"Battery Water level", "flag": False},
    # # "14. Is there any damage to the battery? (Y/N). If yes, please attach an image.",
    # {"question":"Condition of Battery", "flag": True},
    # # # "15. Is there any leak or rust in the battery? (Y/N)",
    # {"question":"Any Leak / Rust in battery", "flag": False},
    # # "16. Provide an overall summary of the battery (up to 1000 characters).",
    # {"question":"Battery overall Summary", "flag": True},
    # # # "17. Is there any rust, dent, or damage to the exterior? (Y/N). If yes, please explain in the notes and attach images.",
    # {"question":"Rust, Dent or Damage to Exterior", "flag": True},
    # # # "18. Is there any oil leak in the suspension? (Y/N)",
    # {"question":"Oil leak in Suspension", "flag": False},
    # # "19. Provide an overall summary of the exterior (up to 1000 characters).",
    # {"question":"Exterior Overall Summary", "flag": True},
    # # # "20. What is the brake fluid level? (Good, Ok, Low)",
    # {"question":"Brake Fluid leve", "flag": False},
    # # # "21. What is the condition of the front brakes? (Good, Ok, Needs Replacement)",
    # {"question":"Brake Condition for Front", "flag": False},
    # # # "22. What is the condition of the rear brakes? (Good, Ok, Needs Replacement)",
    # {"question":"Brake Condition for Rear", "flag": False},
    # # # "23. What is the condition of the emergency brake? (Good, Ok, Low)",
    # {"question":"Emergency Brake", "flag": False},
    # # # "24. Provide an overall summary of the brakes (up to 1000 characters).",
    # {"question":"Brake Overall Summary", "flag": True},
    # # "25. Is there any rust, dent, or damage to the engine? (Y/N). If yes, please explain in the notes and attach images.",
    # {"question":"Rust, Dents or Damage in Engine", "flag": True},
    # # # "26. What is the condition of the engine oil? (Good, Bad)",
    # {"question":"Engine Oil Condition", "flag": False},
    # # # "27. What is the color of the engine oil? (Clean, Brown, Black, etc.)",
    # {"question":"Engine Oil Color", "flag": False},
    # # # "28. What is the condition of the brake fluid? (Good, Bad)",
    # {"question":"Brake Fluid Condition", "flag": False},
    # # # "29. What is the color of the brake fluid? (Clean, Brown, Black, etc.)",
    # {"question":"Brake Fluid Color", "flag": False},
    # # # "30. Is there any oil leak in the engine? (Y/N)",
    # {"question":"Any oil leak in Engine", "flag": False},
    # # "31. Provide an overall summary of the engine (up to 1000 characters).",
    # {"question":"Engine Overall Summary", "flag": True},
    # # "32. Is there any feedback from the customer?"
    # {"question":"Any feedback from Customer", "flag": True}
]

# Store the answers and current state
answers = OrderedDict()
current_question_index = -1


# Mapping dictionaries
condition_mapping = {
    1: "good",
    2: "ok",
    3: "needs replacement"
}

fluid_level_mapping = {
    1: "good",
    2: "ok",
    3: "low"
}

yes_no_mapping = {
    1: "yes",
    2: "no"
}

quality_mapping = {
    1: "good",
    2: "bad"
}

color_mapping = {
    1: "clean",
    2: "brown",
    3: "black"
}

@app.route('/')
def index():
    return "Welcome to the Audio Processing API"

@app.route('/start-form', methods=['POST'])
def start_form():
    global answers, current_question_index
    answers = OrderedDict()
    current_question_index = 0
    # playsound('C:/Users/nagpa/Desktop/inspectionApplication/audios-main/introduction.wav')
    return jsonify({'message': 'Form started. Please proceed with answering the questions.'})

@app.route('/next-question', methods=['POST'])
def next_question():
    global current_question_index, answers

    if current_question_index <0:
        pygame.mixer.music.load(f"C:/Users/nagpa/Desktop/inspectionApplication/audios-main/introduction.wav")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():  # wait for music to finish playing
            continue
        current_question_index+=1
        return jsonify({'Output': 'Introduction Played'})

    if current_question_index >= len(questions):
        with open(json_file_path, 'w') as json_file:
            json.dump(answers, json_file, indent=4)
        print(answers)
        return jsonify({'Output': 'All questions have been answered.'})

    question_dict = questions[current_question_index]
    question_text = question_dict["question"]
    flag = question_dict["flag"]
    print(question_text)

    pygame.mixer.music.load(f"C:/Users/nagpa/Desktop/inspectionApplication/audios-main/question_{current_question_index+1}.wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():  # wait for music to finish playing
        continue

    if flag:
        # Capture the audio for the current question
        audio_filename = f"audio_{current_question_index + 1}.wav" 
        capture_audio(audio_filename)
        
        transcription = transcribe_audio(audio_filename)

        if current_question_index in[0,1,4,5,11]:
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "You are a data extractor. Give me only the numerical psi value from the given text"},
                {"role": "user", "content": transcription}
            ]
            )
            output = completion.choices[0].message.content

            answers[question_text] = output
        else :
            answers[question_text] = transcription

        
    else:
        # Capture the image for the current question
        photo = image_mapping.capture_photo()

        # Detect the number for the current question
        try:
            which_number = int(image_mapping.detect_number(photo))
            if current_question_index in [2, 3, 6, 7, 20, 21]:
                mapped_answer = condition_mapping.get(which_number, "Unknown value")
            elif current_question_index in [12, 19, 22]:
                mapped_answer = fluid_level_mapping.get(which_number, "Unknown value")
            elif current_question_index in [14, 17, 29]:
                mapped_answer = yes_no_mapping.get(which_number, "Unknown value")
            elif current_question_index in [25, 27]:
                mapped_answer = quality_mapping.get(which_number, "Unknown value")
            else:
                mapped_answer = color_mapping.get(which_number, "Unknown value")

            answers[question_text] = mapped_answer
        except:
            print("There was no number held up in the image")

    current_question_index +=1
    
    if current_question_index < len(questions):
        next_question = questions[current_question_index]
        return jsonify({'question': next_question, 'current_index': current_question_index})
    else:
        return jsonify({'message': 'All questions have been answered.', 'answers': answers})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
