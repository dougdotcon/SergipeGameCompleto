"""
GERENCIADOR DE CONFIGURAÇÕES - VIVA SERGIPE!
Sistema para salvar e carregar configurações do jogo de forma persistente
"""

import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    """Gerenciador de configurações do jogo"""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Inicializa o gerenciador de configurações
        
        Args:
            config_file (str): Caminho para o arquivo de configuração
        """
        self.config_file = config_file
        self.default_config = {
            # Configurações do jogo
            "game": {
                "duration": 300,  # 5 minutos em segundos
                "win_threshold": 30.0,  # 30% de preenchimento para vencer
                "min_body_pixels": 1000,  # Mínimo de pixels do corpo para detecção válida
                "fullscreen": True,  # Iniciar em tela cheia
                "auto_save_photos": True,  # Salvar fotos automaticamente
            },
            
            # Configurações de áudio
            "audio": {
                "master_volume": 0.7,  # Volume geral (0.0 a 1.0)
                "music_volume": 0.5,   # Volume da música de fundo
                "effects_volume": 0.8, # Volume dos efeitos sonoros
                "voice_volume": 0.9,   # Volume dos comandos de voz
                "mute_all": False,     # Silenciar tudo
            },
            
            # Configurações visuais
            "visual": {
                "contour_color": [0, 255, 0],  # Cor do contorno (BGR)
                "contour_thickness": 3,        # Espessura do contorno
                "show_percentage": True,       # Mostrar percentual
                "show_timer": True,           # Mostrar timer
                "show_progress_bar": True,    # Mostrar barra de progresso
                "camera_mirror": True,        # Espelhar câmera
            },
            
            # Configurações da câmera
            "camera": {
                "device_id": 0,        # ID da câmera (0 = padrão)
                "resolution_width": 1280,  # Largura da resolução
                "resolution_height": 720,  # Altura da resolução
                "fps": 30,             # Frames por segundo
            },
            
            # Configurações de interface
            "interface": {
                "language": "pt-BR",   # Idioma da interface
                "theme": "sergipe",    # Tema visual
                "font_size": 1.0,      # Multiplicador do tamanho da fonte
                "show_help_on_start": True,  # Mostrar ajuda na primeira execução
            },
            
            # Estatísticas e dados do usuário
            "stats": {
                "games_played": 0,     # Número de jogos jogados
                "games_won": 0,        # Número de jogos vencidos
                "best_percentage": 0.0, # Melhor percentual alcançado
                "best_time": 0.0,      # Melhor tempo para alcançar a meta
                "total_playtime": 0.0, # Tempo total jogado (segundos)
                "photos_saved": 0,     # Número de fotos salvas
            }
        }
        
        # Carrega configurações existentes ou cria arquivo padrão
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """
        Carrega configurações do arquivo JSON
        
        Returns:
            Dict[str, Any]: Dicionário com as configurações
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                
                # Mescla com configurações padrão para garantir que todas as chaves existam
                config = self._merge_configs(self.default_config, loaded_config)
                print(f"✅ Configurações carregadas de {self.config_file}")
                return config
            else:
                print(f"📄 Arquivo de configuração não encontrado. Criando {self.config_file} com valores padrão.")
                self.save_config(self.default_config)
                return self.default_config.copy()
                
        except Exception as e:
            print(f"❌ Erro ao carregar configurações: {e}")
            print("🔄 Usando configurações padrão.")
            return self.default_config.copy()
    
    def save_config(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Salva configurações no arquivo JSON
        
        Args:
            config (Optional[Dict[str, Any]]): Configurações para salvar. Se None, usa self.config
            
        Returns:
            bool: True se salvou com sucesso, False caso contrário
        """
        try:
            config_to_save = config if config is not None else self.config
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_to_save, f, indent=4, ensure_ascii=False)
            
            print(f"💾 Configurações salvas em {self.config_file}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar configurações: {e}")
            return False
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Obtém um valor de configuração
        
        Args:
            section (str): Seção da configuração (ex: 'game', 'audio')
            key (str): Chave da configuração
            default (Any): Valor padrão se não encontrar
            
        Returns:
            Any: Valor da configuração
        """
        try:
            return self.config.get(section, {}).get(key, default)
        except Exception:
            return default
    
    def set(self, section: str, key: str, value: Any, save: bool = True) -> bool:
        """
        Define um valor de configuração
        
        Args:
            section (str): Seção da configuração
            key (str): Chave da configuração
            value (Any): Valor para definir
            save (bool): Se deve salvar automaticamente no arquivo
            
        Returns:
            bool: True se definiu com sucesso
        """
        try:
            if section not in self.config:
                self.config[section] = {}
            
            self.config[section][key] = value
            
            if save:
                return self.save_config()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao definir configuração {section}.{key}: {e}")
            return False
    
    def get_game_settings(self) -> Dict[str, Any]:
        """
        Obtém configurações específicas do jogo no formato esperado pelo jogo
        
        Returns:
            Dict[str, Any]: Configurações do jogo
        """
        return {
            'duration': self.get('game', 'duration', 300),
            'win_threshold': self.get('game', 'win_threshold', 30.0),
            'min_body_pixels': self.get('game', 'min_body_pixels', 1000),
        }
    
    def update_game_settings(self, settings: Dict[str, Any], save: bool = True) -> bool:
        """
        Atualiza configurações do jogo
        
        Args:
            settings (Dict[str, Any]): Novas configurações
            save (bool): Se deve salvar automaticamente
            
        Returns:
            bool: True se atualizou com sucesso
        """
        try:
            for key, value in settings.items():
                self.set('game', key, value, save=False)
            
            if save:
                return self.save_config()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao atualizar configurações do jogo: {e}")
            return False
    
    def reset_to_defaults(self, section: Optional[str] = None, save: bool = True) -> bool:
        """
        Restaura configurações padrão
        
        Args:
            section (Optional[str]): Seção específica para restaurar. Se None, restaura tudo
            save (bool): Se deve salvar automaticamente
            
        Returns:
            bool: True se restaurou com sucesso
        """
        try:
            if section is None:
                self.config = self.default_config.copy()
            else:
                if section in self.default_config:
                    self.config[section] = self.default_config[section].copy()
                else:
                    return False
            
            if save:
                return self.save_config()
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao restaurar configurações padrão: {e}")
            return False
    
    def _merge_configs(self, default: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mescla configurações carregadas com padrões para garantir completude
        
        Args:
            default (Dict[str, Any]): Configurações padrão
            loaded (Dict[str, Any]): Configurações carregadas
            
        Returns:
            Dict[str, Any]: Configurações mescladas
        """
        result = default.copy()
        
        for section, values in loaded.items():
            if section in result and isinstance(values, dict):
                result[section].update(values)
            else:
                result[section] = values
        
        return result
    
    def update_stats(self, **kwargs) -> bool:
        """
        Atualiza estatísticas do jogador
        
        Args:
            **kwargs: Estatísticas para atualizar
            
        Returns:
            bool: True se atualizou com sucesso
        """
        try:
            for key, value in kwargs.items():
                if key in self.default_config['stats']:
                    current_value = self.get('stats', key, 0)
                    
                    # Para algumas estatísticas, incrementamos; para outras, substituímos
                    if key in ['games_played', 'games_won', 'photos_saved']:
                        self.set('stats', key, current_value + value, save=False)
                    elif key in ['total_playtime']:
                        self.set('stats', key, current_value + value, save=False)
                    elif key in ['best_percentage', 'best_time']:
                        # Para "melhores", só atualiza se for melhor
                        if key == 'best_percentage' and value > current_value:
                            self.set('stats', key, value, save=False)
                        elif key == 'best_time' and (current_value == 0 or value < current_value):
                            self.set('stats', key, value, save=False)
                    else:
                        self.set('stats', key, value, save=False)
            
            return self.save_config()
            
        except Exception as e:
            print(f"❌ Erro ao atualizar estatísticas: {e}")
            return False


# Instância global do gerenciador de configurações
config_manager = ConfigManager()


def get_config_manager() -> ConfigManager:
    """
    Obtém a instância global do gerenciador de configurações
    
    Returns:
        ConfigManager: Instância do gerenciador
    """
    return config_manager
