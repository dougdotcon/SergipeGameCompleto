#!/usr/bin/env python3
"""
VIVA SERGIPE! - Teste de Instalação
Verifica se todos os componentes estão funcionando corretamente
"""

import os
import sys
import importlib
from pathlib import Path

def test_python_version():
    """Testa versão do Python"""
    print("🐍 Testando versão do Python...")
    
    version = sys.version_info
    if version >= (3, 7):
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (mínimo: 3.7)")
        return False

def test_environment_variables():
    """Testa variáveis de ambiente"""
    print("\n🌍 Testando variáveis de ambiente...")
    
    # Definir variável se não existir
    if 'PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION' not in os.environ:
        os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
        print("✅ Variável PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION definida")
    else:
        print("✅ Variável PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION já existe")
    
    return True

def test_dependencies():
    """Testa importação de dependências"""
    print("\n📦 Testando dependências...")
    
    dependencies = {
        'cv2': 'OpenCV',
        'numpy': 'NumPy',
        'pygame': 'Pygame',
        'mediapipe': 'MediaPipe',
        'PyQt5': 'PyQt5'
    }
    
    results = {}
    
    for module, name in dependencies.items():
        try:
            imported_module = importlib.import_module(module)
            version = getattr(imported_module, '__version__', 'N/A')
            print(f"✅ {name} v{version}")
            results[module] = True
        except ImportError as e:
            print(f"❌ {name}: {e}")
            results[module] = False
    
    return all(results.values())

def test_game_files():
    """Testa presença dos arquivos do jogo"""
    print("\n📁 Testando arquivos do jogo...")
    
    required_files = [
        'sergipe_game.py',
        'sergipe_utils.py',
        'utils.py',
        'config_manager.py',
        'assets/contorno-mapa-SE.png'
    ]
    
    optional_files = [
        'start_game.py',
        'VIVA_SERGIPE.bat',
        'fix_opencv.py',
        'requirements.txt'
    ]
    
    all_present = True
    
    # Arquivos obrigatórios
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (obrigatório)")
            all_present = False
    
    # Arquivos opcionais
    for file in optional_files:
        if Path(file).exists():
            print(f"✅ {file} (opcional)")
        else:
            print(f"⚠️ {file} (opcional - não encontrado)")
    
    return all_present

def test_camera():
    """Testa acesso à câmera"""
    print("\n📷 Testando câmera...")
    
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            # Tentar ler um frame
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"✅ Câmera funcionando - Resolução: {frame.shape[1]}x{frame.shape[0]}")
                cap.release()
                return True
            else:
                print("⚠️ Câmera detectada mas não consegue capturar frames")
                cap.release()
                return False
        else:
            print("❌ Não foi possível abrir a câmera")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao testar câmera: {e}")
        return False

def test_game_components():
    """Testa componentes específicos do jogo"""
    print("\n🎮 Testando componentes do jogo...")
    
    try:
        # Testar carregamento do contorno
        from sergipe_utils import load_sergipe_contour
        contour = load_sergipe_contour("assets/contorno-mapa-SE.png")
        
        if contour is not None:
            print("✅ Contorno de Sergipe carregado")
        else:
            print("❌ Erro ao carregar contorno de Sergipe")
            return False
        
        # Testar MediaPipe
        from utils import initialize_pose_model
        pose = initialize_pose_model()
        
        if pose is not None:
            print("✅ MediaPipe inicializado")
        else:
            print("❌ Erro ao inicializar MediaPipe")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos componentes do jogo: {e}")
        return False

def run_comprehensive_test():
    """Executa teste completo"""
    print("🎮 VIVA SERGIPE! - Teste de Instalação")
    print("=" * 50)
    
    tests = [
        ("Versão do Python", test_python_version),
        ("Variáveis de ambiente", test_environment_variables),
        ("Dependências", test_dependencies),
        ("Arquivos do jogo", test_game_files),
        ("Câmera", test_camera),
        ("Componentes do jogo", test_game_components)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste '{test_name}': {e}")
            results.append((test_name, False))
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 INSTALAÇÃO PERFEITA!")
        print("✅ Todos os testes passaram")
        print("🚀 O jogo está pronto para ser executado")
        print("\nPara jogar:")
        print("• Windows: Clique duas vezes em VIVA_SERGIPE.bat")
        print("• Ou execute: python start_game.py")
        print("• Ou execute: python sergipe_game.py")
    else:
        print(f"\n⚠️ {total - passed} teste(s) falharam")
        print("💡 Soluções:")
        print("1. Execute: python fix_opencv.py")
        print("2. Instale dependências: pip install -r requirements.txt")
        print("3. Verifique se a câmera está conectada")
        print("4. Consulte INSTALACAO.md para mais detalhes")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_comprehensive_test()
        input(f"\nPressione Enter para sair...")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido pelo usuário")
        sys.exit(1)
