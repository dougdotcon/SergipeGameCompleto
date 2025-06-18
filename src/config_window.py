"""
JANELA DE CONFIGURAÇÕES - VIVA SERGIPE!
Interface PyQt5 para configurar o jogo
"""

import sys
import os
from PyQt5.QtWidgets import (QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QSlider, QSpinBox, QCheckBox,
                             QGroupBox, QGridLayout, QTabWidget, QWidget,
                             QMessageBox, QComboBox, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush
from config_manager import get_config_manager


class ConfigWindow(QDialog):
    """Janela de configurações do jogo"""
    
    settings_changed = pyqtSignal()  # Sinal emitido quando configurações mudam
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config_manager = get_config_manager()
        self.init_ui()
        self.load_current_settings()
    
    def init_ui(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle("⚙️ Configurações - Viva Sergipe!")
        self.setFixedSize(800, 600)
        self.setModal(True)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Título
        title_label = QLabel("⚙️ CONFIGURAÇÕES")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #00aa00;
                font-size: 28px;
                font-weight: bold;
                font-family: 'Arial Black', Arial, sans-serif;
                margin-bottom: 20px;
            }
        """)
        main_layout.addWidget(title_label)
        
        # Abas de configuração
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #cccccc;
                background-color: #f0f0f0;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 10px 20px;
                margin-right: 2px;
                border: 1px solid #cccccc;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #00aa00;
                color: white;
                font-weight: bold;
            }
        """)
        
        # Criar abas
        self.create_game_tab()
        self.create_audio_tab()
        self.create_visual_tab()
        self.create_stats_tab()
        
        main_layout.addWidget(self.tab_widget)
        
        # Botões de ação
        self.create_action_buttons(main_layout)
    
    def create_game_tab(self):
        """Cria a aba de configurações do jogo"""
        game_tab = QWidget()
        layout = QVBoxLayout(game_tab)
        layout.setSpacing(20)
        
        # Grupo: Configurações de Jogo
        game_group = QGroupBox("🎮 Configurações de Jogo")
        game_layout = QGridLayout(game_group)
        
        # Duração do jogo
        game_layout.addWidget(QLabel("Duração do Jogo:"), 0, 0)
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setRange(60, 600)  # 1 a 10 minutos
        self.duration_spinbox.setSuffix(" segundos")
        self.duration_spinbox.setSingleStep(30)
        game_layout.addWidget(self.duration_spinbox, 0, 1)
        
        # Meta de preenchimento
        game_layout.addWidget(QLabel("Meta de Preenchimento:"), 1, 0)
        self.threshold_spinbox = QSpinBox()
        self.threshold_spinbox.setRange(10, 100)
        self.threshold_spinbox.setSuffix("%")
        self.threshold_spinbox.setSingleStep(5)
        game_layout.addWidget(self.threshold_spinbox, 1, 1)
        
        # Sensibilidade corporal
        game_layout.addWidget(QLabel("Sensibilidade Corporal:"), 2, 0)
        self.sensitivity_spinbox = QSpinBox()
        self.sensitivity_spinbox.setRange(500, 5000)
        self.sensitivity_spinbox.setSuffix(" pixels")
        self.sensitivity_spinbox.setSingleStep(250)
        game_layout.addWidget(self.sensitivity_spinbox, 2, 1)
        
        # Tela cheia
        self.fullscreen_checkbox = QCheckBox("Iniciar em Tela Cheia")
        game_layout.addWidget(self.fullscreen_checkbox, 3, 0, 1, 2)
        
        # Salvar fotos automaticamente
        self.auto_save_checkbox = QCheckBox("Salvar Fotos de Vitória Automaticamente")
        game_layout.addWidget(self.auto_save_checkbox, 4, 0, 1, 2)
        
        layout.addWidget(game_group)
        layout.addStretch()
        
        self.tab_widget.addTab(game_tab, "🎮 Jogo")
    
    def create_audio_tab(self):
        """Cria a aba de configurações de áudio"""
        audio_tab = QWidget()
        layout = QVBoxLayout(audio_tab)
        layout.setSpacing(20)
        
        # Grupo: Volume
        volume_group = QGroupBox("🔊 Controles de Volume")
        volume_layout = QGridLayout(volume_group)
        
        # Volume geral
        volume_layout.addWidget(QLabel("Volume Geral:"), 0, 0)
        self.master_volume_slider = QSlider(Qt.Horizontal)
        self.master_volume_slider.setRange(0, 100)
        self.master_volume_label = QLabel("70%")
        volume_layout.addWidget(self.master_volume_slider, 0, 1)
        volume_layout.addWidget(self.master_volume_label, 0, 2)
        
        # Volume da música
        volume_layout.addWidget(QLabel("Música de Fundo:"), 1, 0)
        self.music_volume_slider = QSlider(Qt.Horizontal)
        self.music_volume_slider.setRange(0, 100)
        self.music_volume_label = QLabel("50%")
        volume_layout.addWidget(self.music_volume_slider, 1, 1)
        volume_layout.addWidget(self.music_volume_label, 1, 2)
        
        # Volume dos efeitos
        volume_layout.addWidget(QLabel("Efeitos Sonoros:"), 2, 0)
        self.effects_volume_slider = QSlider(Qt.Horizontal)
        self.effects_volume_slider.setRange(0, 100)
        self.effects_volume_label = QLabel("80%")
        volume_layout.addWidget(self.effects_volume_slider, 2, 1)
        volume_layout.addWidget(self.effects_volume_label, 2, 2)
        
        # Volume da voz
        volume_layout.addWidget(QLabel("Comandos de Voz:"), 3, 0)
        self.voice_volume_slider = QSlider(Qt.Horizontal)
        self.voice_volume_slider.setRange(0, 100)
        self.voice_volume_label = QLabel("90%")
        volume_layout.addWidget(self.voice_volume_slider, 3, 1)
        volume_layout.addWidget(self.voice_volume_label, 3, 2)
        
        # Conectar sliders aos labels
        self.master_volume_slider.valueChanged.connect(
            lambda v: self.master_volume_label.setText(f"{v}%"))
        self.music_volume_slider.valueChanged.connect(
            lambda v: self.music_volume_label.setText(f"{v}%"))
        self.effects_volume_slider.valueChanged.connect(
            lambda v: self.effects_volume_label.setText(f"{v}%"))
        self.voice_volume_slider.valueChanged.connect(
            lambda v: self.voice_volume_label.setText(f"{v}%"))
        
        # Silenciar tudo
        self.mute_all_checkbox = QCheckBox("🔇 Silenciar Tudo")
        volume_layout.addWidget(self.mute_all_checkbox, 4, 0, 1, 3)
        
        layout.addWidget(volume_group)
        layout.addStretch()
        
        self.tab_widget.addTab(audio_tab, "🔊 Áudio")
    
    def create_visual_tab(self):
        """Cria a aba de configurações visuais"""
        visual_tab = QWidget()
        layout = QVBoxLayout(visual_tab)
        layout.setSpacing(20)
        
        # Grupo: Interface
        interface_group = QGroupBox("🎨 Interface Visual")
        interface_layout = QGridLayout(interface_group)
        
        # Mostrar percentual
        self.show_percentage_checkbox = QCheckBox("Mostrar Percentual de Preenchimento")
        interface_layout.addWidget(self.show_percentage_checkbox, 0, 0, 1, 2)
        
        # Mostrar timer
        self.show_timer_checkbox = QCheckBox("Mostrar Timer")
        interface_layout.addWidget(self.show_timer_checkbox, 1, 0, 1, 2)
        
        # Mostrar barra de progresso
        self.show_progress_checkbox = QCheckBox("Mostrar Barra de Progresso")
        interface_layout.addWidget(self.show_progress_checkbox, 2, 0, 1, 2)
        
        # Espelhar câmera
        self.mirror_camera_checkbox = QCheckBox("Espelhar Imagem da Câmera")
        interface_layout.addWidget(self.mirror_camera_checkbox, 3, 0, 1, 2)
        
        # Espessura do contorno
        interface_layout.addWidget(QLabel("Espessura do Contorno:"), 4, 0)
        self.contour_thickness_spinbox = QSpinBox()
        self.contour_thickness_spinbox.setRange(1, 10)
        self.contour_thickness_spinbox.setSuffix(" pixels")
        interface_layout.addWidget(self.contour_thickness_spinbox, 4, 1)
        
        layout.addWidget(interface_group)
        layout.addStretch()
        
        self.tab_widget.addTab(visual_tab, "🎨 Visual")
    
    def create_stats_tab(self):
        """Cria a aba de estatísticas"""
        stats_tab = QWidget()
        layout = QVBoxLayout(stats_tab)
        layout.setSpacing(20)
        
        # Grupo: Estatísticas
        stats_group = QGroupBox("📊 Suas Estatísticas")
        stats_layout = QGridLayout(stats_group)
        
        # Labels para mostrar estatísticas
        self.stats_labels = {}
        stats_items = [
            ("games_played", "Jogos Jogados:"),
            ("games_won", "Jogos Vencidos:"),
            ("best_percentage", "Melhor Percentual:"),
            ("best_time", "Melhor Tempo:"),
            ("total_playtime", "Tempo Total Jogado:"),
            ("photos_saved", "Fotos Salvas:")
        ]
        
        for i, (key, label) in enumerate(stats_items):
            stats_layout.addWidget(QLabel(label), i, 0)
            value_label = QLabel("0")
            value_label.setStyleSheet("font-weight: bold; color: #00aa00;")
            stats_layout.addWidget(value_label, i, 1)
            self.stats_labels[key] = value_label
        
        layout.addWidget(stats_group)
        
        # Botão para resetar estatísticas
        reset_stats_btn = QPushButton("🗑️ Resetar Estatísticas")
        reset_stats_btn.clicked.connect(self.reset_statistics)
        reset_stats_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff6666;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff4444;
            }
        """)
        layout.addWidget(reset_stats_btn)
        
        layout.addStretch()
        
        self.tab_widget.addTab(stats_tab, "📊 Stats")
    
    def create_action_buttons(self, layout):
        """Cria os botões de ação"""
        buttons_layout = QHBoxLayout()
        
        # Botão Restaurar Padrões
        restore_btn = QPushButton("🔄 Restaurar Padrões")
        restore_btn.clicked.connect(self.restore_defaults)
        restore_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffaa00;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff8800;
            }
        """)
        
        # Botão Cancelar
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """)
        
        # Botão Salvar
        save_btn = QPushButton("💾 Salvar")
        save_btn.clicked.connect(self.save_settings)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #00aa00;
                color: white;
                font-weight: bold;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #008800;
            }
        """)
        
        buttons_layout.addWidget(restore_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def load_current_settings(self):
        """Carrega as configurações atuais nos controles"""
        # Configurações do jogo
        self.duration_spinbox.setValue(self.config_manager.get('game', 'duration', 300))
        self.threshold_spinbox.setValue(int(self.config_manager.get('game', 'win_threshold', 30.0)))
        self.sensitivity_spinbox.setValue(self.config_manager.get('game', 'min_body_pixels', 1000))
        self.fullscreen_checkbox.setChecked(self.config_manager.get('game', 'fullscreen', True))
        self.auto_save_checkbox.setChecked(self.config_manager.get('game', 'auto_save_photos', True))
        
        # Configurações de áudio
        self.master_volume_slider.setValue(int(self.config_manager.get('audio', 'master_volume', 0.7) * 100))
        self.music_volume_slider.setValue(int(self.config_manager.get('audio', 'music_volume', 0.5) * 100))
        self.effects_volume_slider.setValue(int(self.config_manager.get('audio', 'effects_volume', 0.8) * 100))
        self.voice_volume_slider.setValue(int(self.config_manager.get('audio', 'voice_volume', 0.9) * 100))
        self.mute_all_checkbox.setChecked(self.config_manager.get('audio', 'mute_all', False))
        
        # Configurações visuais
        self.show_percentage_checkbox.setChecked(self.config_manager.get('visual', 'show_percentage', True))
        self.show_timer_checkbox.setChecked(self.config_manager.get('visual', 'show_timer', True))
        self.show_progress_checkbox.setChecked(self.config_manager.get('visual', 'show_progress_bar', True))
        self.mirror_camera_checkbox.setChecked(self.config_manager.get('visual', 'camera_mirror', True))
        self.contour_thickness_spinbox.setValue(self.config_manager.get('visual', 'contour_thickness', 3))
        
        # Estatísticas
        self.load_statistics()
    
    def load_statistics(self):
        """Carrega e exibe as estatísticas"""
        stats = self.config_manager.config.get('stats', {})
        
        self.stats_labels['games_played'].setText(str(stats.get('games_played', 0)))
        self.stats_labels['games_won'].setText(str(stats.get('games_won', 0)))
        self.stats_labels['best_percentage'].setText(f"{stats.get('best_percentage', 0.0):.1f}%")
        
        best_time = stats.get('best_time', 0.0)
        if best_time > 0:
            minutes = int(best_time // 60)
            seconds = int(best_time % 60)
            self.stats_labels['best_time'].setText(f"{minutes}:{seconds:02d}")
        else:
            self.stats_labels['best_time'].setText("--:--")
        
        total_time = stats.get('total_playtime', 0.0)
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        self.stats_labels['total_playtime'].setText(f"{hours}h {minutes}m")
        
        self.stats_labels['photos_saved'].setText(str(stats.get('photos_saved', 0)))
    
    def save_settings(self):
        """Salva as configurações"""
        try:
            # Salvar configurações do jogo
            self.config_manager.set('game', 'duration', self.duration_spinbox.value(), save=False)
            self.config_manager.set('game', 'win_threshold', float(self.threshold_spinbox.value()), save=False)
            self.config_manager.set('game', 'min_body_pixels', self.sensitivity_spinbox.value(), save=False)
            self.config_manager.set('game', 'fullscreen', self.fullscreen_checkbox.isChecked(), save=False)
            self.config_manager.set('game', 'auto_save_photos', self.auto_save_checkbox.isChecked(), save=False)
            
            # Salvar configurações de áudio
            self.config_manager.set('audio', 'master_volume', self.master_volume_slider.value() / 100.0, save=False)
            self.config_manager.set('audio', 'music_volume', self.music_volume_slider.value() / 100.0, save=False)
            self.config_manager.set('audio', 'effects_volume', self.effects_volume_slider.value() / 100.0, save=False)
            self.config_manager.set('audio', 'voice_volume', self.voice_volume_slider.value() / 100.0, save=False)
            self.config_manager.set('audio', 'mute_all', self.mute_all_checkbox.isChecked(), save=False)
            
            # Salvar configurações visuais
            self.config_manager.set('visual', 'show_percentage', self.show_percentage_checkbox.isChecked(), save=False)
            self.config_manager.set('visual', 'show_timer', self.show_timer_checkbox.isChecked(), save=False)
            self.config_manager.set('visual', 'show_progress_bar', self.show_progress_checkbox.isChecked(), save=False)
            self.config_manager.set('visual', 'camera_mirror', self.mirror_camera_checkbox.isChecked(), save=False)
            self.config_manager.set('visual', 'contour_thickness', self.contour_thickness_spinbox.value(), save=False)
            
            # Salvar tudo de uma vez
            if self.config_manager.save_config():
                QMessageBox.information(self, "Sucesso", "✅ Configurações salvas com sucesso!")
                self.settings_changed.emit()
                self.accept()
            else:
                QMessageBox.warning(self, "Erro", "❌ Erro ao salvar configurações.")
                
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"❌ Erro inesperado: {e}")
    
    def restore_defaults(self):
        """Restaura configurações padrão"""
        reply = QMessageBox.question(self, "Confirmar", 
                                   "🔄 Tem certeza que deseja restaurar todas as configurações padrão?",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.config_manager.reset_to_defaults():
                self.load_current_settings()
                QMessageBox.information(self, "Sucesso", "✅ Configurações padrão restauradas!")
            else:
                QMessageBox.warning(self, "Erro", "❌ Erro ao restaurar configurações padrão.")
    
    def reset_statistics(self):
        """Reseta as estatísticas"""
        reply = QMessageBox.question(self, "Confirmar", 
                                   "🗑️ Tem certeza que deseja resetar todas as estatísticas?\n\nEsta ação não pode ser desfeita!",
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.config_manager.reset_to_defaults('stats'):
                self.load_statistics()
                QMessageBox.information(self, "Sucesso", "✅ Estatísticas resetadas!")
            else:
                QMessageBox.warning(self, "Erro", "❌ Erro ao resetar estatísticas.")


def show_config_window(parent=None):
    """
    Mostra a janela de configurações
    
    Args:
        parent: Widget pai
        
    Returns:
        bool: True se configurações foram alteradas
    """
    # Verificar se já existe uma instância do QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    config_window = ConfigWindow(parent)
    
    # Variável para controlar se houve mudanças
    settings_changed = {'changed': False}
    
    def on_settings_changed():
        settings_changed['changed'] = True
    
    config_window.settings_changed.connect(on_settings_changed)
    
    config_window.exec_()
    
    return settings_changed['changed']


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfigWindow()
    window.show()
    sys.exit(app.exec_())
