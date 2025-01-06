# Whisper Local API

Una implementación local de la API de Whisper para transcripción de audio usando FastAPI.

## Características

- Transcripción de audio usando el modelo Whisper de OpenAI
- Soporte para múltiples idiomas con detección automática
- Preprocesamiento de audio para mejorar la calidad de transcripción
- API RESTful con autenticación por token
- Soporte para Windows y Linux

## Requisitos

- Python 3.8 o superior
- FFmpeg (requerido para procesar archivos de audio)
- Torch (CPU o GPU)
- 2GB de espacio en disco para los modelos

## Instalación

### Windows

1. Instalar Python 3.8 o superior desde [python.org](https://www.python.org/downloads/)

2. Instalar FFmpeg:
   - Descargar FFmpeg desde [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extraer el archivo zip
   - Agregar la carpeta `bin` al PATH del sistema

3. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/whisper-local.git
   cd whisper-local
   ```

4. Ejecutar el script de configuración:
   ```bash
   setup.bat
   ```

### Linux

1. Instalar dependencias del sistema:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv ffmpeg
   ```

2. Clonar el repositorio y configurar:
   ```bash
   git clone https://github.com/tu-usuario/whisper-local.git
   cd whisper-local
   ./setup.sh
   ```

## Configuración

1. Copiar `.env.example` a `.env`:
   ```bash
   cp .env.example .env
   ```

2. Editar `.env` con tus configuraciones:
   ```
   API_KEY=tu-api-key
   HOST=0.0.0.0
   PORT=8000
   WHISPER_MODEL=small  # opciones: tiny, base, small, medium, large
   ```

## Uso

1. Iniciar el servidor:
   ```bash
   python api_server.py
   ```

2. Hacer una petición de transcripción:
   ```bash
   curl -X POST "http://localhost:8000/transcribe/" \
        -H "Authorization: Bearer tu-api-key" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@tu-archivo.wav" \
        -F "language=es"  # opcional
   ```

## Modelos Disponibles

- `tiny`: Más rápido, menos preciso (~1GB RAM)
- `base`: Balance entre velocidad y precisión (~1GB RAM)
- `small`: Mejor precisión, más lento (~2GB RAM)
- `medium`: Alta precisión, muy lento (~5GB RAM)
- `large`: Máxima precisión, extremadamente lento (~10GB RAM)

## Solución de Problemas

### Windows

1. Error "FFmpeg not found":
   - Verificar que FFmpeg está en el PATH
   - Reiniciar la terminal después de agregar FFmpeg al PATH

2. Error de CUDA:
   - Por defecto se usa CPU
   - Para GPU, instalar CUDA Toolkit y cuDNN
   - Actualizar torch con soporte CUDA: `pip install torch --index-url https://download.pytorch.org/whl/cu118`

3. Error de tipos de datos:
   - Asegurarse de tener instalado scipy: `pip install scipy`
   - Los archivos de audio deben estar en formato WAV o MP3

### Linux

1. Error de permisos FFmpeg:
   ```bash
   sudo chmod +x /usr/bin/ffmpeg
   ```

2. Error de memoria:
   - Usar un modelo más pequeño en `.env`
   - Cerrar aplicaciones innecesarias

## Notas de Desarrollo

- El preprocesamiento de audio incluye:
  - Normalización de amplitud
  - Filtrado de frecuencias para voz (300-3000 Hz)
  - Reducción de ruido básica

- Parámetros de transcripción optimizados:
  - `temperature=0`: Más determinístico
  - `best_of=5`: Mejores resultados
  - `beam_size=5`: Mejor decodificación
  - `condition_on_previous_text=True`: Usa contexto

## Contribuir

1. Fork el repositorio
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Crear un Pull Request

## Licencia

MIT
