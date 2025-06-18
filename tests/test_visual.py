#!/usr/bin/env python3
"""
Teste de funcionalidades visuais do jogo Viva Sergipe!
"""

import sys
import os
import cv2
import numpy as np

# Adicionar src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sergipe_utils import load_sergipe_contour
from . import get_asset_path

def test_contour_loading():
    """Testa o carregamento do contorno de Sergipe"""
    print("🧪 Testando carregamento do contorno...")
    
    # Testar carregamento do contorno
    contour_mask = load_sergipe_contour(get_asset_path("assets/contorno-mapa-SE.png"))
    
    if contour_mask is not None:
        print(f"✅ Contorno carregado com sucesso!")
        print(f"   Dimensões: {contour_mask.shape}")
        print(f"   Pixels não-zero: {np.sum(contour_mask > 0)}")
        return True
    else:
        print("❌ Falha ao carregar contorno")
        return False

def main():
    """Função principal do teste"""
    print("🎮 VIVA SERGIPE! - Teste de Funcionalidades Visuais")
    print("=" * 50)
    
    success = test_contour_loading()
    
    if success:
        print("\n🎉 Todos os testes visuais passaram!")
    else:
        print("\n❌ Alguns testes falharam!")
    
    return success

if __name__ == "__main__":
    main()
