from app.tts import text_to_speech

if __name__ == "__main__":
    text = "Hello! I am your voice assistant. How can I help you today?"
    output_file = text_to_speech(text)
    print("✅ Voice output saved to:", output_file)
