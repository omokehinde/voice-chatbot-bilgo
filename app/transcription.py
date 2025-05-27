# import os
# from google.cloud import speech
# import io

# def transcribe_audio(audio_file_path):
#     """Transcribes speech from an audio file using Google Cloud Speech-to-Text."""
#     client = speech.SpeechClient()

#     with io.open(audio_file_path, "rb") as audio_file:
#         content = audio_file.read()

#     audio = speech.RecognitionAudio(content=content)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#         sample_rate_hertz=16000,
#         language_code="en-US",
#     )

#     response = client.recognize(config=config, audio=audio)

#     # Get the first transcript (most likely)
#     transcript = " ".join(result.alternatives[0].transcript for result in response.results)
#     return transcript



# app/transcription.py

import os
import pathlib
from google.cloud import speech
from dotenv import load_dotenv

load_dotenv()

def transcribe_audio(file_name="sample_audio.aac"):
    audio_path = os.path.join("audio", file_name)
    if not pathlib.Path(audio_path).exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    client = speech.SpeechClient()

    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,  # Use this if unsure
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)

    transcription = ""
    for result in response.results:
        transcription += result.alternatives[0].transcript + " "

    return transcription.strip()
