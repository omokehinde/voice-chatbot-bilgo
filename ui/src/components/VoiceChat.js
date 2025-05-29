import React, { useState, useRef } from 'react';
import {
  Button,
  Typography,
  Box,
  CircularProgress,
  Paper
} from '@mui/material';

export default function VoiceChat() {
  const [recording, setRecording] = useState(false);
  const [transcription, setTranscription] = useState(''); // This will store the transcribed user query
  const [textResponse, setTextResponse] = useState(''); // This will store the chatbot's text response
  const [audioResponseUrl, setAudioResponseUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const mediaRecorderRef = useRef(null);
  const audioChunks = useRef([]);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunks.current = [];

      mediaRecorderRef.current = new MediaRecorder(stream);
      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunks.current, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio', audioBlob, 'user_audio.wav');

        setLoading(true);
        setError(null);
        setTranscription(''); // Clear previous transcription
        setTextResponse('');    // Clear previous text response
        setAudioResponseUrl(''); // Clear previous audio URL

        try {
          const res = await fetch('http://localhost:5000/api/voice-chat', {
            method: 'POST',
            body: formData,
          });

          if (!res.ok) {
            const errorText = await res.text(); // Get error text from response
            throw new Error(`Failed to get a valid response: ${res.status} - ${errorText}`);
          }

          const data = await res.json();
          console.log("Received data:", data); // Log the received data to inspect its structure

          // Correctly assign data based on your Flask API response
          setTranscription(data.query); // User's transcribed query from Flask
          setTextResponse(data.text); // Chatbot's text response from Flask
          setAudioResponseUrl(data.audio_url); // Chatbot's audio URL from Flask

        } catch (err) {
          console.error('Error during fetch:', err);
          setError('Error contacting the chatbot. Please try again. Details: ' + err.message);
        } finally {
          setLoading(false);
        }
      };

      mediaRecorderRef.current.start();
      setRecording(true);

      // Automatically stop recording after 8 seconds
      setTimeout(() => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
          mediaRecorderRef.current.stop();
          setRecording(false);
        }
      }, 8000);
    } catch (err) {
      console.error('Error accessing microphone:', err);
      setError('Microphone access denied or unavailable. Details: ' + err.message);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', mt: 5, textAlign: 'center' }}>
      <Typography variant="h4" gutterBottom>
        🎙️ Voice Chatbot
      </Typography>

      <Button
        variant="contained"
        color={recording ? 'secondary' : 'primary'}
        onClick={startRecording}
        disabled={recording || loading}
      >
        {recording ? 'Recording…' : 'Start Recording'}
      </Button>

      {loading && (
        <Box mt={2}>
          <CircularProgress />
          <Typography variant="body2">Processing your audio...</Typography>
        </Box>
      )}

      {error && (
        <Box mt={2} color="error.main">
          <Typography variant="body2" color="error">
            {error}
          </Typography>
        </Box>
      )}

      {/* Display user's transcription */}
      {transcription && (
        <Paper elevation={2} sx={{ p: 2, mt: 3 }}>
          <Typography variant="h6">You said:</Typography>
          <Typography>{transcription}</Typography>
        </Paper>
      )}

      {/* Display chatbot's text response */}
      {textResponse && (
        <Paper elevation={2} sx={{ p: 2, mt: 2 }}>
          <Typography variant="h6">🤖 Chatbot says:</Typography>
          <Typography>{textResponse}</Typography>
        </Paper>
      )}

      {/* Play chatbot's audio response */}
      {audioResponseUrl && (
        <Box mt={3}>
          <audio controls autoPlay src={`http://localhost:5000${audioResponseUrl}`} />
        </Box>
      )}
    </Box>
  );
}