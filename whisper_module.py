import whisper
import multiprocessing
from typing import Optional
from pathlib import Path

class WhisperTranscriber:
    def __init__(self, model_name: str = "base"):
        """Initialize Whisper model with specified size."""
        self.model = whisper.load_model(model_name)
        self.num_cpus = multiprocessing.cpu_count()

    def transcribe(
        self,
        audio_path: str | Path,
        language: Optional[str] = None,
        task: str = "transcribe"
    ) -> dict:
        """
        Transcribe audio file using Whisper.
        
        Args:
            audio_path: Path to audio file
            language: Optional language code (e.g., "es" for Spanish)
            task: Either "transcribe" or "translate" (to English)
        
        Returns:
            Dictionary containing transcription results
        """
        options = {
            "task": task,
            "language": language,
            "num_workers": max(1, self.num_cpus - 1)
        }
        
        try:
            result = self.model.transcribe(
                str(audio_path),
                **{k: v for k, v in options.items() if v is not None}
            )
            return result
        except Exception as e:
            return {"error": str(e)}
