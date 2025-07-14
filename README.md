# Hands-Free Machine Inspection System

A fully voice- and gesture-controlled machine inspection system designed for mechanics to perform inspections **without touching the laptop**. This system supports **speech input**, **gesture-based multiple-choice input**, and **wireless navigation**, allowing seamless interaction even in tight or dirty inspection environments.

---

## Hackathon Achievement

This project was developed during a **2-day hackathon** hosted by **Caterpillar Digital Inc.**, where our team **5 Neophytes** advanced to the **final round** of the competition. The challenge demanded a solution that could address real-world industrial inspection needs within an extremely tight timeframe. We strategically leveraged **OpenAI APIs** to enable rapid development while maintaining high functionality, allowing us to focus on creating a practical system optimized for harsh worksite conditions.

---

## Project Overview

This application runs through a form of **32 questions** to evaluate the condition of a machine and decide if servicing is required. It is designed to be efficient, mobile, and completely hands-free.

---

## Key Features

- No typing or laptop interaction required
- Speech input for descriptive/feedback answers
- Gesture input using hand signs for multiple-choice questions
- Glove-based navigation through questions using ESP32 microcontroller
- Cap-mounted camera and headphones for mobility
- Fully automated, question-by-question iteration
- Structured output saved in `output.json`

---

## Flow

1. Mechanic initiates the form with a glove button press
2. Each question is played aloud using TTS
3. Based on the question type:
   - **Multiple-choice**: Mechanic shows fingers (1/2/3) to the camera
   - **Descriptive answer**: Mechanic speaks response
4. Image or audio is captured and processed accordingly
5. Response is saved
6. Mechanic presses the glove button to move to the next question
7. After all 32 questions, results are stored in a JSON file

---

## Models Used

| Task                  | Model Used            |
|-----------------------|------------------------|
| Speech-to-Text (ASR)  | OpenAI Whisper         |
| Text-to-Speech (TTS)  | OpenAI TTS-1           |
| Image Classification  | OpenAI GPT-4o-mini     |
| Value Extraction      | OpenAI GPT-3.5-Turbo   |

---

## Input Modalities

### 1. Voice Input
- For feedback or informative questions
- Recorded via mic, transcribed using Whisper

### 2. Gesture Input
- For multiple-choice questions
- Camera captures hand sign (number of fingers)
- Interpreted using GPT-4o-mini

---

## Hardware Integration

### ESP32 Microcontroller
- Used to navigate through questions
- Worn in a glove with a button
- Sends signal via **Bluetooth**
- Coded using **Arduino IDE (Embedded C)**

### Cap Setup
- Mounted camera (for gesture recognition)
- Headphones (for audio prompts)

---

## Libraries & Tools Used

| Purpose                 | Library/Tool              |
|--------------------------|----------------------------|
| Backend API              | Flask                      |
| Audio Playback           | `pygame.mixer`, OpenAI TTS |
| Audio Recording          | Custom mic interface       |
| Speech-to-Text           | OpenAI Whisper API         |
| Text-to-Speech           | OpenAI TTS-1 API           |
| Image Capture            | `cv2`, webcam module       |
| Image Classification     | OpenAI GPT-4o-mini         |
| Glove Control            | ESP32 (Arduino Bluetooth)  |
| Output Storage           | `json`, `OrderedDict`      |

---

## Output

All responses from the mechanic are stored in a structured JSON file called `output.json`.

### Example Output

```json
{
  "What is the tire pressure for the left front tire?": "Hi, this is Ajay, the pressure is 35 PSI.",
  "What is the tire pressure for the right front tire?": "the pressure is 32 psi",
  "What is the condition of the left front tire? (Good, Ok, Needs Replacement)": "good",
  "What is the condition of the right front tire? (Good, Ok, Needs Replacement)": "good",
  "What is the tire pressure for the left rear tire?": "uh... thirty-five psi",
  "What is the tire pressure for the right rear tire?": "39 PSI",
  "What is the condition of the left rear tire? (Good, Ok, Needs Replacement)": "ok",
  "What is the condition of the right rear tire? (Good, Ok, Needs Replacement)": "needs replacement",
  "Provide an overall summary of the tires (up to 1000 characters).": "Overall, the tyres are very good.",
  "What is the make of the battery? (e.g., CAT, ABC, XYZ)": "Oh, God.",
  "What is the battery replacement date?": "27th January 2024",
  "What is the battery voltage? (e.g., 12V, 13V)": "44 Volts",
  "What is the battery water level? (Good, Ok, Low)": "good",
  "Is there any damage to the battery? (Y/N). If yes, please attach an image.": "Yes, there is damage to the battery.",
  "Provide an overall summary of the battery (up to 1000 characters).": "Overall the battery is working fine.",
  "Is there any rust, dent, or damage to the exterior? (Y/N). If yes, please explain in the notes and attach images.": "Thanks for watching!",
  "Is there any oil leak in the suspension? (Y/N)": "yes",
  "Provide an overall summary of the exterior (up to 1000 characters).": "Overall exterior is very beautiful.",
  "What is the brake fluid level? (Good, Ok, Low)": "Unknown value",
  "What is the condition of the front brakes? (Good, Ok, Needs Replacement)": "Unknown value",
  "What is the condition of the rear brakes? (Good, Ok, Needs Replacement)": "ok",
  "What is the condition of the emergency brake? (Good, Ok, Low)": "good",
  "Provide an overall summary of the brakes (up to 1000 characters).": "Oh, brakes are good.",
  "Is there any rust, dent, or damage to the engine? (Y/N). If yes, please explain in the notes and attach images.": "There is no rust dent or damage.",
  "What is the condition of the engine oil? (Good, Bad)": "good",
  "What is the color of the engine oil? (Clean, Brown, Black, etc.)": "clean",
  "What is the condition of the brake fluid? (Good, Bad)": "bad",
  "What is the color of the brake fluid? (Clean, Brown, Black, etc.)": "black",
  "Is there any oil leak in the engine? (Y/N)": "yes",
  "Provide an overall summary of the engine (up to 1000 characters).": "Engine is good",
  "Is there any feedback from the customer?": "Overdramatic the way The application is insane very good job"
}
```
