@echo off
echo Configurando entorno virtual para Whisper Local API...

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no esta instalado. Por favor, instalalo primero.
    exit /b 1
)

REM Verificar si pip está instalado
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip no esta instalado. Por favor, instalalo primero.
    exit /b 1
)

REM Crear entorno virtual
echo Creando entorno virtual...
python -m venv .venv

REM Activar entorno virtual
call .venv\Scripts\activate.bat

REM Instalar/Actualizar pip
echo Actualizando pip...
python -m pip install --upgrade pip

REM Instalar poetry si no está instalado
poetry --version >nul 2>&1
if errorlevel 1 (
    echo Instalando Poetry...
    curl -sSL https://install.python-poetry.org | python -
)

REM Configurar Poetry para usar el entorno virtual en el proyecto
poetry config virtualenvs.in-project true

REM Instalar dependencias con Poetry
echo Instalando dependencias...
poetry install

REM Crear archivo .env si no existe
if not exist .env (
    echo Creando archivo .env...
    copy .env.example .env
    echo Por favor, edita el archivo .env con tu configuracion
)

echo Configuracion completada!
echo Para activar el entorno virtual:
echo .venv\Scripts\activate.bat
