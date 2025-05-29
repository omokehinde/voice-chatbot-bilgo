# voice-chatbot-bilgo

# 🎙️ Voice Chatbot with RAG, Google Gemini & ElevenLabs TTS

This project is a voice-enabled AI chatbot built with Python (Flask backend) and React (frontend UI). It uses:

- **Google Gemini (via LangChain)** for generating answers.
- **FAISS** for Retrieval-Augmented Generation (RAG).
- **Google Speech-to-Text** for transcribing voice input.
- **ElevenLabs** (or fallback to `pyttsx3`) for voice responses.
- **React + Material UI** for the frontend.

---

## 🚀 Features

- 🎤 Speak to the chatbot via voice
- 🤖 Receives text + voice responses
- 🧠 RAG-enabled contextual answering
- 🌐 Supports Arabic and English
- ✅ Terminal-based CLI test available

---

## 🧩 Tech Stack

- **Backend:** Python, Flask, LangChain, FAISS, Google Generative AI, Google Speech-to-Text, ElevenLabs
- **Frontend:** React, Material UI, MediaRecorder API

---

## 📦 How to Clone and Run

### 1. Clone the Repository

```bash
git clone https://github.com/omokehinde/voice-chatbot-bilgo.git
cd voice-chatbot-bilgo
```

### 2. Set Up Python Virtual Environment

On Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```
On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```
Ensure you set up your .env file with GOOGLE_API_KEY, GOOGLE_APPLICATION_CREDENTIALS, and ELEVENLABS_API_KEY.

### 4. Start the Flask Backend

```bash
python main.py
```
This runs the Flask API server on `http://localhost:5000`

### 5. Start the React Frontend

```bash
cd ui
npm install
npm start
```
This opens the frontend in your browser at http://localhost:3000

## 🖥️ CLI Mode (Terminal Test)

You can also test the chatbot directly from the terminal using your microphone.
```bash
python cli_test_chatbot.py
```
This will:
Record your voice

Transcribe it using Google Speech-to-Text

Query the RAG chatbot

Display the chatbot’s response (text)

Speak the response aloud (using ElevenLabs or fallback TTS)

## 📁 Project Structure

```bash
voice-chatbot-bilgo/
├── app/                 # Core backend logic (chatbot, TTS, transcription, etc.)
├── ui/                  # React frontend app
├── audio/               # Temporary voice recordings
├── output/              # Audio responses from ElevenLabs
├── static/              # Public Flask audio files
├── main.py              # Flask server entry point
├── cli_test_chatbot.py  # CLI for testing bot interaction via voice
└── requirements.txt
```

## 📝 License
MIT License – feel free to use, fork, and build on this.

## 🙌 Acknowledgements

- LangChain

- Google Generative AI

- ElevenLabs

- [React, Material UI, FAISS]

- Many more I didn't mention. 

Made with ❤️ by @omokehinde

```yaml

---

Let me know if you want a shorter version, want to include a demo GIF or screenshots, or want to add deployment instructions!
```