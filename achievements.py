"""
SISTEMA DE CONQUISTAS - VIVA SERGIPE!
Sistema de achievements para motivar e recompensar jogadores
"""

import time
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
from config_manager import get_config_manager


class AchievementType(Enum):
    """Tipos de conquistas"""
    MILESTONE = "milestone"      # Marcos de progresso
    PERFORMANCE = "performance"  # Performance específica
    CONSISTENCY = "consistency"  # Consistência ao longo do tempo
    EXPLORATION = "exploration"  # Explorar diferentes aspectos
    SPECIAL = "special"         # Conquistas especiais/secretas


class AchievementManager:
    """Gerenciador de conquistas"""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.achievements = self._define_achievements()
        self.unlocked_achievements = self._load_unlocked_achievements()
        
    def _define_achievements(self) -> Dict[str, Dict[str, Any]]:
        """Define todas as conquistas disponíveis"""
        return {
            # Conquistas de Marco (Milestone)
            "first_steps": {
                "name": "👶 Primeiros Passos",
                "description": "Complete seu primeiro jogo",
                "type": AchievementType.MILESTONE,
                "icon": "👶",
                "condition": {"games_played": 1},
                "reward_points": 10,
                "hidden": False
            },
            
            "getting_started": {
                "name": "🎮 Começando",
                "description": "Vença seu primeiro jogo",
                "type": AchievementType.MILESTONE,
                "icon": "🎮",
                "condition": {"games_won": 1},
                "reward_points": 25,
                "hidden": False
            },
            
            "dedicated_player": {
                "name": "🎯 Jogador Dedicado",
                "description": "Jogue 10 partidas",
                "type": AchievementType.MILESTONE,
                "icon": "🎯",
                "condition": {"games_played": 10},
                "reward_points": 50,
                "hidden": False
            },
            
            "sergipe_enthusiast": {
                "name": "🏆 Entusiasta de Sergipe",
                "description": "Vença 5 jogos",
                "type": AchievementType.MILESTONE,
                "icon": "🏆",
                "condition": {"games_won": 5},
                "reward_points": 75,
                "hidden": False
            },
            
            "sergipe_champion": {
                "name": "👑 Campeão de Sergipe",
                "description": "Vença 25 jogos",
                "type": AchievementType.MILESTONE,
                "icon": "👑",
                "condition": {"games_won": 25},
                "reward_points": 200,
                "hidden": False
            },
            
            # Conquistas de Performance
            "perfectionist": {
                "name": "🎯 Perfeccionista",
                "description": "Alcance 50% de preenchimento",
                "type": AchievementType.PERFORMANCE,
                "icon": "🎯",
                "condition": {"best_percentage": 50.0},
                "reward_points": 100,
                "hidden": False
            },
            
            "master_of_sergipe": {
                "name": "🌟 Mestre de Sergipe",
                "description": "Alcance 70% de preenchimento",
                "type": AchievementType.PERFORMANCE,
                "icon": "🌟",
                "condition": {"best_percentage": 70.0},
                "reward_points": 250,
                "hidden": False
            },
            
            "speed_demon": {
                "name": "⚡ Demônio da Velocidade",
                "description": "Vença um jogo em menos de 60 segundos",
                "type": AchievementType.PERFORMANCE,
                "icon": "⚡",
                "condition": {"best_time": 60.0, "operator": "less_than"},
                "reward_points": 150,
                "hidden": False
            },
            
            "lightning_fast": {
                "name": "🏃‍♂️ Raio",
                "description": "Vença um jogo em menos de 30 segundos",
                "type": AchievementType.PERFORMANCE,
                "icon": "🏃‍♂️",
                "condition": {"best_time": 30.0, "operator": "less_than"},
                "reward_points": 300,
                "hidden": True
            },
            
            # Conquistas de Consistência
            "consistent_player": {
                "name": "📈 Jogador Consistente",
                "description": "Mantenha uma taxa de vitória de 50%",
                "type": AchievementType.CONSISTENCY,
                "icon": "📈",
                "condition": {"win_rate": 0.5, "min_games": 10},
                "reward_points": 100,
                "hidden": False
            },
            
            "unstoppable": {
                "name": "🔥 Imparável",
                "description": "Vença 5 jogos consecutivos",
                "type": AchievementType.CONSISTENCY,
                "icon": "🔥",
                "condition": {"consecutive_wins": 5},
                "reward_points": 150,
                "hidden": False
            },
            
            "marathon_runner": {
                "name": "🏃‍♀️ Maratonista",
                "description": "Jogue por mais de 2 horas no total",
                "type": AchievementType.CONSISTENCY,
                "icon": "🏃‍♀️",
                "condition": {"total_playtime": 7200},  # 2 horas em segundos
                "reward_points": 100,
                "hidden": False
            },
            
            # Conquistas de Exploração
            "photographer": {
                "name": "📸 Fotógrafo",
                "description": "Salve 10 fotos de vitória",
                "type": AchievementType.EXPLORATION,
                "icon": "📸",
                "condition": {"photos_saved": 10},
                "reward_points": 75,
                "hidden": False
            },
            
            "customizer": {
                "name": "⚙️ Personalizador",
                "description": "Altere as configurações do jogo",
                "type": AchievementType.EXPLORATION,
                "icon": "⚙️",
                "condition": {"config_changes": 1},
                "reward_points": 25,
                "hidden": False
            },
            
            "mode_explorer": {
                "name": "🎮 Explorador de Modos",
                "description": "Jogue em 3 modos diferentes",
                "type": AchievementType.EXPLORATION,
                "icon": "🎮",
                "condition": {"modes_played": 3},
                "reward_points": 100,
                "hidden": False
            },
            
            # Conquistas Especiais
            "early_bird": {
                "name": "🌅 Madrugador",
                "description": "Jogue entre 5h e 7h da manhã",
                "type": AchievementType.SPECIAL,
                "icon": "🌅",
                "condition": {"time_range": (5, 7)},
                "reward_points": 50,
                "hidden": True
            },
            
            "night_owl": {
                "name": "🦉 Coruja",
                "description": "Jogue entre 23h e 1h da madrugada",
                "type": AchievementType.SPECIAL,
                "icon": "🦉",
                "condition": {"time_range": (23, 1)},
                "reward_points": 50,
                "hidden": True
            },
            
            "sergipe_pride": {
                "name": "💚 Orgulho Sergipano",
                "description": "Jogue no dia 8 de julho (Emancipação de Sergipe)",
                "type": AchievementType.SPECIAL,
                "icon": "💚",
                "condition": {"special_date": (7, 8)},  # 8 de julho
                "reward_points": 100,
                "hidden": True
            },
            
            "completionist": {
                "name": "🏅 Completista",
                "description": "Desbloqueie todas as outras conquistas",
                "type": AchievementType.SPECIAL,
                "icon": "🏅",
                "condition": {"all_achievements": True},
                "reward_points": 500,
                "hidden": True
            }
        }
    
    def _load_unlocked_achievements(self) -> List[str]:
        """Carrega conquistas já desbloqueadas"""
        return self.config_manager.get('achievements', 'unlocked', [])
    
    def _save_unlocked_achievements(self):
        """Salva conquistas desbloqueadas"""
        self.config_manager.set('achievements', 'unlocked', self.unlocked_achievements)
    
    def check_achievements(self, game_data: Optional[Dict[str, Any]] = None) -> List[str]:
        """
        Verifica e desbloqueia conquistas baseado no estado atual
        
        Args:
            game_data: Dados específicos do jogo atual (opcional)
            
        Returns:
            Lista de conquistas recém-desbloqueadas
        """
        newly_unlocked = []
        stats = self.config_manager.config.get('stats', {})
        
        # Adicionar dados do jogo atual se fornecidos
        if game_data:
            stats.update(game_data)
        
        for achievement_id, achievement in self.achievements.items():
            if achievement_id in self.unlocked_achievements:
                continue  # Já desbloqueada
            
            if self._check_achievement_condition(achievement, stats):
                self.unlocked_achievements.append(achievement_id)
                newly_unlocked.append(achievement_id)
                print(f"🏆 Conquista desbloqueada: {achievement['name']}")
        
        if newly_unlocked:
            self._save_unlocked_achievements()
            
            # Atualizar pontos totais
            total_points = sum(
                self.achievements[aid]['reward_points'] 
                for aid in self.unlocked_achievements
            )
            self.config_manager.set('achievements', 'total_points', total_points)
        
        return newly_unlocked
    
    def _check_achievement_condition(self, achievement: Dict[str, Any], 
                                   stats: Dict[str, Any]) -> bool:
        """
        Verifica se uma conquista foi alcançada
        
        Args:
            achievement: Dados da conquista
            stats: Estatísticas do jogador
            
        Returns:
            True se a conquista foi alcançada
        """
        condition = achievement['condition']
        
        # Conquista especial: todas as outras
        if 'all_achievements' in condition:
            other_achievements = [aid for aid in self.achievements.keys() if aid != 'completionist']
            return all(aid in self.unlocked_achievements for aid in other_achievements)
        
        # Conquistas baseadas em horário
        if 'time_range' in condition:
            current_hour = time.localtime().tm_hour
            start_hour, end_hour = condition['time_range']
            
            if start_hour <= end_hour:
                return start_hour <= current_hour <= end_hour
            else:  # Atravessa meia-noite
                return current_hour >= start_hour or current_hour <= end_hour
        
        # Conquistas baseadas em data especial
        if 'special_date' in condition:
            current_date = time.localtime()
            target_month, target_day = condition['special_date']
            return current_date.tm_mon == target_month and current_date.tm_mday == target_day
        
        # Conquistas baseadas em taxa de vitória
        if 'win_rate' in condition:
            games_played = stats.get('games_played', 0)
            games_won = stats.get('games_won', 0)
            min_games = condition.get('min_games', 1)
            
            if games_played < min_games:
                return False
            
            win_rate = games_won / games_played if games_played > 0 else 0
            return win_rate >= condition['win_rate']
        
        # Conquistas com operadores especiais
        operator = condition.get('operator', 'greater_equal')
        
        for key, target_value in condition.items():
            if key == 'operator':
                continue
            
            current_value = stats.get(key, 0)
            
            if operator == 'less_than':
                if current_value == 0 or current_value >= target_value:
                    return False
            elif operator == 'greater_equal':
                if current_value < target_value:
                    return False
            elif operator == 'equal':
                if current_value != target_value:
                    return False
        
        return True
    
    def get_achievement_progress(self) -> Dict[str, Any]:
        """
        Obtém progresso das conquistas
        
        Returns:
            Dict com progresso das conquistas
        """
        stats = self.config_manager.config.get('stats', {})
        progress = {}
        
        for achievement_id, achievement in self.achievements.items():
            is_unlocked = achievement_id in self.unlocked_achievements
            
            progress[achievement_id] = {
                'name': achievement['name'],
                'description': achievement['description'],
                'icon': achievement['icon'],
                'type': achievement['type'].value,
                'points': achievement['reward_points'],
                'unlocked': is_unlocked,
                'hidden': achievement.get('hidden', False),
                'progress_percentage': 100 if is_unlocked else self._calculate_progress(achievement, stats)
            }
        
        return progress
    
    def _calculate_progress(self, achievement: Dict[str, Any], 
                          stats: Dict[str, Any]) -> float:
        """
        Calcula progresso percentual de uma conquista
        
        Args:
            achievement: Dados da conquista
            stats: Estatísticas do jogador
            
        Returns:
            Progresso percentual (0-100)
        """
        condition = achievement['condition']
        
        # Conquistas especiais não têm progresso linear
        if any(key in condition for key in ['all_achievements', 'time_range', 'special_date']):
            return 0
        
        # Conquistas baseadas em taxa de vitória
        if 'win_rate' in condition:
            games_played = stats.get('games_played', 0)
            games_won = stats.get('games_won', 0)
            min_games = condition.get('min_games', 1)
            target_rate = condition['win_rate']
            
            if games_played < min_games:
                return (games_played / min_games) * 50  # 50% por ter jogos suficientes
            
            current_rate = games_won / games_played if games_played > 0 else 0
            return min(100, (current_rate / target_rate) * 100)
        
        # Conquistas baseadas em valores numéricos
        total_progress = 0
        condition_count = 0
        
        for key, target_value in condition.items():
            if key == 'operator':
                continue
            
            current_value = stats.get(key, 0)
            condition_count += 1
            
            if isinstance(target_value, (int, float)):
                progress = min(100, (current_value / target_value) * 100)
                total_progress += progress
        
        return total_progress / condition_count if condition_count > 0 else 0
    
    def get_unlocked_achievements(self) -> List[Dict[str, Any]]:
        """
        Obtém lista de conquistas desbloqueadas
        
        Returns:
            Lista de conquistas desbloqueadas
        """
        return [
            {
                'id': achievement_id,
                'name': self.achievements[achievement_id]['name'],
                'description': self.achievements[achievement_id]['description'],
                'icon': self.achievements[achievement_id]['icon'],
                'points': self.achievements[achievement_id]['reward_points']
            }
            for achievement_id in self.unlocked_achievements
        ]
    
    def get_total_points(self) -> int:
        """
        Obtém total de pontos de conquistas
        
        Returns:
            Total de pontos
        """
        return self.config_manager.get('achievements', 'total_points', 0)
    
    def get_achievement_summary(self) -> Dict[str, Any]:
        """
        Obtém resumo das conquistas
        
        Returns:
            Dict com resumo
        """
        total_achievements = len(self.achievements)
        unlocked_count = len(self.unlocked_achievements)
        total_points = self.get_total_points()
        max_points = sum(achievement['reward_points'] for achievement in self.achievements.values())
        
        return {
            'total_achievements': total_achievements,
            'unlocked_count': unlocked_count,
            'completion_percentage': (unlocked_count / total_achievements) * 100,
            'total_points': total_points,
            'max_points': max_points,
            'points_percentage': (total_points / max_points) * 100
        }


# Instância global do gerenciador de conquistas
achievement_manager = AchievementManager()


def get_achievement_manager() -> AchievementManager:
    """
    Obtém a instância global do gerenciador de conquistas
    
    Returns:
        AchievementManager: Instância do gerenciador
    """
    return achievement_manager
