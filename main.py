from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid
import soundfile as sf
import numpy as np

from app.transcription import transcribe_audio
from app.tts import text_to_speech
from app.chatbot import get_chatbot
from app.arabic_support import is_arabic

app = Flask(__name__)
CORS(app)

AUDIO_FOLDER = "static"
os.makedirs(AUDIO_FOLDER, exist_ok=True)

chatbot = get_chatbot()

def apply_language_prompt(query: str) -> str:
    if is_arabic(query):
        return "أنت مساعد ذكي ترد دائمًا باللغة العربية وبوضوح.\n\n" + query
    return query

@app.route("/api/voice-chat", methods=["POST"])
def voice_chat():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    audio_path = os.path.join(AUDIO_FOLDER, "input.wav")
    audio_file.save(audio_path)

    query = transcribe_audio(file_name=audio_path) # Get the user's transcribed query

    if not query.strip():
        return jsonify({"error": "No speech detected"}), 400

    applied_query = apply_language_prompt(query)
    result = chatbot.invoke({"query": applied_query})["result"]

    output_audio_path = text_to_speech(result)

    # Ensure unique file name for concurrent sessions
    response_id = str(uuid.uuid4())
    final_audio_path = os.path.join(AUDIO_FOLDER, f"response_{response_id}.mp3")
    # It's better to move the file after it's fully written by text_to_speech
    # For now, let's assume text_to_speech directly saves to output_audio_path
    # and then we rename it. If text_to_speech returns the path, os.rename is fine.
    # If text_to_speech already names it uniquely, you might not need os.rename here.
    # Based on tts.py, it saves to output_path and returns it, so os.rename is needed if output_path isn't the final one.
    os.rename(output_audio_path, final_audio_path)


    return jsonify({
        "query": query,  # Include the user's transcribed query
        "text": result,
        "audio_url": f"/api/audio/{response_id}"
    })

@app.route("/api/audio/<response_id>")
def get_audio(response_id):
    filename = f"response_{response_id}.mp3"
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)