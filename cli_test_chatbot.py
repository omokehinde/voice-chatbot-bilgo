import os
import sounddevice as sd
import wavio
from pydub import AudioSegment
from pydub.playback import play

from app.transcription import transcribe_audio
from app.tts import text_to_speech
from app.chatbot import get_chatbot
from app.arabic_support import is_arabic

# Constants
AUDIO_FOLDER = "audio"
AUDIO_FILENAME = "input.wav"
AUDIO_PATH = os.path.join(AUDIO_FOLDER, AUDIO_FILENAME)
DURATION = 10  # seconds
SAMPLE_RATE = 44100

def record_audio(filepath=AUDIO_PATH, duration=DURATION, fs=SAMPLE_RATE):
    print("🎙️ Recording...")
    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    recording = recording / max(abs(recording))  # Normalize audio
    wavio.write(filepath, recording, fs, sampwidth=2)
    print("✅ Recording saved")

def apply_language_prompt(query: str) -> str:
    if is_arabic(query):
        arabic_prompt = "أنت مساعد ذكي ترد دائمًا باللغة العربية وبوضوح."
        return f"{arabic_prompt}\n\n{query}"
    return query

def main_chat_loop():
    chatbot = get_chatbot()
    print("🤖 Voice chatbot started. Speak into the mic. Press Ctrl+C to exit.")

    while True:
        try:
            record_audio()
            query = transcribe_audio(file_name=AUDIO_FILENAME)

            if not query.strip():
                print("🤔 Couldn’t hear anything. Try again.")
                continue

            print(f"🗣️ You said: {query}")
            query = apply_language_prompt(query)

            response = chatbot.invoke({"query": query})
            answer = response["result"]
            print(f"🤖 {answer}")

            # Use TTS and try to play audio if ElevenLabs succeeded
            audio_path = text_to_speech(answer)
            if audio_path and os.path.exists(audio_path):
                audio = AudioSegment.from_file(audio_path)
                play(audio)

        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break

if __name__ == "__main__":
    main_chat_loop()
