#!/bin/bash

# Colores para mensajes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Configurando entorno virtual para Whisper Local API...${NC}"

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado. Por favor, instálalo primero."
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 no está instalado. Por favor, instálalo primero."
    exit 1
fi

# Crear entorno virtual
echo -e "${BLUE}Creando entorno virtual...${NC}"
python3 -m venv .venv

# Activar entorno virtual
source .venv/bin/activate

# Instalar/Actualizar pip
echo -e "${BLUE}Actualizando pip...${NC}"
python -m pip install --upgrade pip

# Instalar poetry si no está instalado
if ! command -v poetry &> /dev/null; then
    echo -e "${BLUE}Instalando Poetry...${NC}"
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Configurar Poetry para usar el entorno virtual en el proyecto
poetry config virtualenvs.in-project true

# Instalar dependencias con Poetry
echo -e "${BLUE}Instalando dependencias...${NC}"
poetry install

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo -e "${BLUE}Creando archivo .env...${NC}"
    cp .env.example .env
    echo -e "${GREEN}Por favor, edita el archivo .env con tu configuración${NC}"
fi

echo -e "${GREEN}¡Configuración completada!${NC}"
echo -e "Para activar el entorno virtual:"
echo -e "${BLUE}source .venv/bin/activate${NC}"
