"""
MODOS DE JOGO - VIVA SERGIPE!
Sistema de diferentes modos de jogo para variar a experiência
"""

import time
import random
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from config_manager import get_config_manager


class GameMode(Enum):
    """Tipos de modos de jogo"""
    CLASSIC = "classic"
    RELAXED = "relaxed"
    SPEEDRUN = "speedrun"
    PRECISION = "precision"
    CHALLENGE = "challenge"
    TRAINING = "training"


class GameModeManager:
    """Gerenciador de modos de jogo"""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.current_mode = GameMode.CLASSIC
        self.mode_data = {}
        self.challenge_progress = {}
        
        # Definir configurações de cada modo
        self.mode_configs = {
            GameMode.CLASSIC: {
                "name": "🎮 Clássico",
                "description": "Modo padrão do jogo com configurações balanceadas",
                "duration": 300,  # 5 minutos
                "win_threshold": 30.0,
                "min_body_pixels": 1000,
                "has_timer": True,
                "difficulty": "normal",
                "unlock_condition": None  # Sempre disponível
            },
            
            GameMode.RELAXED: {
                "name": "😌 Relaxado",
                "description": "Sem pressão de tempo, foque apenas em se divertir",
                "duration": 0,  # Sem limite de tempo
                "win_threshold": 25.0,
                "min_body_pixels": 800,
                "has_timer": False,
                "difficulty": "easy",
                "unlock_condition": None  # Sempre disponível
            },
            
            GameMode.SPEEDRUN: {
                "name": "⚡ Speedrun",
                "description": "Alcance a meta o mais rápido possível!",
                "duration": 120,  # 2 minutos
                "win_threshold": 35.0,
                "min_body_pixels": 1200,
                "has_timer": True,
                "difficulty": "hard",
                "unlock_condition": {"games_won": 5}
            },
            
            GameMode.PRECISION: {
                "name": "🎯 Precisão",
                "description": "Meta alta para jogadores experientes",
                "duration": 360,  # 6 minutos
                "win_threshold": 50.0,
                "min_body_pixels": 1500,
                "has_timer": True,
                "difficulty": "expert",
                "unlock_condition": {"games_won": 10, "best_percentage": 40.0}
            },
            
            GameMode.CHALLENGE: {
                "name": "🏆 Desafio",
                "description": "Desafios especiais com objetivos únicos",
                "duration": 240,  # 4 minutos
                "win_threshold": 40.0,
                "min_body_pixels": 1300,
                "has_timer": True,
                "difficulty": "variable",
                "unlock_condition": {"games_won": 3}
            },
            
            GameMode.TRAINING: {
                "name": "📚 Treinamento",
                "description": "Aprenda com feedback detalhado e dicas",
                "duration": 600,  # 10 minutos
                "win_threshold": 20.0,
                "min_body_pixels": 600,
                "has_timer": True,
                "difficulty": "tutorial",
                "unlock_condition": None  # Sempre disponível
            }
        }
        
        # Desafios especiais para o modo Challenge
        self.challenges = [
            {
                "id": "speed_demon",
                "name": "Demônio da Velocidade",
                "description": "Alcance 30% em menos de 60 segundos",
                "target_percentage": 30.0,
                "time_limit": 60,
                "reward": "🏃‍♂️ Velocista"
            },
            {
                "id": "perfectionist",
                "name": "Perfeccionista",
                "description": "Alcance exatamente 50% de preenchimento",
                "target_percentage": 50.0,
                "tolerance": 1.0,
                "reward": "🎯 Precisão Perfeita"
            },
            {
                "id": "endurance",
                "name": "Resistência",
                "description": "Mantenha 25% por 3 minutos consecutivos",
                "maintain_percentage": 25.0,
                "maintain_duration": 180,
                "reward": "💪 Resistente"
            },
            {
                "id": "sergipe_master",
                "name": "Mestre de Sergipe",
                "description": "Preencha 80% do mapa pelo menos uma vez",
                "target_percentage": 80.0,
                "reward": "👑 Mestre de Sergipe"
            }
        ]
    
    def get_available_modes(self) -> List[Dict[str, Any]]:
        """
        Obtém lista de modos disponíveis baseado no progresso do jogador
        
        Returns:
            Lista de modos disponíveis
        """
        available_modes = []
        stats = self.config_manager.config.get('stats', {})
        
        for mode, config in self.mode_configs.items():
            mode_info = config.copy()
            mode_info['mode'] = mode
            mode_info['unlocked'] = self.is_mode_unlocked(mode, stats)
            
            available_modes.append(mode_info)
        
        return available_modes
    
    def is_mode_unlocked(self, mode: GameMode, stats: Dict[str, Any]) -> bool:
        """
        Verifica se um modo está desbloqueado
        
        Args:
            mode: Modo de jogo
            stats: Estatísticas do jogador
            
        Returns:
            True se o modo está desbloqueado
        """
        unlock_condition = self.mode_configs[mode]["unlock_condition"]
        
        if unlock_condition is None:
            return True  # Sempre disponível
        
        for requirement, value in unlock_condition.items():
            if stats.get(requirement, 0) < value:
                return False
        
        return True
    
    def set_current_mode(self, mode: GameMode) -> bool:
        """
        Define o modo de jogo atual
        
        Args:
            mode: Modo de jogo para ativar
            
        Returns:
            True se o modo foi ativado com sucesso
        """
        stats = self.config_manager.config.get('stats', {})
        
        if not self.is_mode_unlocked(mode, stats):
            print(f"❌ Modo {mode.value} não está desbloqueado")
            return False
        
        self.current_mode = mode
        print(f"✅ Modo ativado: {self.mode_configs[mode]['name']}")
        
        # Salvar modo atual nas configurações
        self.config_manager.set('game', 'current_mode', mode.value)
        
        return True
    
    def get_current_mode_config(self) -> Dict[str, Any]:
        """
        Obtém configuração do modo atual
        
        Returns:
            Dict com configuração do modo
        """
        return self.mode_configs[self.current_mode].copy()
    
    def get_game_settings_for_mode(self, mode: Optional[GameMode] = None) -> Dict[str, Any]:
        """
        Obtém configurações de jogo para um modo específico
        
        Args:
            mode: Modo de jogo (usa atual se None)
            
        Returns:
            Dict com configurações do jogo
        """
        if mode is None:
            mode = self.current_mode
        
        config = self.mode_configs[mode]
        
        return {
            'duration': config['duration'],
            'win_threshold': config['win_threshold'],
            'min_body_pixels': config['min_body_pixels'],
            'has_timer': config['has_timer'],
            'mode_name': config['name'],
            'mode_description': config['description']
        }
    
    def get_random_challenge(self) -> Dict[str, Any]:
        """
        Obtém um desafio aleatório para o modo Challenge
        
        Returns:
            Dict com dados do desafio
        """
        return random.choice(self.challenges).copy()
    
    def check_challenge_completion(self, challenge: Dict[str, Any], 
                                 current_percentage: float, 
                                 elapsed_time: float,
                                 time_at_percentage: Dict[float, float]) -> bool:
        """
        Verifica se um desafio foi completado
        
        Args:
            challenge: Dados do desafio
            current_percentage: Percentual atual
            elapsed_time: Tempo decorrido
            time_at_percentage: Histórico de tempo em cada percentual
            
        Returns:
            True se o desafio foi completado
        """
        challenge_id = challenge["id"]
        
        if challenge_id == "speed_demon":
            return (current_percentage >= challenge["target_percentage"] and 
                   elapsed_time <= challenge["time_limit"])
        
        elif challenge_id == "perfectionist":
            tolerance = challenge.get("tolerance", 0.5)
            target = challenge["target_percentage"]
            return abs(current_percentage - target) <= tolerance
        
        elif challenge_id == "endurance":
            maintain_percentage = challenge["maintain_percentage"]
            maintain_duration = challenge["maintain_duration"]
            
            # Verificar se manteve a porcentagem pelo tempo necessário
            time_above_threshold = 0
            for percentage, time_spent in time_at_percentage.items():
                if percentage >= maintain_percentage:
                    time_above_threshold += time_spent
            
            return time_above_threshold >= maintain_duration
        
        elif challenge_id == "sergipe_master":
            return current_percentage >= challenge["target_percentage"]
        
        return False
    
    def get_mode_tips(self, mode: Optional[GameMode] = None) -> List[str]:
        """
        Obtém dicas específicas para um modo
        
        Args:
            mode: Modo de jogo (usa atual se None)
            
        Returns:
            Lista de dicas
        """
        if mode is None:
            mode = self.current_mode
        
        tips = {
            GameMode.CLASSIC: [
                "Use movimentos amplos para cobrir mais área",
                "Mantenha-se dentro do campo de visão da câmera",
                "Seja criativo com suas poses!"
            ],
            
            GameMode.RELAXED: [
                "Não há pressa! Divirta-se explorando diferentes poses",
                "Experimente movimentos lentos e controlados",
                "Use este modo para praticar novas técnicas"
            ],
            
            GameMode.SPEEDRUN: [
                "Planeje seus movimentos com antecedência",
                "Use poses que cobrem múltiplas áreas rapidamente",
                "Mantenha-se próximo ao centro para transições rápidas"
            ],
            
            GameMode.PRECISION: [
                "Foque na qualidade, não na velocidade",
                "Use movimentos precisos e controlados",
                "Observe o feedback visual para otimizar sua posição"
            ],
            
            GameMode.CHALLENGE: [
                "Leia o objetivo do desafio cuidadosamente",
                "Adapte sua estratégia ao desafio específico",
                "Pratique em outros modos antes de tentar desafios difíceis"
            ],
            
            GameMode.TRAINING: [
                "Preste atenção ao feedback detalhado",
                "Experimente diferentes poses e observe os resultados",
                "Use este modo para melhorar sua técnica"
            ]
        }
        
        return tips.get(mode, [])
    
    def update_mode_statistics(self, mode: GameMode, game_result: Dict[str, Any]):
        """
        Atualiza estatísticas específicas do modo
        
        Args:
            mode: Modo de jogo
            game_result: Resultado do jogo
        """
        mode_stats_key = f'mode_stats_{mode.value}'
        current_stats = self.config_manager.get('stats', mode_stats_key, {
            'games_played': 0,
            'games_won': 0,
            'best_percentage': 0.0,
            'best_time': 0.0,
            'total_time': 0.0
        })
        
        # Atualizar estatísticas
        current_stats['games_played'] += 1
        current_stats['total_time'] += game_result.get('game_time', 0)
        
        if game_result.get('won', False):
            current_stats['games_won'] += 1
            
            if game_result.get('completion_time', 0) > 0:
                if (current_stats['best_time'] == 0 or 
                    game_result['completion_time'] < current_stats['best_time']):
                    current_stats['best_time'] = game_result['completion_time']
        
        if game_result.get('best_percentage', 0) > current_stats['best_percentage']:
            current_stats['best_percentage'] = game_result['best_percentage']
        
        # Salvar estatísticas
        self.config_manager.set('stats', mode_stats_key, current_stats)
    
    def get_mode_statistics(self, mode: GameMode) -> Dict[str, Any]:
        """
        Obtém estatísticas de um modo específico
        
        Args:
            mode: Modo de jogo
            
        Returns:
            Dict com estatísticas do modo
        """
        mode_stats_key = f'mode_stats_{mode.value}'
        return self.config_manager.get('stats', mode_stats_key, {
            'games_played': 0,
            'games_won': 0,
            'best_percentage': 0.0,
            'best_time': 0.0,
            'total_time': 0.0
        })
    
    def get_unlock_progress(self) -> Dict[str, Any]:
        """
        Obtém progresso para desbloquear modos
        
        Returns:
            Dict com progresso de desbloqueio
        """
        stats = self.config_manager.config.get('stats', {})
        progress = {}
        
        for mode, config in self.mode_configs.items():
            unlock_condition = config["unlock_condition"]
            
            if unlock_condition is None:
                progress[mode.value] = {"unlocked": True, "progress": {}}
            else:
                mode_progress = {}
                unlocked = True
                
                for requirement, target_value in unlock_condition.items():
                    current_value = stats.get(requirement, 0)
                    mode_progress[requirement] = {
                        "current": current_value,
                        "target": target_value,
                        "percentage": min(100, (current_value / target_value) * 100)
                    }
                    
                    if current_value < target_value:
                        unlocked = False
                
                progress[mode.value] = {
                    "unlocked": unlocked,
                    "progress": mode_progress
                }
        
        return progress


# Instância global do gerenciador de modos
game_mode_manager = GameModeManager()


def get_game_mode_manager() -> GameModeManager:
    """
    Obtém a instância global do gerenciador de modos
    
    Returns:
        GameModeManager: Instância do gerenciador
    """
    return game_mode_manager
