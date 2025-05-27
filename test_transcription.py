# from app.transcription import transcribe_audio

# def test_transcribe_audio():
#     audio_path = "sample_audio.wav"  # Replace with your actual test audio file
#     transcript = transcribe_audio(audio_path)
#     assert isinstance(transcript, str)
#     print("Transcript:", transcript)




from app.transcription import transcribe_audio

if __name__ == "__main__":
    transcription = transcribe_audio("sample_audio.wav")
    print("🎙 Transcribed Text:\n", transcription)

