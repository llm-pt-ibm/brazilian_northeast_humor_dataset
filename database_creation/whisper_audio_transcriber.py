import whisper

class WhisperAudioTranscriber:

    def __init__(self):
        self.model = whisper.load_model("large")

    def extract_text_from_audio(self, audio_path: str):
        try:
            result = self.model.transcribe(audio_path)
            return result['text']
        
        except Exception as e:
            print(str(e))
            return ''