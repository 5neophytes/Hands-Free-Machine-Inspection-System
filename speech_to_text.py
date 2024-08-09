from openai import OpenAI

api_key = 'sk-proj-MugzvB91E6HoJee02kdwT3BlbkFJTQFtSA9C99xnXXVq5sXI'
client = OpenAI(api_key=api_key)

# audio_file= open("C:/Users/nagpa/Desktop/cat_hackathon/english_example.m4a", "rb")
# transcription = client.audio.transcriptions.create(
#   model="whisper-1", 
#   file=audio_file,
# #   response_format="text"
# )
# print(transcription.text)

audio_file = open("C:/Users/nagpa/Desktop/cat_hackathon/audios_input/english_example.m4a","rb")
# C:\Users\nagpa\Desktop\cat_hackathon\audios_input\english_example.m4a
translation = client.audio.translations.create(
  model="whisper-1", 
  file=audio_file
)
print(translation.text)

