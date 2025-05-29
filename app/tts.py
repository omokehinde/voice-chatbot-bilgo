import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.core.api_error import ApiError
import pyttsx3

# Load environment variables
load_dotenv()

# Initialize ElevenLabs client and pyttsx3 engine
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
engine = pyttsx3.init()

def text_to_speech(text: str, output_path: str = "static/audio_response.mp3") -> str:
    """
    Converts text to speech using ElevenLabs. Falls back to pyttsx3 if ElevenLabs fails.

    Args:
        text (str): Text to convert to speech.
        output_path (str): File path to save ElevenLabs audio output.

    Returns:
        str: Path to saved audio file if ElevenLabs is used, or None if fallback is used.
    """
    try:
        print("🎧 Using ElevenLabs for text-to-speech...")
        audio_stream = client.text_to_speech.convert(
            text=text,
            voice_id="JBFqnCBsd6RMkjVDRZzb",  # Rachel (replace if needed)
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)

        return output_path

    except ApiError as e:
        print("⚠️ ElevenLabs API error:", e)
        print("🔊 Falling back to pyttsx3...")
        print(f"🗣️ Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
        return None

    except Exception as e:
        print("❌ Unexpected error with ElevenLabs:", e)
        print("🔊 Falling back to pyttsx3...")
        print(f"🗣️ Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
        return None
