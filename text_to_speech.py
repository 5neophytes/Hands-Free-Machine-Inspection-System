from pathlib import Path
from openai import OpenAI

api_key = 'sk-proj-MugzvB91E6HoJee02kdwT3BlbkFJTQFtSA9C99xnXXVq5sXI'
client = OpenAI(api_key=api_key)

speech_file_path = "C:/Users/nagpa/Desktop/cat_hackathon/audios_output/speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input="Please input the tire pressure"
)

response.stream_to_file(speech_file_path)