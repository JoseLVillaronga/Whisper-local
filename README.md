# Whisper Local API

Servidor API local para transcripción de audio usando Whisper de OpenAI.

## Requisitos del Sistema

- Python 3.10 o superior
- pip3
- Conexión a internet (para la instalación inicial)
- CPU multicore (optimizado para AMD Ryzen 5 5600G)
- Mínimo 8GB RAM (recomendado 16GB+)

## Instalación

### Linux/macOS

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd Whisper-local
```

2. Ejecutar el script de configuración:
```bash
chmod +x setup.sh
./setup.sh
```

3. Activar el entorno virtual:
```bash
source .venv/bin/activate
```

### Windows

1. Clonar el repositorio:
```cmd
git clone <repository-url>
cd Whisper-local
```

2. Ejecutar el script de configuración:
```cmd
setup.bat
```

3. Activar el entorno virtual:
```cmd
.venv\Scripts\activate.bat
```

### Configuración

El script de configuración creará automáticamente un archivo `.env` basado en `.env.example`. Edita el archivo `.env` y configura las siguientes variables:

- `API_KEY`: Tu clave de API para autenticación
- `HOST`: Host donde se ejecutará el servidor (default: 0.0.0.0)
- `PORT`: Puerto para el servidor (default: 8000)
- `WHISPER_MODEL`: Modelo de Whisper a usar (default: base)

## Uso

1. Activar el entorno virtual (si no está activado):
```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate.bat
```

2. Iniciar el servidor API:
```bash
poetry run python api_server.py
```

El servidor se iniciará en `http://0.0.0.0:8000` (o la configuración especificada en `.env`)

## Endpoints

### 1. Verificar Estado del Servidor
```bash
curl -X GET "http://localhost:8000/" \
     -H "Authorization: Bearer tu-api-key"
```

Respuesta:
```json
{
    "status": "online",
    "service": "Whisper Local API",
    "model": "base"
}
```

### 2. Transcribir Audio
```bash
# Transcribir audio en español
curl -X POST "http://localhost:8000/transcribe/" \
     -H "Authorization: Bearer tu-api-key" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@audio.mp3" \
     -F "language=es"

# Traducir audio a inglés
curl -X POST "http://localhost:8000/transcribe/" \
     -H "Authorization: Bearer tu-api-key" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@audio.mp3" \
     -F "task=translate"
```

Respuesta:
```json
{
    "text": "Transcripción del audio...",
    "segments": [...],
    "language": "es"
}
```

## Formatos de Audio Soportados
- MP3 (.mp3)
- WAV (.wav)
- M4A (.m4a)
- OGG (.ogg)

## Seguridad

La API está protegida mediante autenticación Bearer token. Todas las solicitudes deben incluir el header:
```
Authorization: Bearer tu-api-key
```

La API key debe configurarse en el archivo `.env`. Por seguridad, nunca compartas tu archivo `.env` ni lo subas al control de versiones.

## Solución de Problemas

### Error al activar el entorno virtual en Windows
Si PowerShell muestra un error de permisos al activar el entorno virtual, ejecuta:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error de Poetry no encontrado
Si después de instalar Poetry el comando no es reconocido, reinicia tu terminal o agrega Poetry al PATH manualmente.

## Notas

- El servidor está configurado para usar CPU principalmente
- Utiliza multiprocessing para optimizar el rendimiento en CPU multicore
- Por defecto usa el modelo "base" de Whisper para balance entre precisión y recursos
- Todos los endpoints requieren autenticación Bearer
- El entorno virtual (.venv) aísla las dependencias del proyecto del sistema principal
