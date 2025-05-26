#!/bin/bash
echo "🎮 VIVA SERGIPE! v1.2.0 - VERSAO FINAL"
echo "========================================"
echo
echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado!"
    echo "Instale Python 3.7+ em python.org"
    read -p "Pressione Enter para sair..."
    exit 1
fi
echo "✅ Python OK"
echo
echo "Verificando dependências..."
python3 -c "import cv2, mediapipe, pygame, PyQt5, numpy, psutil" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependências não instaladas!"
    echo
    echo "Para instalar:"
    echo "pip3 install -r requirements.txt"
    echo
    read -p "Pressione Enter para sair..."
    exit 1
fi
echo "✅ Dependências OK"
echo
echo "🚀 Iniciando VIVA SERGIPE!..."
echo
python3 sergipe_game.py
if [ $? -ne 0 ]; then
    echo
    echo "❌ Erro ao executar o jogo"
    echo "Verifique a documentação em docs/"
    read -p "Pressione Enter para sair..."
fi
