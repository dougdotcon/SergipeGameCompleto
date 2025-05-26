"""
SISTEMA DE ANALYTICS - VIVA SERGIPE!
Sistema opcional de coleta de dados anônimos para melhorar o jogo
"""

import json
import time
import hashlib
import platform
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
import threading
from config_manager import get_config_manager


class AnalyticsManager:
    """Gerenciador de analytics respeitando privacidade"""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.analytics_file = Path("analytics_data.json")
        self.session_id = str(uuid.uuid4())[:8]
        self.session_start = time.time()
        self.events = []
        self.enabled = self._check_analytics_consent()
        
        # Dados anônimos do sistema (apenas para otimização)
        self.system_info = self._get_anonymous_system_info()
        
    def _check_analytics_consent(self) -> bool:
        """Verifica se o usuário consentiu com analytics"""
        consent = self.config_manager.get('privacy', 'analytics_consent', None)
        
        if consent is None:
            # Primeira execução - perguntar consentimento
            self._show_privacy_notice()
            return False
        
        return consent
    
    def _show_privacy_notice(self):
        """Mostra aviso de privacidade na primeira execução"""
        print("\n" + "="*60)
        print("🔒 AVISO DE PRIVACIDADE - VIVA SERGIPE!")
        print("="*60)
        print("Para melhorar o jogo, gostaríamos de coletar dados ANÔNIMOS:")
        print("• Estatísticas de gameplay (sem dados pessoais)")
        print("• Informações de performance do sistema")
        print("• Dados de uso de funcionalidades")
        print("\nNÃO coletamos:")
        print("• Informações pessoais")
        print("• Fotos ou vídeos")
        print("• Dados de localização")
        print("• Informações identificáveis")
        print("\nVocê pode alterar esta configuração a qualquer momento.")
        print("="*60)
        
        # Por padrão, analytics desabilitado (opt-in)
        self.config_manager.set('privacy', 'analytics_consent', False)
        self.config_manager.set('privacy', 'privacy_notice_shown', True)
    
    def _get_anonymous_system_info(self) -> Dict[str, Any]:
        """Obtém informações anônimas do sistema"""
        try:
            # Hash do nome do usuário para anonimização
            user_hash = hashlib.sha256(
                platform.node().encode('utf-8')
            ).hexdigest()[:8]
            
            return {
                'user_id': user_hash,  # ID anônimo
                'os': platform.system(),
                'os_version': platform.release(),
                'python_version': platform.python_version(),
                'architecture': platform.architecture()[0],
                'processor': platform.processor()[:20] if platform.processor() else 'unknown'
            }
        except:
            return {'user_id': 'anonymous', 'os': 'unknown'}
    
    def track_event(self, event_type: str, properties: Optional[Dict[str, Any]] = None):
        """
        Registra um evento de analytics
        
        Args:
            event_type: Tipo do evento (ex: 'game_start', 'achievement_unlocked')
            properties: Propriedades adicionais do evento
        """
        if not self.enabled:
            return
        
        event = {
            'event_type': event_type,
            'timestamp': time.time(),
            'session_id': self.session_id,
            'properties': properties or {}
        }
        
        self.events.append(event)
        
        # Salvar eventos periodicamente
        if len(self.events) >= 10:
            self._save_events()
    
    def track_game_session(self, mode: str, duration: float, result: Dict[str, Any]):
        """
        Registra dados de uma sessão de jogo
        
        Args:
            mode: Modo de jogo
            duration: Duração da sessão
            result: Resultado do jogo
        """
        if not self.enabled:
            return
        
        # Dados anônimos da sessão
        session_data = {
            'mode': mode,
            'duration': round(duration, 2),
            'won': result.get('won', False),
            'percentage': round(result.get('best_percentage', 0), 1),
            'completion_time': round(result.get('completion_time', 0), 2)
        }
        
        self.track_event('game_session', session_data)
    
    def track_performance_metrics(self, metrics: Dict[str, Any]):
        """
        Registra métricas de performance
        
        Args:
            metrics: Métricas de performance
        """
        if not self.enabled:
            return
        
        # Apenas métricas agregadas, sem dados específicos
        performance_data = {
            'avg_fps': round(metrics.get('avg_fps', 0), 1),
            'hardware_class': metrics.get('hardware_class', 'unknown'),
            'quality_level': metrics.get('quality_level', 'unknown'),
            'frame_drops': metrics.get('frame_drops', 0)
        }
        
        self.track_event('performance_metrics', performance_data)
    
    def track_feature_usage(self, feature: str, action: str):
        """
        Registra uso de funcionalidades
        
        Args:
            feature: Nome da funcionalidade
            action: Ação realizada
        """
        if not self.enabled:
            return
        
        usage_data = {
            'feature': feature,
            'action': action
        }
        
        self.track_event('feature_usage', usage_data)
    
    def track_achievement(self, achievement_id: str, points: int):
        """
        Registra conquista desbloqueada
        
        Args:
            achievement_id: ID da conquista
            points: Pontos da conquista
        """
        if not self.enabled:
            return
        
        achievement_data = {
            'achievement_id': achievement_id,
            'points': points
        }
        
        self.track_event('achievement_unlocked', achievement_data)
    
    def track_error(self, error_type: str, error_context: str):
        """
        Registra erro para debugging
        
        Args:
            error_type: Tipo do erro
            error_context: Contexto onde ocorreu
        """
        if not self.enabled:
            return
        
        # Apenas informações técnicas, sem dados pessoais
        error_data = {
            'error_type': error_type,
            'context': error_context,
            'system_info': self.system_info['os']
        }
        
        self.track_event('error_occurred', error_data)
    
    def _save_events(self):
        """Salva eventos no arquivo local"""
        try:
            # Carregar eventos existentes
            existing_events = []
            if self.analytics_file.exists():
                with open(self.analytics_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    existing_events = data.get('events', [])
            
            # Adicionar novos eventos
            existing_events.extend(self.events)
            
            # Manter apenas os últimos 1000 eventos
            if len(existing_events) > 1000:
                existing_events = existing_events[-1000:]
            
            # Salvar dados
            analytics_data = {
                'system_info': self.system_info,
                'last_updated': time.time(),
                'events': existing_events
            }
            
            with open(self.analytics_file, 'w', encoding='utf-8') as f:
                json.dump(analytics_data, f, indent=2)
            
            # Limpar eventos da memória
            self.events = []
            
        except Exception as e:
            print(f"Erro ao salvar analytics: {e}")
    
    def get_local_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas locais para o usuário
        
        Returns:
            Dict com estatísticas locais
        """
        try:
            if not self.analytics_file.exists():
                return {}
            
            with open(self.analytics_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                events = data.get('events', [])
            
            # Calcular estatísticas
            game_sessions = [e for e in events if e['event_type'] == 'game_session']
            achievements = [e for e in events if e['event_type'] == 'achievement_unlocked']
            
            stats = {
                'total_sessions': len(game_sessions),
                'total_playtime': sum(s['properties'].get('duration', 0) for s in game_sessions),
                'win_rate': 0,
                'avg_percentage': 0,
                'achievements_unlocked': len(achievements),
                'total_points': sum(a['properties'].get('points', 0) for a in achievements)
            }
            
            if game_sessions:
                won_sessions = [s for s in game_sessions if s['properties'].get('won', False)]
                stats['win_rate'] = len(won_sessions) / len(game_sessions) * 100
                stats['avg_percentage'] = sum(s['properties'].get('percentage', 0) for s in game_sessions) / len(game_sessions)
            
            return stats
            
        except Exception as e:
            print(f"Erro ao calcular estatísticas: {e}")
            return {}
    
    def export_data(self, export_path: Path) -> bool:
        """
        Exporta dados do usuário (GDPR compliance)
        
        Args:
            export_path: Caminho para exportar
            
        Returns:
            True se exportou com sucesso
        """
        try:
            if not self.analytics_file.exists():
                return False
            
            with open(self.analytics_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Adicionar informações de exportação
            export_data = {
                'export_date': time.strftime('%Y-%m-%d %H:%M:%S'),
                'data_type': 'VIVA_SERGIPE_Analytics',
                'user_consent': self.enabled,
                'data': data
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Erro ao exportar dados: {e}")
            return False
    
    def delete_all_data(self) -> bool:
        """
        Deleta todos os dados de analytics (GDPR compliance)
        
        Returns:
            True se deletou com sucesso
        """
        try:
            if self.analytics_file.exists():
                self.analytics_file.unlink()
            
            # Limpar eventos da memória
            self.events = []
            
            # Desabilitar analytics
            self.enabled = False
            self.config_manager.set('privacy', 'analytics_consent', False)
            
            print("✅ Todos os dados de analytics foram removidos")
            return True
            
        except Exception as e:
            print(f"Erro ao deletar dados: {e}")
            return False
    
    def enable_analytics(self):
        """Habilita analytics com consentimento do usuário"""
        self.enabled = True
        self.config_manager.set('privacy', 'analytics_consent', True)
        print("✅ Analytics habilitado")
    
    def disable_analytics(self):
        """Desabilita analytics"""
        self.enabled = False
        self.config_manager.set('privacy', 'analytics_consent', False)
        print("🔒 Analytics desabilitado")
    
    def finalize_session(self):
        """Finaliza sessão e salva dados pendentes"""
        if self.events:
            self._save_events()
        
        # Registrar duração da sessão
        session_duration = time.time() - self.session_start
        self.track_event('session_end', {'duration': round(session_duration, 2)})
        
        # Salvar eventos finais
        if self.events:
            self._save_events()


# Instância global do gerenciador de analytics
analytics_manager = AnalyticsManager()


def get_analytics_manager() -> AnalyticsManager:
    """
    Obtém a instância global do gerenciador de analytics
    
    Returns:
        AnalyticsManager: Instância do gerenciador
    """
    return analytics_manager


def track_game_start(mode: str):
    """Registra início de jogo"""
    analytics_manager.track_event('game_start', {'mode': mode})


def track_game_end(mode: str, duration: float, result: Dict[str, Any]):
    """Registra fim de jogo"""
    analytics_manager.track_game_session(mode, duration, result)


def track_menu_action(action: str):
    """Registra ação no menu"""
    analytics_manager.track_feature_usage('menu', action)


def track_config_change(setting: str):
    """Registra mudança de configuração"""
    analytics_manager.track_feature_usage('config', f'changed_{setting}')


# Cleanup automático na saída
import atexit
atexit.register(analytics_manager.finalize_session)
