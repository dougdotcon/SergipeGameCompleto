@echo off
title VIVA SERGIPE! v1.2.0
echo 🎮 VIVA SERGIPE! v1.2.0 - VERSAO FINAL
echo ========================================
echo.
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado!
    echo Instale Python 3.7+ em python.org
    pause
    exit /b 1
)
echo ✅ Python OK
echo.
echo Verificando dependencias...
python -c "import cv2, mediapipe, pygame, PyQt5, numpy, psutil" 2>nul
if errorlevel 1 (
    echo ❌ Dependencias nao instaladas!
    echo.
    echo Para instalar:
    echo pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)
echo ✅ Dependencias OK
echo.
echo 🚀 Iniciando VIVA SERGIPE!...
echo.
python sergipe_game.py
if errorlevel 1 (
    echo.
    echo ❌ Erro ao executar o jogo
    echo Verifique a documentacao em docs/
    pause
)
