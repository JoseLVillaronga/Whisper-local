from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import uvicorn
from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv
from whisper_module import WhisperTranscriber
from typing import Optional

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Whisper Local API")
security = HTTPBearer()

# Obtener configuración desde variables de entorno
API_KEY = os.getenv("API_KEY")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

if not API_KEY:
    raise ValueError("API_KEY no está configurada en el archivo .env")

# Configurar CORS para permitir acceso desde la red local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)) -> bool:
    """Verificar la API key proporcionada."""
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True

# Inicializar el modelo Whisper
transcriber = WhisperTranscriber(model_name=WHISPER_MODEL)

@app.get("/")
async def root(authenticated: bool = Depends(verify_api_key)):
    """Endpoint de verificación de estado del servidor."""
    return {
        "status": "online",
        "service": "Whisper Local API",
        "model": WHISPER_MODEL
    }

@app.post("/transcribe/")
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = None,
    task: str = "transcribe",
    authenticated: bool = Depends(verify_api_key)
):
    """
    Endpoint para transcribir archivos de audio.
    
    Args:
        file: Archivo de audio a transcribir
        language: Código de idioma opcional (ej: "es" para español)
        task: "transcribe" o "translate" (para traducir a inglés)
    """
    if not file.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
        raise HTTPException(400, "Formato de archivo no soportado")

    # Guardar archivo temporalmente
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        try:
            # Escribir el archivo subido al archivo temporal
            content = await file.read()
            temp_file.write(content)
            temp_file.flush()
            
            # Transcribir el audio
            result = transcriber.transcribe(
                temp_file.name,
                language=language,
                task=task
            )
            
            if "error" in result:
                raise HTTPException(500, result["error"])
                
            return result
            
        finally:
            # Limpiar el archivo temporal
            os.unlink(temp_file.name)

def start_server():
    """Iniciar el servidor API."""
    uvicorn.run(app, host=HOST, port=PORT)

if __name__ == "__main__":
    start_server()
