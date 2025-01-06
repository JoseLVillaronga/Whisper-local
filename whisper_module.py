import whisper
import multiprocessing
from typing import Optional, Union
from pathlib import Path
import logging
import os
import numpy as np
import soundfile as sf
from scipy import signal

logger = logging.getLogger(__name__)

class WhisperTranscriber:
    def __init__(self, model_name: str = "small"):
        """Initialize Whisper model with specified size."""
        logger.info(f"Inicializando modelo Whisper: {model_name}")
        self.model = whisper.load_model(model_name)
        logger.info(f"Modelo cargado exitosamente")

    def preprocess_audio(self, audio_data: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Preprocesa el audio para mejorar la calidad de la transcripción.
        """
        # Asegurar que los datos estén en float32
        audio_data = audio_data.astype(np.float32)
        
        # Convertir a mono si es estéreo
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)

        # Normalizar el audio
        max_abs = np.max(np.abs(audio_data))
        if max_abs > 0:
            audio_data = audio_data / max_abs

        # Aplicar un filtro paso alto para reducir ruido de baja frecuencia
        nyquist = sample_rate / 2
        cutoff = 100  # Hz
        b, a = signal.butter(4, cutoff/nyquist, btype='high', analog=False)
        audio_data = signal.filtfilt(b, a, audio_data).astype(np.float32)

        # Aplicar un filtro de énfasis en frecuencias de voz (300-3000 Hz)
        b, a = signal.butter(4, [300/nyquist, 3000/nyquist], btype='band', analog=False)
        audio_data = signal.filtfilt(b, a, audio_data).astype(np.float32)

        # Reducción de ruido simple
        noise_threshold = np.std(audio_data) * 2
        audio_data[np.abs(audio_data) < noise_threshold] = 0

        # Normalizar nuevamente después del filtrado
        max_abs = np.max(np.abs(audio_data))
        if max_abs > 0:
            audio_data = audio_data / max_abs

        return audio_data.astype(np.float32)

    def transcribe(
        self,
        audio_path: Union[str, Path],
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
        audio_path = str(audio_path)
        logger.info(f"Intentando transcribir archivo: {audio_path}")
        
        # Verificar que el archivo existe
        if not os.path.exists(audio_path):
            error_msg = f"El archivo no existe: {audio_path}"
            logger.error(error_msg)
            return {"error": error_msg}
            
        # Cargar el audio directamente en memoria
        try:
            logger.info("Cargando archivo de audio en memoria...")
            audio_data, sample_rate = sf.read(audio_path, dtype=np.float32)
            
            # Preprocesar el audio
            logger.info("Preprocesando audio...")
            audio_data = self.preprocess_audio(audio_data, sample_rate)
            
            # Verificar que los datos están en float32
            logger.info(f"Tipo de datos del audio: {audio_data.dtype}")
            logger.info(f"Audio procesado: {len(audio_data)} muestras, {sample_rate}Hz")
            
        except Exception as e:
            error_msg = f"Error al cargar el audio: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
        
        options = {
            "task": task,
            "language": language,
            "temperature": 0,      # Más determinístico
            "best_of": 5,         # Número de muestras a considerar
            "beam_size": 5,       # Beam search para mejor decodificación
            "condition_on_previous_text": True,  # Usar contexto previo
            "initial_prompt": "Transcripción en español: "  # Ayuda al modelo con el contexto
        }
        
        try:
            logger.info(f"Iniciando transcripción con opciones: {options}")
            
            # Si no se especifica el idioma, intentar detectarlo primero
            if language is None:
                logger.info("Detectando idioma del audio...")
                audio_features = self.model.embed_audio(audio_data)
                _, probs = self.model.detect_language(audio_features)
                detected_lang = max(probs, key=probs.get)
                logger.info(f"Idioma detectado: {detected_lang}")
                options["language"] = detected_lang
            else:
                logger.info(f"Usando idioma especificado: {language}")
            
            # Usar el audio en memoria en lugar del archivo
            result = self.model.transcribe(
                audio_data,
                **{k: v for k, v in options.items() if v is not None}
            )
            
            # Si no se detectó texto, intentar con diferentes parámetros
            if not result.get("text", "").strip():
                logger.info("No se detectó texto, intentando con diferentes parámetros...")
                options["temperature"] = 0.2
                options["best_of"] = 1
                result = self.model.transcribe(
                    audio_data,
                    **{k: v for k, v in options.items() if v is not None}
                )
            
            logger.info("Transcripción completada exitosamente")
            return result
        except Exception as e:
            error_msg = f"Error durante la transcripción: {str(e)}"
            logger.error(error_msg)
            return {"error": error_msg}
