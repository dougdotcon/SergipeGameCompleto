#!/usr/bin/env python3
"""
Teste de instalação e dependências do jogo Viva Sergipe!
"""

import sys
import os
import cv2
import numpy as np
import pygame
import mediapipe as mp

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sergipe_utils import load_sergipe_contour

def get_asset_path(relative_path):
    """Função para obter caminho de assets"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, relative_path)

def test_dependencies():
    """Testa se todas as dependências estão instaladas"""
    print("🧪 Testando dependências...")
    
    dependencies = [
        ('cv2', cv2),
        ('numpy', np),
        ('pygame', pygame),
        ('mediapipe', mp)
    ]
    
    all_ok = True
    for name, module in dependencies:
        try:
            version = getattr(module, '__version__', 'N/A')
            print(f"✅ {name}: {version}")
        except Exception as e:
            print(f"❌ {name}: Erro - {e}")
            all_ok = False
    
    return all_ok

def test_assets():
    """Testa se os assets estão disponíveis"""
    print("\n🧪 Testando assets...")
    
    assets_to_test = [
        'assets/contorno-mapa-SE.png',
        'assets/flag-se.jpg',
        'sounds/background.mp3',
        'sounds/confirmation.mp3'
    ]
    
    all_ok = True
    for asset in assets_to_test:
        try:
            asset_path = get_asset_path(asset)
            if os.path.exists(asset_path):
                print(f"✅ {asset}")
            else:
                print(f"❌ {asset} - Arquivo não encontrado")
                all_ok = False
        except Exception as e:
            print(f"❌ {asset} - Erro: {e}")
            all_ok = False
    
    return all_ok

def test_contour_loading():
    """Testa o carregamento do contorno"""
    print("\n🧪 Testando carregamento do contorno...")
    
    try:
        contour_mask = load_sergipe_contour(get_asset_path("assets/contorno-mapa-SE.png"))
        
        if contour_mask is not None:
            print(f"✅ Contorno carregado com sucesso!")
            print(f"   Dimensões: {contour_mask.shape}")
            print(f"   Pixels não-zero: {np.sum(contour_mask > 0)}")
            return True
        else:
            print("❌ Falha ao carregar contorno")
            return False
    except Exception as e:
        print(f"❌ Erro ao carregar contorno: {e}")
        return False

def main():
    """Função principal do teste"""
    print("🎮 VIVA SERGIPE! - Teste de Instalação")
    print("=" * 50)
    
    tests = [
        ("Dependências", test_dependencies),
        ("Assets", test_assets),
        ("Contorno", test_contour_loading)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Instalação completa e funcional!")
        print("🚀 O jogo está pronto para ser executado!")
    else:
        print("⚠️ Alguns problemas foram encontrados.")
        print("💡 Execute: python scripts/fix_opencv.py")
    
    return passed == total

if __name__ == "__main__":
    main()
