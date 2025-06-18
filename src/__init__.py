"""
Módulo principal do jogo Viva Sergipe!
Contém todos os componentes principais do jogo.
"""

import os

__version__ = "1.2.0"
__author__ = "Equipe Viva Sergipe"

def get_project_root():
    """Retorna o caminho absoluto para a raiz do projeto"""
    # Se estamos em src/, sobe um nível para a raiz
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(current_dir) == 'src':
        return os.path.dirname(current_dir)
    # Se estamos na raiz, retorna o diretório atual
    return current_dir

def get_asset_path(relative_path):
    """Retorna o caminho absoluto para um asset"""
    return os.path.join(get_project_root(), relative_path)

def get_sound_path(relative_path):
    """Retorna o caminho absoluto para um arquivo de som"""
    return os.path.join(get_project_root(), relative_path) 