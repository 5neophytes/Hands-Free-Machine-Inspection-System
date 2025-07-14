import openai


api_key = 'sk-proj-MugzvB91E6HoJee02kdwT3BlbkFJTQFtSA9C99xnXXVq5sXI'
def transcribe_audio(file_path):
    
    client = openai.OpenAI(api_key=api_key)
    audio_file = open(file_path, "rb")

    translation = client.audio.translations.create(
        model="whisper-1",
        file=audio_file
    )
    text = translation.text
    return text

