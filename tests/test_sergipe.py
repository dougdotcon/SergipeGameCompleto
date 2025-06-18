#!/usr/bin/env python3
"""
Teste básico do jogo Viva Sergipe!
"""

import sys
import os
import cv2
import numpy as np

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sergipe_utils import load_sergipe_contour

def get_asset_path(relative_path):
    """Função para obter caminho de assets"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(project_root, relative_path)

def test_basic_functionality():
    """Testa funcionalidades básicas do jogo"""
    print("🧪 Testando funcionalidades básicas...")
    
    # Testar carregamento do contorno
    contour_mask = load_sergipe_contour(get_asset_path("assets/contorno-mapa-SE.png"))
    
    if contour_mask is not None:
        print(f"✅ Contorno carregado com sucesso!")
        print(f"   Dimensões: {contour_mask.shape}")
        return True
    else:
        print("❌ Falha ao carregar contorno")
        return False

def main():
    """Função principal do teste"""
    print("🎮 VIVA SERGIPE! - Teste Básico")
    print("=" * 30)
    
    success = test_basic_functionality()
    
    if success:
        print("\n🎉 Teste básico passou!")
    else:
        print("\n❌ Teste básico falhou!")
    
    return success

if __name__ == "__main__":
    main()
