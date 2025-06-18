"""
OTIMIZADOR DE PERFORMANCE - VIVA SERGIPE!
Sistema para otimizar performance e adaptar para diferentes hardwares
"""

import cv2
import numpy as np
import time
import psutil
import threading
from typing import Dict, Any, Tuple, Optional
from config_manager import get_config_manager


class PerformanceOptimizer:
    """Otimizador de performance adaptativo"""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.performance_data = {
            "fps_history": [],
            "cpu_usage": [],
            "memory_usage": [],
            "frame_processing_time": [],
            "detection_time": []
        }
        
        # Configurações adaptativas
        self.adaptive_settings = {
            "target_fps": 30,
            "min_fps": 15,
            "frame_skip": 1,
            "detection_frequency": 1,
            "resolution_scale": 1.0,
            "quality_level": "high"  # high, medium, low
        }
        
        # Limites de hardware
        self.hardware_limits = {
            "low_end": {"cpu_cores": 2, "ram_gb": 4},
            "mid_range": {"cpu_cores": 4, "ram_gb": 8},
            "high_end": {"cpu_cores": 8, "ram_gb": 16}
        }
        
        # Detectar hardware automaticamente
        self.detect_hardware_capabilities()
        
        # Thread de monitoramento
        self.monitoring = True
        self.monitor_thread = None
        self.start_monitoring()
    
    def detect_hardware_capabilities(self):
        """Detecta capacidades do hardware automaticamente"""
        try:
            # Informações do sistema
            cpu_count = psutil.cpu_count(logical=False)
            memory_gb = psutil.virtual_memory().total / (1024**3)
            
            print(f"🖥️ Hardware detectado:")
            print(f"  • CPU Cores: {cpu_count}")
            print(f"  • RAM: {memory_gb:.1f} GB")
            
            # Classificar hardware
            if cpu_count <= 2 and memory_gb <= 4:
                hardware_class = "low_end"
                self.adaptive_settings["quality_level"] = "low"
                self.adaptive_settings["target_fps"] = 20
                self.adaptive_settings["resolution_scale"] = 0.7
            elif cpu_count <= 4 and memory_gb <= 8:
                hardware_class = "mid_range"
                self.adaptive_settings["quality_level"] = "medium"
                self.adaptive_settings["target_fps"] = 25
                self.adaptive_settings["resolution_scale"] = 0.85
            else:
                hardware_class = "high_end"
                self.adaptive_settings["quality_level"] = "high"
                self.adaptive_settings["target_fps"] = 30
                self.adaptive_settings["resolution_scale"] = 1.0
            
            print(f"  • Classificação: {hardware_class}")
            print(f"  • Qualidade adaptativa: {self.adaptive_settings['quality_level']}")
            
            # Salvar nas configurações
            self.config_manager.set('performance', 'hardware_class', hardware_class, save=False)
            self.config_manager.set('performance', 'auto_detected', True, save=False)
            
        except Exception as e:
            print(f"⚠️ Erro ao detectar hardware: {e}")
            # Usar configurações conservadoras
            self.adaptive_settings["quality_level"] = "medium"
            self.adaptive_settings["target_fps"] = 25
    
    def optimize_frame_processing(self, frame: np.ndarray) -> np.ndarray:
        """
        Otimiza o processamento do frame baseado na performance
        
        Args:
            frame: Frame original
            
        Returns:
            Frame otimizado
        """
        # Aplicar escala de resolução se necessário
        if self.adaptive_settings["resolution_scale"] < 1.0:
            height, width = frame.shape[:2]
            new_width = int(width * self.adaptive_settings["resolution_scale"])
            new_height = int(height * self.adaptive_settings["resolution_scale"])
            frame = cv2.resize(frame, (new_width, new_height))
        
        # Aplicar filtros baseados na qualidade
        quality = self.adaptive_settings["quality_level"]
        
        if quality == "low":
            # Reduzir qualidade para melhor performance
            frame = cv2.GaussianBlur(frame, (3, 3), 0)
        elif quality == "medium":
            # Qualidade balanceada
            pass  # Sem filtros adicionais
        else:  # high
            # Manter qualidade máxima
            pass
        
        return frame
    
    def should_skip_frame(self, frame_count: int) -> bool:
        """
        Determina se deve pular o frame atual para manter FPS
        
        Args:
            frame_count: Contador de frames
            
        Returns:
            True se deve pular o frame
        """
        return frame_count % self.adaptive_settings["frame_skip"] != 0
    
    def should_skip_detection(self, frame_count: int) -> bool:
        """
        Determina se deve pular a detecção corporal neste frame
        
        Args:
            frame_count: Contador de frames
            
        Returns:
            True se deve pular a detecção
        """
        return frame_count % self.adaptive_settings["detection_frequency"] != 0
    
    def update_performance_metrics(self, fps: float, processing_time: float, 
                                 detection_time: float = 0.0):
        """
        Atualiza métricas de performance
        
        Args:
            fps: Frames por segundo atual
            processing_time: Tempo de processamento do frame
            detection_time: Tempo de detecção corporal
        """
        # Manter histórico limitado
        max_history = 100
        
        self.performance_data["fps_history"].append(fps)
        self.performance_data["frame_processing_time"].append(processing_time)
        self.performance_data["detection_time"].append(detection_time)
        
        # Limitar tamanho do histórico
        for key in ["fps_history", "frame_processing_time", "detection_time"]:
            if len(self.performance_data[key]) > max_history:
                self.performance_data[key] = self.performance_data[key][-max_history:]
        
        # Adaptar configurações baseado na performance
        self.adapt_settings_based_on_performance()
    
    def adapt_settings_based_on_performance(self):
        """Adapta configurações baseado na performance atual"""
        if len(self.performance_data["fps_history"]) < 10:
            return  # Não há dados suficientes
        
        # Calcular FPS médio recente
        recent_fps = np.mean(self.performance_data["fps_history"][-10:])
        target_fps = self.adaptive_settings["target_fps"]
        min_fps = self.adaptive_settings["min_fps"]
        
        # Se FPS está muito baixo, reduzir qualidade
        if recent_fps < min_fps:
            if self.adaptive_settings["frame_skip"] < 3:
                self.adaptive_settings["frame_skip"] += 1
                print(f"⚡ Performance baixa detectada. Frame skip: {self.adaptive_settings['frame_skip']}")
            
            if self.adaptive_settings["detection_frequency"] < 3:
                self.adaptive_settings["detection_frequency"] += 1
                print(f"⚡ Reduzindo frequência de detecção: {self.adaptive_settings['detection_frequency']}")
            
            if self.adaptive_settings["resolution_scale"] > 0.5:
                self.adaptive_settings["resolution_scale"] -= 0.1
                print(f"⚡ Reduzindo resolução: {self.adaptive_settings['resolution_scale']:.1f}")
        
        # Se FPS está bom, pode melhorar qualidade
        elif recent_fps > target_fps * 1.2:
            if self.adaptive_settings["frame_skip"] > 1:
                self.adaptive_settings["frame_skip"] = max(1, self.adaptive_settings["frame_skip"] - 1)
                print(f"⚡ Performance boa. Frame skip: {self.adaptive_settings['frame_skip']}")
            
            if self.adaptive_settings["detection_frequency"] > 1:
                self.adaptive_settings["detection_frequency"] = max(1, self.adaptive_settings["detection_frequency"] - 1)
                print(f"⚡ Aumentando frequência de detecção: {self.adaptive_settings['detection_frequency']}")
            
            if self.adaptive_settings["resolution_scale"] < 1.0:
                self.adaptive_settings["resolution_scale"] = min(1.0, self.adaptive_settings["resolution_scale"] + 0.1)
                print(f"⚡ Aumentando resolução: {self.adaptive_settings['resolution_scale']:.1f}")
    
    def get_optimized_camera_settings(self) -> Dict[str, Any]:
        """
        Obtém configurações otimizadas da câmera
        
        Returns:
            Dict com configurações da câmera
        """
        quality = self.adaptive_settings["quality_level"]
        
        if quality == "low":
            return {
                "width": 640,
                "height": 480,
                "fps": 20,
                "buffer_size": 1
            }
        elif quality == "medium":
            return {
                "width": 1280,
                "height": 720,
                "fps": 25,
                "buffer_size": 2
            }
        else:  # high
            return {
                "width": 1920,
                "height": 1080,
                "fps": 30,
                "buffer_size": 3
            }
    
    def start_monitoring(self):
        """Inicia monitoramento de sistema em background"""
        if self.monitor_thread and self.monitor_thread.is_alive():
            return
        
        self.monitor_thread = threading.Thread(
            target=self._monitor_system,
            daemon=True,
            name="PerformanceMonitor"
        )
        self.monitor_thread.start()
    
    def _monitor_system(self):
        """Loop de monitoramento do sistema"""
        while self.monitoring:
            try:
                # Coletar métricas do sistema
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_percent = psutil.virtual_memory().percent
                
                self.performance_data["cpu_usage"].append(cpu_percent)
                self.performance_data["memory_usage"].append(memory_percent)
                
                # Limitar histórico
                max_history = 60  # 1 minuto de dados
                for key in ["cpu_usage", "memory_usage"]:
                    if len(self.performance_data[key]) > max_history:
                        self.performance_data[key] = self.performance_data[key][-max_history:]
                
                # Verificar se sistema está sobrecarregado
                if cpu_percent > 90 or memory_percent > 90:
                    print(f"⚠️ Sistema sobrecarregado - CPU: {cpu_percent:.1f}%, RAM: {memory_percent:.1f}%")
                    # Forçar configurações mais conservadoras
                    self.adaptive_settings["frame_skip"] = max(2, self.adaptive_settings["frame_skip"])
                    self.adaptive_settings["detection_frequency"] = max(2, self.adaptive_settings["detection_frequency"])
                
                time.sleep(1)
                
            except Exception as e:
                print(f"Erro no monitoramento: {e}")
                time.sleep(5)
    
    def get_performance_report(self) -> Dict[str, Any]:
        """
        Gera relatório de performance
        
        Returns:
            Dict com relatório de performance
        """
        report = {
            "hardware": {
                "cpu_cores": psutil.cpu_count(logical=False),
                "ram_gb": psutil.virtual_memory().total / (1024**3),
                "class": self.config_manager.get('performance', 'hardware_class', 'unknown')
            },
            "current_settings": self.adaptive_settings.copy(),
            "performance": {}
        }
        
        # Calcular estatísticas de performance
        if self.performance_data["fps_history"]:
            report["performance"]["avg_fps"] = np.mean(self.performance_data["fps_history"])
            report["performance"]["min_fps"] = np.min(self.performance_data["fps_history"])
            report["performance"]["max_fps"] = np.max(self.performance_data["fps_history"])
        
        if self.performance_data["cpu_usage"]:
            report["performance"]["avg_cpu"] = np.mean(self.performance_data["cpu_usage"])
            report["performance"]["max_cpu"] = np.max(self.performance_data["cpu_usage"])
        
        if self.performance_data["memory_usage"]:
            report["performance"]["avg_memory"] = np.mean(self.performance_data["memory_usage"])
            report["performance"]["max_memory"] = np.max(self.performance_data["memory_usage"])
        
        return report
    
    def stop_monitoring(self):
        """Para o monitoramento"""
        self.monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2)
    
    def reset_adaptive_settings(self):
        """Reseta configurações adaptativas para padrões"""
        self.detect_hardware_capabilities()
        print("🔄 Configurações adaptativas resetadas")


# Instância global do otimizador
performance_optimizer = PerformanceOptimizer()


def get_performance_optimizer() -> PerformanceOptimizer:
    """
    Obtém a instância global do otimizador de performance
    
    Returns:
        PerformanceOptimizer: Instância do otimizador
    """
    return performance_optimizer
