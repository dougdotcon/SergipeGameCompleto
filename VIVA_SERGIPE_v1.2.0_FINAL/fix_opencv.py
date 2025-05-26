#!/usr/bin/env python3
"""
Script para corrigir problemas do OpenCV no Windows
"""

import subprocess
import sys
import os

def run_command(command):
    """Executa um comando e mostra o resultado"""
    print(f"Executando: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Sucesso!")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Erro:")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro executando comando: {e}")
        return False

def fix_opencv():
    """Corrige problemas do OpenCV"""
    print("🔧 Corrigindo OpenCV para Windows...")
    print()
    
    # Desinstalar versões problemáticas
    print("1. Removendo versões antigas do OpenCV...")
    commands_uninstall = [
        "pip uninstall opencv-python -y",
        "pip uninstall opencv-python-headless -y", 
        "pip uninstall opencv-contrib-python -y",
        "pip uninstall opencv-contrib-python-headless -y"
    ]
    
    for cmd in commands_uninstall:
        run_command(cmd)
    
    print()
    print("2. Instalando OpenCV com suporte GUI...")
    
    # Instalar versão correta
    success = run_command("pip install opencv-python==4.8.0.76")
    
    if not success:
        print("Tentando versão alternativa...")
        success = run_command("pip install opencv-python")
    
    print()
    print("3. Testando OpenCV...")
    
    # Testar OpenCV
    try:
        import cv2
        print(f"✅ OpenCV versão: {cv2.__version__}")
        
        # Testar criação de janela
        try:
            cv2.namedWindow("Teste", cv2.WINDOW_NORMAL)
            cv2.destroyAllWindows()
            print("✅ Suporte a janelas funcionando!")
        except Exception as e:
            print(f"❌ Erro no suporte a janelas: {e}")
            return False
            
        # Testar câmera
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                print("✅ Câmera detectada!")
                cap.release()
            else:
                print("⚠️ Câmera não detectada (pode estar em uso)")
        except Exception as e:
            print(f"⚠️ Erro testando câmera: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro importando OpenCV: {e}")
        return False

def install_all_requirements():
    """Instala todas as dependências"""
    print()
    print("4. Instalando outras dependências...")
    
    requirements = [
        "mediapipe",
        "numpy", 
        "pygame",
        "PyQt5"
    ]
    
    for req in requirements:
        run_command(f"pip install {req}")

if __name__ == "__main__":
    print("🎮 VIVA SERGIPE! - Correção de Dependências")
    print("=" * 50)
    
    if fix_opencv():
        print()
        print("✅ OpenCV corrigido com sucesso!")
        install_all_requirements()
        print()
        print("🎉 Todas as dependências instaladas!")
        print()
        print("Agora você pode executar:")
        print("python sergipe_game.py")
    else:
        print()
        print("❌ Falha ao corrigir OpenCV")
        print()
        print("Soluções alternativas:")
        print("1. Reinicie o terminal como administrador")
        print("2. Execute: pip install --upgrade pip")
        print("3. Execute: pip install opencv-python --force-reinstall")
        print("4. Se persistir, instale Visual C++ Redistributable")
