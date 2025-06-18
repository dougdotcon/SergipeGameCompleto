#!/usr/bin/env python3
"""
VIVA SERGIPE! - Script de Inicialização
Script que configura o ambiente e inicia o jogo automaticamente
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Configura variáveis de ambiente necessárias"""
    print("🔧 Configurando ambiente...")
    
    # Definir variável para corrigir problema do protobuf
    os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
    print("✅ Variável PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION definida")
    
    # Verificar se estamos no diretório correto
    current_dir = Path.cwd()
    game_file = current_dir / "sergipe_game.py"
    
    if not game_file.exists():
        print("❌ Arquivo sergipe_game.py não encontrado!")
        print(f"📁 Diretório atual: {current_dir}")
        print("💡 Certifique-se de executar este script no diretório do jogo")
        return False
    
    print(f"✅ Jogo encontrado em: {game_file}")
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("\n🔍 Verificando dependências...")
    
    required_modules = [
        'cv2',
        'mediapipe', 
        'pygame',
        'numpy',
        'PyQt5'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} não encontrado")
            missing_modules.append(module)
    
    if missing_modules:
        print(f"\n⚠️ Módulos faltando: {', '.join(missing_modules)}")
        print("💡 Execute: python scripts/fix_opencv.py")
        return False
    
    print("✅ Todas as dependências estão instaladas")
    return True

def start_game():
    """Inicia o jogo"""
    print("\n🎮 Iniciando VIVA SERGIPE!...")
    print("=" * 50)
    
    try:
        # Importar e executar o jogo
        import sergipe_game
        sergipe_game.main()
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Jogo interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar o jogo: {e}")
        print("\n💡 Soluções:")
        print("1. Execute: python scripts/fix_opencv.py")
        print("2. Verifique se a câmera está conectada")
        print("3. Feche outros programas que usam a câmera")
        return False
    
    return True

def main():
    """Função principal"""
    print("🎮 VIVA SERGIPE! - Inicializador v1.2")
    print("=" * 50)
    
    # Configurar ambiente
    if not setup_environment():
        input("\nPressione Enter para sair...")
        return
    
    # Verificar dependências
    if not check_dependencies():
        print("\n💡 Execute primeiro: python scripts/fix_opencv.py")
        input("\nPressione Enter para sair...")
        return
    
    # Iniciar jogo
    start_game()
    
    print("\n🎉 Obrigado por jogar VIVA SERGIPE!")

if __name__ == "__main__":
    main()
