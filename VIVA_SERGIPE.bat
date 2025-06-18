@echo off
title VIVA SERGIPE! - Jogo Interativo de Sergipe
color 0A

echo.
echo ========================================
echo    VIVA SERGIPE! - Jogo Interativo
echo ========================================
echo.

REM Definir variável de ambiente para corrigir protobuf
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale Python 3.7+ e tente novamente.
    echo.
    pause
    exit /b 1
)

REM Verificar se o arquivo principal existe
if not exist "main.py" (
    echo ERRO: Arquivo main.py nao encontrado!
    echo Certifique-se de estar no diretorio correto do jogo.
    echo.
    pause
    exit /b 1
)

echo Iniciando o jogo...
echo.

REM Executar o arquivo principal
python main.py

REM Verificar se houve erro
if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERRO AO INICIAR O JOGO
    echo ========================================
    echo.
    echo Possiveis solucoes:
    echo 1. Execute: python scripts/fix_opencv.py
    echo 2. Verifique se a camera esta conectada
    echo 3. Feche outros programas que usam a camera
    echo 4. Reinstale as dependencias
    echo.
    echo Para corrigir dependencias, execute:
    echo python scripts/fix_opencv.py
    echo.
)

echo.
echo Obrigado por jogar VIVA SERGIPE!
pause
