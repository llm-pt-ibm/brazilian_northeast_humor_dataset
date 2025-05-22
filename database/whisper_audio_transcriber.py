"""
Whisper Audio Transcriber Module

This module provides a class that wraps OpenAI's Whisper model for transcribing
audio files into text.

It uses the "large" version of the Whisper model, which provides high transcription
accuracy at the cost of increased memory and computation time.

Dependencies:
- whisper (OpenAI's Whisper library)

Class:
    WhisperAudioTranscriber
"""
import whisper


class WhisperAudioTranscriber:
    """
    A class that uses the Whisper model to transcribe speech from audio files.
    """

    def __init__(self):
        """
        Loads the Whisper model in 'large' configuration for high-accuracy transcription.
        """
        self.model = whisper.load_model("large")

    def extract_text_from_audio(self, audio_path: str):
        """
        Transcribes an audio file to text using the Whisper model.

        Args:
            audio_path (str): Path to the input audio file.

        Returns:
            str: Transcribed text. Returns an empty string if transcription fails.
        """
        try:
            result = self.model.transcribe(audio_path)
            return result['text']
        except Exception as e:
            return ''
