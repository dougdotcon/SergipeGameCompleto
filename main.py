#!/usr/bin/env python3
"""
Arquivo principal para execução do jogo Viva Sergipe!
Este arquivo serve como ponto de entrada principal do jogo.
"""

import sys
import os

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Função principal que inicia o jogo"""
    try:
        # Mudar para o diretório src antes de executar
        src_dir = os.path.join(os.path.dirname(__file__), 'src')
        original_dir = os.getcwd()
        os.chdir(src_dir)
        
        from start_game import main as start_game_main
        start_game_main()
        
        # Voltar para o diretório original
        os.chdir(original_dir)
        
    except ImportError as e:
        print(f"Erro ao importar módulos: {e}")
        print("Certifique-se de que todas as dependências estão instaladas.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 