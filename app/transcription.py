import os
import pathlib
from google.cloud import speech
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio(file_name="sample_audio.aac"):

    audio_path = file_name # Directly use file_name as the path

    # Ensure the audio file exists
    if not pathlib.Path(audio_path).exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    client = speech.SpeechClient()

    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)

    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript + " "

    return transcription.strip()