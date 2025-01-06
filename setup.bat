@echo off
SETLOCAL EnableDelayedExpansion

echo Configurando entorno virtual de Python...

:: Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no está instalado o no está en el PATH
    echo Por favor, instala Python desde https://www.python.org/downloads/
    exit /b 1
)

:: Verificar si ffmpeg está instalado
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo Error: FFmpeg no está instalado o no está en el PATH
    echo Por favor, instala FFmpeg desde https://ffmpeg.org/download.html
    echo y agrega la carpeta bin al PATH del sistema
    exit /b 1
)

:: Crear entorno virtual si no existe
if not exist .venv (
    echo Creando entorno virtual...
    python -m venv .venv
) else (
    echo Entorno virtual ya existe
)

:: Activar entorno virtual
call .venv\Scripts\activate.bat

:: Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip

:: Instalar dependencias
echo Instalando dependencias...
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install openai-whisper
pip install fastapi
pip install python-multipart
pip install uvicorn
pip install python-dotenv
pip install numpy
pip install soundfile
pip install scipy

:: Crear archivo .env si no existe
if not exist .env (
    echo Creando archivo .env...
    echo API_KEY=5d93bb84-d748-4236-f203-5ec3673c7b9e> .env
    echo HOST=0.0.0.0>> .env
    echo PORT=8000>> .env
    echo WHISPER_MODEL=small>> .env
) else (
    echo Archivo .env ya existe
)

echo.
echo Instalación completada exitosamente!
echo.
echo Para iniciar el servidor:
echo 1. Activa el entorno virtual: .venv\Scripts\activate.bat
echo 2. Ejecuta: python api_server.py
echo.
echo Para hacer una prueba:
echo curl -X POST "http://localhost:8000/transcribe/" ^
    -H "Authorization: Bearer 5d93bb84-d748-4236-f203-5ec3673c7b9e" ^
    -H "accept: application/json" ^
    -H "Content-Type: multipart/form-data" ^
    -F "file=@tu-archivo.wav" ^
    -F "language=es"

pause
