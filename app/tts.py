import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

load_dotenv()  # Loads ELEVENLABS_API_KEY from .env

# Initialize client
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

def text_to_speech(text: str, output_path: str = "output/audio_response.mp3") -> str:
    audio_stream = client.text_to_speech.convert( # Changed variable name to reflect it's a stream
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # Default: Rachel. Replace with your preferred voice ID.
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    # Ensure output folder exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        for chunk in audio_stream: # Iterate over the generator
            f.write(chunk)

    return output_path