#!/usr/bin/env python3
"""
Teste do menu PyQt para o jogo Viva Sergipe!
"""

import sys
import os

# Adiciona o diretório atual ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from menu_gui import show_menu
    
    def test_menu():
        """Testa o menu PyQt"""
        print("Iniciando teste do menu...")
        
        # Testa o menu
        result = show_menu()
        
        if result:
            print("✅ Menu funcionou! Usuário escolheu JOGAR")
        else:
            print("✅ Menu funcionou! Usuário escolheu SAIR")
        
        return result
    
    if __name__ == "__main__":
        test_menu()
        
except ImportError as e:
    print(f"❌ Erro de importação: {e}")
    print("Certifique-se de que PyQt5 está instalado:")
    print("pip install PyQt5")
    
except Exception as e:
    print(f"❌ Erro inesperado: {e}")
