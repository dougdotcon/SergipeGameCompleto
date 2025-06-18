"""
SISTEMA DE FEEDBACK VISUAL - VIVA SERGIPE!
Melhorias na interface visual e feedback para o usuário
"""

import cv2
import numpy as np
import time
from typing import Tuple, Optional, Dict, Any
from config_manager import get_config_manager


class VisualFeedbackManager:
    """Gerenciador de feedback visual avançado"""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.last_detection_time = 0
        self.detection_status = "unknown"  # "good", "poor", "none", "unknown"
        self.calibration_data = {
            "lighting_quality": 0.0,
            "background_contrast": 0.0,
            "body_visibility": 0.0
        }
        self.feedback_messages = []
        self.message_start_time = 0
        
    def analyze_detection_quality(self, frame: np.ndarray, results, body_pixels: int) -> Dict[str, Any]:
        """
        Analisa a qualidade da detecção corporal
        
        Args:
            frame: Frame atual da câmera
            results: Resultados do MediaPipe
            body_pixels: Número de pixels do corpo detectados
            
        Returns:
            Dict com análise da qualidade
        """
        analysis = {
            "status": "unknown",
            "confidence": 0.0,
            "issues": [],
            "suggestions": []
        }
        
        # Verificar se há detecção de pose
        if results.pose_landmarks is None:
            analysis["status"] = "none"
            analysis["issues"].append("Nenhuma pose detectada")
            analysis["suggestions"].extend([
                "Posicione-se em frente à câmera",
                "Certifique-se de que todo seu corpo está visível",
                "Melhore a iluminação do ambiente"
            ])
            return analysis
        
        # Analisar qualidade da iluminação
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        contrast = np.std(gray)
        
        if brightness < 80:
            analysis["issues"].append("Iluminação muito escura")
            analysis["suggestions"].append("Aumente a iluminação do ambiente")
        elif brightness > 200:
            analysis["issues"].append("Iluminação muito clara")
            analysis["suggestions"].append("Reduza a iluminação ou evite contraluz")
        
        if contrast < 30:
            analysis["issues"].append("Baixo contraste")
            analysis["suggestions"].append("Use roupas contrastantes com o fundo")
        
        # Analisar pixels do corpo
        min_pixels = self.config_manager.get('game', 'min_body_pixels', 1000)
        
        if body_pixels < min_pixels * 0.5:
            analysis["status"] = "poor"
            analysis["issues"].append("Detecção corporal insuficiente")
            analysis["suggestions"].extend([
                "Aproxime-se da câmera",
                "Use movimentos mais amplos",
                "Verifique se não há obstruções"
            ])
        elif body_pixels < min_pixels:
            analysis["status"] = "fair"
            analysis["issues"].append("Detecção corporal limitada")
            analysis["suggestions"].append("Tente movimentos mais amplos")
        else:
            analysis["status"] = "good"
        
        # Calcular confiança geral
        confidence_factors = []
        
        # Fator de iluminação (0-1)
        if 80 <= brightness <= 200:
            confidence_factors.append(1.0)
        else:
            confidence_factors.append(max(0.0, 1.0 - abs(brightness - 140) / 140))
        
        # Fator de contraste (0-1)
        confidence_factors.append(min(1.0, contrast / 50))
        
        # Fator de detecção corporal (0-1)
        confidence_factors.append(min(1.0, body_pixels / (min_pixels * 2)))
        
        analysis["confidence"] = np.mean(confidence_factors)
        
        # Atualizar status baseado na confiança
        if analysis["confidence"] > 0.8:
            analysis["status"] = "excellent"
        elif analysis["confidence"] > 0.6:
            analysis["status"] = "good"
        elif analysis["confidence"] > 0.4:
            analysis["status"] = "fair"
        else:
            analysis["status"] = "poor"
        
        return analysis
    
    def draw_detection_feedback(self, frame: np.ndarray, analysis: Dict[str, Any]) -> np.ndarray:
        """
        Desenha feedback visual da detecção no frame
        
        Args:
            frame: Frame para desenhar
            analysis: Análise da qualidade da detecção
            
        Returns:
            Frame com feedback visual
        """
        height, width = frame.shape[:2]
        
        # Cores baseadas no status
        status_colors = {
            "excellent": (0, 255, 0),    # Verde
            "good": (0, 200, 0),         # Verde claro
            "fair": (0, 255, 255),       # Amarelo
            "poor": (0, 165, 255),       # Laranja
            "none": (0, 0, 255)          # Vermelho
        }
        
        status = analysis.get("status", "unknown")
        color = status_colors.get(status, (128, 128, 128))
        confidence = analysis.get("confidence", 0.0)
        
        # Desenhar indicador de qualidade no canto superior direito
        indicator_size = 20
        indicator_pos = (width - 150, 30)
        
        # Círculo de status
        cv2.circle(frame, indicator_pos, indicator_size, color, -1)
        cv2.circle(frame, indicator_pos, indicator_size, (255, 255, 255), 2)
        
        # Texto de status
        status_text = status.upper()
        cv2.putText(frame, status_text, (indicator_pos[0] + 30, indicator_pos[1] + 7),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        
        # Barra de confiança
        bar_width = 100
        bar_height = 10
        bar_pos = (width - 150, indicator_pos[1] + 30)
        
        # Fundo da barra
        cv2.rectangle(frame, bar_pos, (bar_pos[0] + bar_width, bar_pos[1] + bar_height),
                     (50, 50, 50), -1)
        
        # Preenchimento da barra
        fill_width = int(bar_width * confidence)
        if fill_width > 0:
            cv2.rectangle(frame, bar_pos, (bar_pos[0] + fill_width, bar_pos[1] + bar_height),
                         color, -1)
        
        # Texto de confiança
        confidence_text = f"{confidence * 100:.0f}%"
        cv2.putText(frame, confidence_text, (bar_pos[0], bar_pos[1] + bar_height + 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame
    
    def draw_calibration_guide(self, frame: np.ndarray) -> np.ndarray:
        """
        Desenha guia de calibração para posicionamento
        
        Args:
            frame: Frame para desenhar
            
        Returns:
            Frame com guia de calibração
        """
        height, width = frame.shape[:2]
        
        # Área recomendada para o corpo (retângulo central)
        margin_x = width // 6
        margin_y = height // 8
        
        guide_rect = (
            margin_x,
            margin_y,
            width - margin_x,
            height - margin_y
        )
        
        # Desenhar retângulo guia
        cv2.rectangle(frame, (guide_rect[0], guide_rect[1]), 
                     (guide_rect[2], guide_rect[3]), (0, 255, 255), 2)
        
        # Linhas de grade
        grid_lines = 3
        for i in range(1, grid_lines):
            # Linhas verticais
            x = guide_rect[0] + (guide_rect[2] - guide_rect[0]) * i // grid_lines
            cv2.line(frame, (x, guide_rect[1]), (x, guide_rect[3]), (0, 255, 255), 1)
            
            # Linhas horizontais
            y = guide_rect[1] + (guide_rect[3] - guide_rect[1]) * i // grid_lines
            cv2.line(frame, (guide_rect[0], y), (guide_rect[2], y), (0, 255, 255), 1)
        
        # Texto de instrução
        instruction = "Posicione seu corpo dentro da area amarela"
        text_size = cv2.getTextSize(instruction, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        text_x = (width - text_size[0]) // 2
        text_y = guide_rect[3] + 40
        
        cv2.putText(frame, instruction, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        return frame
    
    def draw_pose_landmarks_enhanced(self, frame: np.ndarray, results) -> np.ndarray:
        """
        Desenha landmarks da pose com feedback visual melhorado
        
        Args:
            frame: Frame para desenhar
            results: Resultados do MediaPipe
            
        Returns:
            Frame com landmarks melhorados
        """
        if results.pose_landmarks is None:
            return frame
        
        # Importar MediaPipe para desenhar
        try:
            import mediapipe as mp
            mp_drawing = mp.solutions.drawing_utils
            mp_pose = mp.solutions.pose
            
            # Estilo personalizado para landmarks
            landmark_style = mp_drawing.DrawingSpec(
                color=(0, 255, 0), thickness=3, circle_radius=3
            )
            connection_style = mp_drawing.DrawingSpec(
                color=(0, 200, 0), thickness=2
            )
            
            # Desenhar landmarks
            mp_drawing.draw_landmarks(
                frame, 
                results.pose_landmarks, 
                mp_pose.POSE_CONNECTIONS,
                landmark_style,
                connection_style
            )
            
        except ImportError:
            # Fallback se MediaPipe não estiver disponível
            pass
        
        return frame
    
    def show_temporary_message(self, message: str, duration: float = 3.0):
        """
        Mostra uma mensagem temporária na tela
        
        Args:
            message: Mensagem para mostrar
            duration: Duração em segundos
        """
        self.feedback_messages.append({
            "text": message,
            "start_time": time.time(),
            "duration": duration
        })
    
    def draw_messages(self, frame: np.ndarray) -> np.ndarray:
        """
        Desenha mensagens temporárias na tela
        
        Args:
            frame: Frame para desenhar
            
        Returns:
            Frame com mensagens
        """
        current_time = time.time()
        height, width = frame.shape[:2]
        
        # Filtrar mensagens expiradas
        self.feedback_messages = [
            msg for msg in self.feedback_messages
            if current_time - msg["start_time"] < msg["duration"]
        ]
        
        # Desenhar mensagens ativas
        y_offset = height - 100
        for i, msg in enumerate(self.feedback_messages):
            text = msg["text"]
            elapsed = current_time - msg["start_time"]
            duration = msg["duration"]
            
            # Calcular alpha baseado no tempo restante
            alpha = 1.0
            if elapsed > duration * 0.7:  # Fade out nos últimos 30%
                alpha = (duration - elapsed) / (duration * 0.3)
            
            # Desenhar fundo semi-transparente
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
            bg_rect = (
                10,
                y_offset - text_size[1] - 10,
                text_size[0] + 20,
                text_size[1] + 20
            )
            
            overlay = frame.copy()
            cv2.rectangle(overlay, (bg_rect[0], bg_rect[1]), 
                         (bg_rect[0] + bg_rect[2], bg_rect[1] + bg_rect[3]),
                         (0, 0, 0), -1)
            
            # Aplicar transparência
            cv2.addWeighted(overlay, alpha * 0.7, frame, 1 - alpha * 0.7, 0, frame)
            
            # Desenhar texto
            text_color = (255, 255, 255)
            cv2.putText(frame, text, (20, y_offset),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
            
            y_offset -= 50
        
        return frame
    
    def draw_performance_info(self, frame: np.ndarray, fps: float, 
                            fill_percentage: float, body_pixels: int) -> np.ndarray:
        """
        Desenha informações de performance no canto da tela
        
        Args:
            frame: Frame para desenhar
            fps: Frames por segundo
            fill_percentage: Percentual de preenchimento
            body_pixels: Pixels do corpo detectados
            
        Returns:
            Frame com informações de performance
        """
        if not self.config_manager.get('visual', 'show_debug_info', False):
            return frame
        
        height, width = frame.shape[:2]
        
        # Informações para mostrar
        info_lines = [
            f"FPS: {fps:.1f}",
            f"Fill: {fill_percentage:.1f}%",
            f"Body Pixels: {body_pixels}",
            f"Status: {self.detection_status}"
        ]
        
        # Desenhar fundo
        bg_height = len(info_lines) * 25 + 10
        cv2.rectangle(frame, (10, 10), (200, bg_height), (0, 0, 0), -1)
        cv2.rectangle(frame, (10, 10), (200, bg_height), (255, 255, 255), 1)
        
        # Desenhar texto
        for i, line in enumerate(info_lines):
            y = 30 + i * 25
            cv2.putText(frame, line, (15, y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        return frame


# Instância global do gerenciador de feedback visual
visual_feedback = VisualFeedbackManager()


def get_visual_feedback_manager() -> VisualFeedbackManager:
    """
    Obtém a instância global do gerenciador de feedback visual
    
    Returns:
        VisualFeedbackManager: Instância do gerenciador
    """
    return visual_feedback
