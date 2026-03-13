#!/bin/bash

# Interrompe o script se qualquer comando falhar
set -e

# Caminho para o ambiente virtual
VENV_DIR="./venv"

echo "➡️ Criando ambiente virtual em $VENV_DIR..."
python3 -m venv "$VENV_DIR"
echo "✅ Ambiente virtual criado."

# Atualiza o pip
echo "➡️ Atualizando pip..."
"$VENV_DIR/bin/python" -m pip install --upgrade pip
echo "✅ pip atualizado."

# Instala dependências
if [ -f "requirements.txt" ]; then
    echo "➡️ Instalando dependências de requirements.txt..."
    "$VENV_DIR/bin/pip" install -r requirements.txt
    echo "✅ Dependências instaladas."
else
    echo "⚠️ Arquivo requirements.txt não encontrado. Nenhuma dependência instalada."
fi

echo "✅ Setup concluído com sucesso."
