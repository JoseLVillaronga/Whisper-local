from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Security, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import uvicorn
from pathlib import Path
import tempfile
import os
import logging
from dotenv import load_dotenv
from whisper_module import WhisperTranscriber
from typing import Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    request: Request,
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
    # Obtener el idioma del form-data si está presente
    form = await request.form()
    if "language" in form:
        language = form["language"]
    
    logger.info(f"Idioma seleccionado: {language}")
    
    if not file.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
        raise HTTPException(400, "Formato de archivo no soportado")

    logger.info(f"Procesando archivo: {file.filename}")
    
    # Crear directorio temporal si no existe
    temp_dir = Path(tempfile.gettempdir()) / "whisper_api"
    temp_dir.mkdir(exist_ok=True)
    
    # Crear archivo temporal con extensión
    temp_file_path = temp_dir / f"temp_{os.urandom(8).hex()}{Path(file.filename).suffix}"
    
    try:
        # Escribir el archivo subido al archivo temporal
        content = await file.read()
        with open(temp_file_path, 'wb') as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())  # Forzar escritura a disco
        
        logger.info(f"Archivo temporal creado en: {temp_file_path}")
        logger.info(f"Tamaño del archivo: {len(content)} bytes")
        
        # Verificar que el archivo existe y es accesible
        if not temp_file_path.exists():
            raise Exception(f"El archivo temporal no existe después de crearlo: {temp_file_path}")
            
        # Transcribir el audio
        result = transcriber.transcribe(
            str(temp_file_path),
            language=language,
            task=task
        )
        
        if "error" in result:
            logger.error(f"Error en la transcripción: {result['error']}")
            raise HTTPException(500, result["error"])
            
        logger.info("Transcripción completada exitosamente")
        return result
        
    except Exception as e:
        logger.error(f"Error durante el proceso: {str(e)}")
        raise HTTPException(500, str(e))
        
    finally:
        # Intentar eliminar el archivo temporal
        try:
            if temp_file_path.exists():
                temp_file_path.unlink()
                logger.info(f"Archivo temporal eliminado: {temp_file_path}")
        except Exception as e:
            logger.warning(f"No se pudo eliminar el archivo temporal: {str(e)}")

def start_server():
    """Iniciar el servidor API."""
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info"
    )

if __name__ == "__main__":
    start_server()
