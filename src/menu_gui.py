#!/usr/bin/env python3
"""
MENU GUI PARA VIVA SERGIPE!
Interface gráfica usando PyQt5 com background da bandeira de Sergipe
"""

import sys
import os
import pygame
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFrame, QSpacerItem,
                             QSizePolicy, QMessageBox, QDialog, QScrollArea, QSlider,
                             QCheckBox, QComboBox, QSpinBox, QGroupBox, QGridLayout, QTabWidget)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QThread, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont, QPainter, QColor, QIcon
import cv2
import numpy as np
from pathlib import Path

# Importar módulos do projeto
try:
    from config_manager import ConfigManager
    from game_modes import GameModeManager
    from . import get_asset_path, get_sound_path
except ImportError:
    # Fallback para imports diretos se necessário
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config_manager import ConfigManager
    from game_modes import GameModeManager

# Configuração do estilo
STYLE_SHEET = """
QMainWindow {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #1e3c72, stop:1 #2a5298);
    color: white;
}

QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #4CAF50, stop:1 #45a049);
    border: 2px solid #4CAF50;
    border-radius: 10px;
    color: white;
    font-size: 16px;
    font-weight: bold;
    padding: 10px;
    min-height: 40px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #45a049, stop:1 #4CAF50);
    border: 2px solid #45a049;
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #3d8b40, stop:1 #4CAF50);
}

QPushButton:disabled {
    background: #cccccc;
    border: 2px solid #cccccc;
    color: #666666;
}

QLabel {
    color: white;
    font-size: 14px;
}

QLabel[class="title"] {
    font-size: 24px;
    font-weight: bold;
    color: #FFD700;
}

QLabel[class="subtitle"] {
    font-size: 18px;
    font-weight: bold;
    color: #FFA500;
}

QGroupBox {
    font-weight: bold;
    border: 2px solid #4CAF50;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    color: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: #FFD700;
}

QSlider::groove:horizontal {
    border: 1px solid #999999;
    height: 8px;
    background: #333333;
    border-radius: 4px;
}

QSlider::handle:horizontal {
    background: #4CAF50;
    border: 1px solid #5c6bc0;
    width: 18px;
    margin: -2px 0;
    border-radius: 9px;
}

QSlider::handle:horizontal:hover {
    background: #45a049;
}

QComboBox {
    border: 2px solid #4CAF50;
    border-radius: 5px;
    padding: 5px;
    background: #333333;
    color: white;
    min-height: 30px;
}

QComboBox::drop-down {
    border: none;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #4CAF50;
    margin-right: 10px;
}

QSpinBox {
    border: 2px solid #4CAF50;
    border-radius: 5px;
    padding: 5px;
    background: #333333;
    color: white;
    min-height: 30px;
}

QCheckBox {
    color: white;
    font-size: 14px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
}

QCheckBox::indicator:unchecked {
    border: 2px solid #4CAF50;
    background: #333333;
    border-radius: 3px;
}

QCheckBox::indicator:checked {
    border: 2px solid #4CAF50;
    background: #4CAF50;
    border-radius: 3px;
}

QTabWidget::pane {
    border: 2px solid #4CAF50;
    border-radius: 5px;
    background: rgba(51, 51, 51, 0.9);
}

QTabBar::tab {
    background: #333333;
    color: white;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
}

QTabBar::tab:selected {
    background: #4CAF50;
    color: white;
}

QTabBar::tab:hover {
    background: #45a049;
}
"""

class HelpWindow(QDialog):
    """
    Janela de ajuda com instruções do jogo
    """
    def __init__(self, help_text, parent=None):
        super().__init__(parent)
        self.help_text = help_text
        self.init_ui()

    def init_ui(self):
        """Inicializa a interface da janela de ajuda"""
        self.setWindowTitle("Como Jogar - Viva Sergipe!")
        self.setFixedSize(800, 600)
        self.setModal(True)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Título
        title_label = QLabel("📖 COMO JOGAR")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #00aa00;
                font-size: 32px;
                font-weight: bold;
                font-family: 'Arial Black', Arial, sans-serif;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(title_label)

        # Texto de ajuda
        help_label = QLabel(self.help_text)
        help_label.setAlignment(Qt.AlignLeft)
        help_label.setWordWrap(True)
        help_label.setStyleSheet("""
            QLabel {
                color: #000000;
                font-size: 16px;
                font-family: Arial, sans-serif;
                background-color: #ffffff;
                border: 2px solid #00aa00;
                border-radius: 10px;
                padding: 20px;
                line-height: 1.5;
            }
        """)
        layout.addWidget(help_label)

        # Botão OK
        ok_button = QPushButton("✅ ENTENDI")
        ok_button.clicked.connect(self.accept)
        ok_button.setStyleSheet("""
            QPushButton {
                background-color: #00aa00;
                color: white;
                font-size: 18px;
                font-weight: bold;
                font-family: Arial, sans-serif;
                border: none;
                border-radius: 10px;
                padding: 15px 30px;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #00cc00;
            }
            QPushButton:pressed {
                background-color: #008800;
            }
        """)
        layout.addWidget(ok_button)

        # Centralizar janela
        self.center_window()

    def center_window(self):
        """Centraliza a janela na tela"""
        if self.parent():
            # Centralizar em relação ao parent
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)

    def keyPressEvent(self, event):
        """Trata eventos de teclado - apenas teclas permitidas"""
        # Lista de teclas permitidas
        allowed_keys = [
            Qt.Key_Escape,
            Qt.Key_Return,
            Qt.Key_Enter
        ]

        # Verificar se a tecla é permitida
        if event.key() not in allowed_keys:
            # Bloquear tecla - não fazer nada
            return

        # Processar teclas permitidas
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.accept()
        else:
            super().keyPressEvent(event)


class SergipeMenuWindow(QMainWindow):
    """
    Janela principal do menu do jogo Viva Sergipe!
    """
    start_game_signal = pyqtSignal()
    exit_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.current_button = 0  # Índice do botão selecionado
        self.buttons = []  # Lista de botões para navegação
        self.config_manager = ConfigManager()
        self.game_mode_manager = GameModeManager()
        self.init_ui()
        self.init_audio()

    def init_audio(self):
        """Inicializa o sistema de áudio"""
        try:
            pygame.mixer.init()
            # Carrega sons do menu
            self.click_sound = pygame.mixer.Sound(get_sound_path("sounds/confirmation.mp3"))
            self.bye_sound = pygame.mixer.Sound(get_sound_path("sounds/bye.mp3"))

            # Música de fundo
            pygame.mixer.music.load(get_sound_path("sounds/background.mp3"))
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)  # Loop infinito

        except Exception as e:
            print(f"Aviso: Não foi possível carregar os arquivos de áudio: {e}")
            self.click_sound = None
            self.bye_sound = None

    def init_ui(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle("VIVA SERGIPE! - Menu Principal")

        # Configurar para fullscreen
        self.setWindowState(Qt.WindowFullScreen)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Configurar background da bandeira de Sergipe
        self.set_sergipe_flag_background()

        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(100, 80, 100, 80)  # Margens maiores para fullscreen
        main_layout.setSpacing(40)  # Espaçamento maior

        # Título principal
        self.create_title_section(main_layout)

        # Espaçador
        main_layout.addItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botões do menu
        self.create_menu_buttons(main_layout)

        # Espaçador
        main_layout.addItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Informações na parte inferior
        self.create_footer_info(main_layout)

    def set_sergipe_flag_background(self):
        """Define a bandeira de Sergipe como background"""
        try:
            # Carrega a imagem da bandeira
            pixmap = QPixmap(get_asset_path("flag-se.jpg"))

            if not pixmap.isNull():
                # Redimensiona para cobrir toda a janela
                scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

                # Define como background
                palette = QPalette()
                palette.setBrush(QPalette.Background, QBrush(scaled_pixmap))
                self.setPalette(palette)
            else:
                # Fallback: cores da bandeira de Sergipe
                self.setStyleSheet("""
                    QMainWindow {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #1e3a8a, stop:0.33 #16a34a, stop:0.66 #eab308, stop:1 #16a34a);
                    }
                """)
        except Exception as e:
            print(f"Erro ao carregar background: {e}")
            # Fallback: cores da bandeira
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1e3a8a, stop:0.33 #16a34a, stop:0.66 #eab308, stop:1 #16a34a);
                }
            """)

    def create_title_section(self, layout):
        """Cria a seção do título"""
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 180);
                border-radius: 20px;
                border: 3px solid #ffffff;
            }
        """)

        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(30, 20, 30, 20)

        # Título principal
        title_label = QLabel("🌟 VIVA SERGIPE! 🌟")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #00ff00;
                font-size: 72px;
                font-weight: bold;
                font-family: 'Arial Black', Arial, sans-serif;
                background: transparent;
                border: none;
            }
        """)

        # Subtítulo
        subtitle_label = QLabel("Jogo de Preenchimento Corporal")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 36px;
                font-weight: bold;
                font-family: Arial, sans-serif;
                background: transparent;
                border: none;
                margin-top: 15px;
            }
        """)

        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        layout.addWidget(title_frame)

    def create_menu_buttons(self, layout):
        """Cria os botões do menu"""
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 150);
                border-radius: 15px;
                border: 2px solid #ffffff;
            }
        """)

        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(40, 30, 40, 30)
        buttons_layout.setSpacing(20)

        # Estilo dos botões
        button_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                color: #000000;
                font-size: 42px;
                font-weight: bold;
                font-family: 'Arial Black', Arial, sans-serif;
                border: 4px solid #ffffff;
                border-radius: 20px;
                padding: 25px 50px;
                min-height: 80px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 0, 200);
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: rgba(0, 200, 0, 255);
                border: 4px solid #00ff00;
            }
        """

        # Botão Jogar
        play_button = QPushButton("🎮 JOGAR")
        play_button.clicked.connect(self.start_game)

        # Botão Configurações
        config_button = QPushButton("⚙️ CONFIGURAÇÕES")
        config_button.clicked.connect(self.show_config)

        # Botão Como Jogar
        help_button = QPushButton("❓ COMO JOGAR")
        help_button.clicked.connect(self.show_help)

        # Botão Sair
        exit_button = QPushButton("🚪 SAIR")
        exit_button.clicked.connect(self.exit_game)

        # Armazenar botões para navegação
        self.buttons = [play_button, config_button, help_button, exit_button]

        # Aplicar estilos e adicionar ao layout
        for i, button in enumerate(self.buttons):
            self.update_button_style(button, i == self.current_button)
            buttons_layout.addWidget(button)

        layout.addWidget(buttons_frame)

        # Garantir que o primeiro botão esteja visualmente selecionado
        if self.buttons:
            self.update_button_style(self.buttons[self.current_button], True)

    def create_footer_info(self, layout):
        """Cria informações do rodapé"""
        footer_frame = QFrame()
        footer_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 120);
                border-radius: 10px;
                border: 1px solid #ffffff;
            }
        """)

        footer_layout = QVBoxLayout(footer_frame)
        footer_layout.setContentsMargins(20, 15, 20, 15)

        info_label = QLabel("Use seu corpo para preencher o mapa de Sergipe!\nMeta: 30% de preenchimento em 5 minutos\n\n⌨️ Use ↑↓ para navegar e ENTER para selecionar")
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                font-family: Arial, sans-serif;
                background: transparent;
                border: none;
            }
        """)

        footer_layout.addWidget(info_label)
        layout.addWidget(footer_frame)

    def center_window(self):
        """Centraliza a janela na tela"""
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

    def start_game(self):
        """Inicia o jogo"""
        if self.click_sound:
            self.click_sound.play()

        # Para a música de fundo
        pygame.mixer.music.stop()

        # Emite sinal para iniciar o jogo
        self.start_game_signal.emit()
        self.close()

    def show_config(self):
        """Mostra a janela de configurações"""
        try:
            from config_window import show_config_window

            if self.click_sound:
                self.click_sound.play()

            # Mostrar janela de configurações
            settings_changed = show_config_window(self)

            if settings_changed:
                # Recarregar configurações se foram alteradas
                print("✅ Configurações atualizadas!")

        except ImportError as e:
            QMessageBox.warning(self, "Erro", f"❌ Erro ao carregar configurações: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"❌ Erro inesperado: {e}")

    def show_help(self):
        """Mostra as instruções do jogo"""
        if self.click_sound:
            self.click_sound.play()

        help_text = """🎯 OBJETIVO:
Use seu corpo para preencher pelo menos 30% do contorno do mapa de Sergipe em 5 minutos!

🎮 COMO JOGAR:
1. Clique "JOGAR" no menu
2. O jogo inicia automaticamente em tela cheia
3. Mova seu corpo para preencher o mapa verde
4. Alcance a meta antes do tempo acabar!

⌨️ CONTROLES:
• ↑↓: Navegar no menu
• ENTER: Selecionar opção
• ESC: Voltar/Sair
• Q: Sair do jogo

🏆 DICAS:
• Use braços e pernas para cobrir mais área
• Mantenha-se dentro do campo de visão da câmera
• Seja criativo com suas poses!"""

        # Criar janela de ajuda personalizada
        help_window = HelpWindow(help_text, self)
        help_window.exec_()

    def exit_game(self):
        """Sai do jogo"""
        if self.bye_sound:
            self.bye_sound.play()
            # Aguarda o som terminar
            QTimer.singleShot(1000, self.close_application)
        else:
            self.close_application()

    def close_application(self):
        """Fecha a aplicação"""
        pygame.mixer.quit()
        self.exit_signal.emit()
        self.close()

    def update_button_style(self, button, selected):
        """Atualiza o estilo do botão baseado na seleção"""
        # Definir propriedade personalizada para controle
        button.setProperty("selected", selected)

        if selected:
            # Estilo do botão selecionado - VERDE
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgb(0, 255, 0);
                    color: rgb(255, 255, 255);
                    font-size: 42px;
                    font-weight: bold;
                    font-family: 'Arial Black', Arial, sans-serif;
                    border: 4px solid rgb(0, 255, 0);
                    border-radius: 20px;
                    padding: 25px 50px;
                    min-height: 80px;
                }
            """)
        else:
            # Estilo do botão normal - BRANCO
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 200);
                    color: rgb(0, 0, 0);
                    font-size: 42px;
                    font-weight: bold;
                    font-family: 'Arial Black', Arial, sans-serif;
                    border: 4px solid rgb(255, 255, 255);
                    border-radius: 20px;
                    padding: 25px 50px;
                    min-height: 80px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 230);
                    border: 4px solid rgb(200, 200, 200);
                }
            """)

    def navigate_buttons(self, direction):
        """Navega entre os botões"""
        if not self.buttons:
            return

        # Mover seleção
        if direction == "up":
            self.current_button = (self.current_button - 1) % len(self.buttons)
        elif direction == "down":
            self.current_button = (self.current_button + 1) % len(self.buttons)

        # Atualizar TODOS os botões para garantir que apenas o selecionado fique verde
        for i, button in enumerate(self.buttons):
            is_selected = (i == self.current_button)
            self.update_button_style(button, is_selected)
            button.update()

        # Forçar atualização visual imediata
        QApplication.processEvents()

        # Som de navegação
        if self.click_sound:
            self.click_sound.play()

    def activate_current_button(self):
        """Ativa o botão atualmente selecionado"""
        if self.buttons and 0 <= self.current_button < len(self.buttons):
            self.buttons[self.current_button].click()

    def keyPressEvent(self, event):
        """Trata eventos de teclado - apenas teclas permitidas"""
        # Lista de teclas permitidas
        allowed_keys = [
            Qt.Key_Escape,
            Qt.Key_Up,
            Qt.Key_Down,
            Qt.Key_Left,
            Qt.Key_Right,
            Qt.Key_Return,
            Qt.Key_Enter
        ]

        # Verificar se a tecla é permitida
        if event.key() not in allowed_keys:
            # Bloquear tecla - não fazer nada
            return

        # Processar teclas permitidas
        if event.key() == Qt.Key_Escape:
            self.exit_game()
        elif event.key() == Qt.Key_Up:
            self.navigate_buttons("up")
        elif event.key() == Qt.Key_Down:
            self.navigate_buttons("down")
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.activate_current_button()
        # Left/Right não fazem nada neste menu, mas são permitidas
        else:
            super().keyPressEvent(event)


class PostGameMenuWindow(QMainWindow):
    """
    Janela do menu pós-jogo (vitória/derrota)
    """
    play_again_signal = pyqtSignal()
    snapshots_signal = pyqtSignal()
    exit_signal = pyqtSignal()

    def __init__(self, won, fill_percentage):
        super().__init__()
        self.won = won
        self.fill_percentage = fill_percentage
        self.current_button = 0  # Índice do botão selecionado
        self.buttons = []  # Lista de botões para navegação
        self.init_ui()
        self.init_audio()

    def init_audio(self):
        """Inicializa o sistema de áudio"""
        try:
            pygame.mixer.init()
            self.click_sound = pygame.mixer.Sound(get_sound_path("sounds/confirmation.mp3"))
            self.bye_sound = pygame.mixer.Sound(get_sound_path("sounds/bye.mp3"))
        except Exception as e:
            print(f"Aviso: Não foi possível carregar os arquivos de áudio: {e}")
            self.click_sound = None
            self.bye_sound = None

    def init_ui(self):
        """Inicializa a interface do usuário"""
        if self.won:
            self.setWindowTitle("🎉 VITÓRIA! - Viva Sergipe!")
        else:
            self.setWindowTitle("⏰ Fim de Jogo - Viva Sergipe!")

        # Configurar para fullscreen
        self.setWindowState(Qt.WindowFullScreen)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Configurar background
        self.set_sergipe_flag_background()

        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(100, 80, 100, 80)  # Margens maiores para fullscreen
        main_layout.setSpacing(50)  # Espaçamento maior

        # Título do resultado
        self.create_result_section(main_layout)

        # Espaçador
        main_layout.addItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botões do menu
        self.create_post_game_buttons(main_layout)

        # Espaçador
        main_layout.addItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def set_sergipe_flag_background(self):
        """Define a bandeira de Sergipe como background"""
        try:
            pixmap = QPixmap(get_asset_path("flag-se.jpg"))
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                palette = QPalette()
                palette.setBrush(QPalette.Background, QBrush(scaled_pixmap))
                self.setPalette(palette)
            else:
                self.setStyleSheet("""
                    QMainWindow {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                            stop:0 #1e3a8a, stop:0.33 #16a34a, stop:0.66 #eab308, stop:1 #16a34a);
                    }
                """)
        except Exception as e:
            print(f"Erro ao carregar background: {e}")
            self.setStyleSheet("""
                QMainWindow {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 #1e3a8a, stop:0.33 #16a34a, stop:0.66 #eab308, stop:1 #16a34a);
                }
            """)

    def create_result_section(self, layout):
        """Cria a seção do resultado"""
        result_frame = QFrame()
        result_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 180);
                border-radius: 20px;
                border: 3px solid #ffffff;
            }
        """)

        result_layout = QVBoxLayout(result_frame)
        result_layout.setContentsMargins(30, 20, 30, 20)

        if self.won:
            # Título de vitória
            title_label = QLabel("🎉 PARABÉNS! 🎉")
            title_label.setStyleSheet("""
                QLabel {
                    color: #00ff00;
                    font-size: 72px;
                    font-weight: bold;
                    font-family: 'Arial Black', Arial, sans-serif;
                    background: transparent;
                    border: none;
                }
            """)

            # Mensagem de vitória
            message_label = QLabel(f"Você preencheu {self.fill_percentage:.1f}% do mapa!")
            message_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 36px;
                    font-weight: bold;
                    font-family: Arial, sans-serif;
                    background: transparent;
                    border: none;
                    margin-top: 15px;
                }
            """)
        else:
            # Título de derrota
            title_label = QLabel("⏰ TEMPO ESGOTADO!")
            title_label.setStyleSheet("""
                QLabel {
                    color: #ff6666;
                    font-size: 64px;
                    font-weight: bold;
                    font-family: 'Arial Black', Arial, sans-serif;
                    background: transparent;
                    border: none;
                }
            """)

            # Mensagem de encorajamento
            message_label = QLabel(f"Você conseguiu {self.fill_percentage:.1f}% - Tente novamente!")
            message_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 36px;
                    font-weight: bold;
                    font-family: Arial, sans-serif;
                    background: transparent;
                    border: none;
                    margin-top: 15px;
                }
            """)

        title_label.setAlignment(Qt.AlignCenter)
        message_label.setAlignment(Qt.AlignCenter)

        result_layout.addWidget(title_label)
        result_layout.addWidget(message_label)
        layout.addWidget(result_frame)

    def create_post_game_buttons(self, layout):
        """Cria os botões do menu pós-jogo"""
        buttons_frame = QFrame()
        buttons_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 150);
                border-radius: 15px;
                border: 2px solid #ffffff;
            }
        """)

        buttons_layout = QVBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(40, 30, 40, 30)
        buttons_layout.setSpacing(20)

        # Estilo dos botões
        button_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                color: #000000;
                font-size: 36px;
                font-weight: bold;
                font-family: 'Arial Black', Arial, sans-serif;
                border: 4px solid #ffffff;
                border-radius: 20px;
                padding: 20px 40px;
                min-height: 70px;
            }
            QPushButton:hover {
                background-color: rgba(0, 255, 0, 200);
                color: #ffffff;
            }
            QPushButton:pressed {
                background-color: rgba(0, 200, 0, 255);
                border: 4px solid #00ff00;
            }
        """

        # Botão Jogar Novamente
        play_again_button = QPushButton("🔄 JOGAR NOVAMENTE")
        play_again_button.clicked.connect(self.play_again)

        # Botão Ver Snapshots
        snapshots_button = QPushButton("📸 VER SNAPSHOTS")
        snapshots_button.clicked.connect(self.view_snapshots)

        # Botão Sair
        exit_button = QPushButton("🚪 SAIR")
        exit_button.clicked.connect(self.exit_game)

        # Armazenar botões para navegação
        self.buttons = [play_again_button, snapshots_button, exit_button]

        # Aplicar estilos e adicionar ao layout
        for i, button in enumerate(self.buttons):
            self.update_button_style(button, i == self.current_button)
            buttons_layout.addWidget(button)

        layout.addWidget(buttons_frame)

        # Garantir que o primeiro botão esteja visualmente selecionado
        if self.buttons:
            self.update_button_style(self.buttons[self.current_button], True)

    def center_window(self):
        """Centraliza a janela na tela"""
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

    def play_again(self):
        """Jogar novamente"""
        if self.click_sound:
            self.click_sound.play()
        self.play_again_signal.emit()
        self.close()

    def view_snapshots(self):
        """Ver snapshots"""
        if self.click_sound:
            self.click_sound.play()
        self.snapshots_signal.emit()
        self.close()

    def exit_game(self):
        """Sair do jogo"""
        if self.bye_sound:
            self.bye_sound.play()
            QTimer.singleShot(1000, self.close_application)
        else:
            self.close_application()

    def close_application(self):
        """Fecha a aplicação"""
        self.exit_signal.emit()
        self.close()

    def update_button_style(self, button, selected):
        """Atualiza o estilo do botão baseado na seleção"""
        # Definir propriedade personalizada para controle
        button.setProperty("selected", selected)

        if selected:
            # Estilo do botão selecionado - VERDE
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgb(0, 255, 0);
                    color: rgb(255, 255, 255);
                    font-size: 36px;
                    font-weight: bold;
                    font-family: 'Arial Black', Arial, sans-serif;
                    border: 4px solid rgb(0, 255, 0);
                    border-radius: 20px;
                    padding: 20px 40px;
                    min-height: 70px;
                }
            """)
        else:
            # Estilo do botão normal - BRANCO
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 200);
                    color: rgb(0, 0, 0);
                    font-size: 36px;
                    font-weight: bold;
                    font-family: 'Arial Black', Arial, sans-serif;
                    border: 4px solid rgb(255, 255, 255);
                    border-radius: 20px;
                    padding: 20px 40px;
                    min-height: 70px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 230);
                    border: 4px solid rgb(200, 200, 200);
                }
            """)

    def navigate_buttons(self, direction):
        """Navega entre os botões"""
        if not self.buttons:
            return

        # Mover seleção
        if direction == "up":
            self.current_button = (self.current_button - 1) % len(self.buttons)
        elif direction == "down":
            self.current_button = (self.current_button + 1) % len(self.buttons)

        # Atualizar TODOS os botões para garantir que apenas o selecionado fique verde
        for i, button in enumerate(self.buttons):
            self.update_button_style(button, i == self.current_button)
            button.repaint()

        # Forçar atualização visual imediata
        QApplication.processEvents()

        # Som de navegação
        if self.click_sound:
            self.click_sound.play()

    def activate_current_button(self):
        """Ativa o botão atualmente selecionado"""
        if self.buttons and 0 <= self.current_button < len(self.buttons):
            self.buttons[self.current_button].click()

    def keyPressEvent(self, event):
        """Trata eventos de teclado - apenas teclas permitidas"""
        # Lista de teclas permitidas
        allowed_keys = [
            Qt.Key_Escape,
            Qt.Key_Up,
            Qt.Key_Down,
            Qt.Key_Left,
            Qt.Key_Right,
            Qt.Key_Return,
            Qt.Key_Enter
        ]

        # Verificar se a tecla é permitida
        if event.key() not in allowed_keys:
            # Bloquear tecla - não fazer nada
            return

        # Processar teclas permitidas
        if event.key() == Qt.Key_Escape:
            self.exit_game()
        elif event.key() == Qt.Key_Up:
            self.navigate_buttons("up")
        elif event.key() == Qt.Key_Down:
            self.navigate_buttons("down")
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.activate_current_button()
        # Left/Right não fazem nada neste menu, mas são permitidas
        else:
            super().keyPressEvent(event)


def show_main_menu():
    """
    Mostra o menu principal
    Retorna: 'play', 'exit'
    """
    # Verificar se já existe uma instância do QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # Configurar ícone da aplicação se existir
    if os.path.exists("logo.png"):
        app.setWindowIcon(QIcon("logo.png"))

    menu = SergipeMenuWindow()

    # Variável para controlar o resultado
    result = {'choice': 'exit'}

    def on_start_game():
        result['choice'] = 'play'
        menu.close()

    def on_exit():
        result['choice'] = 'exit'
        menu.close()

    menu.start_game_signal.connect(on_start_game)
    menu.exit_signal.connect(on_exit)

    menu.show()

    # Usar loop de eventos local
    while menu.isVisible():
        app.processEvents()
        import time
        time.sleep(0.01)

    return result['choice']


def show_post_game_menu(won, fill_percentage):
    """
    Mostra menu pós-jogo
    Retorna: 'play_again', 'snapshots', 'exit'
    """
    # Verificar se já existe uma instância do QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # Configurar ícone da aplicação se existir
    if os.path.exists("logo.png"):
        app.setWindowIcon(QIcon("logo.png"))

    menu = PostGameMenuWindow(won, fill_percentage)

    # Variável para controlar o resultado
    result = {'choice': 'exit'}

    def on_play_again():
        result['choice'] = 'play_again'
        menu.close()

    def on_snapshots():
        result['choice'] = 'snapshots'
        menu.close()

    def on_exit():
        result['choice'] = 'exit'
        menu.close()

    menu.play_again_signal.connect(on_play_again)
    menu.snapshots_signal.connect(on_snapshots)
    menu.exit_signal.connect(on_exit)

    menu.show()

    # Usar loop de eventos local ao invés de app.exec_()
    while menu.isVisible():
        app.processEvents()
        import time
        time.sleep(0.01)

    return result['choice']


def show_snapshots_viewer():
    """
    Mostra visualizador de snapshots
    """
    import os
    import glob

    # Verificar se há snapshots
    snapshots_dir = "snapshots"
    if not os.path.exists(snapshots_dir):
        show_no_snapshots_message()
        return

    # Buscar arquivos de snapshot
    snapshot_files = glob.glob(os.path.join(snapshots_dir, "*.jpg")) + glob.glob(os.path.join(snapshots_dir, "*.png"))

    if not snapshot_files:
        show_no_snapshots_message()
        return

    # Mostrar galeria de snapshots
    app = QApplication(sys.argv)
    viewer = SnapshotsViewerWindow(snapshot_files)
    viewer.show()
    app.exec_()


def show_no_snapshots_message():
    """Mostra mensagem quando não há snapshots"""
    app = QApplication(sys.argv)

    msg = QMessageBox()
    msg.setWindowTitle("📸 Snapshots - Viva Sergipe!")
    msg.setText("Nenhum snapshot encontrado!")
    msg.setInformativeText("Jogue e vença para capturar seus melhores momentos! 🏆")
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setStyleSheet("""
        QMessageBox {
            background-color: #ffffff;
            font-size: 16px;
            font-family: Arial, sans-serif;
            min-width: 400px;
            min-height: 200px;
        }
        QMessageBox QLabel {
            color: #000000;
            font-weight: bold;
            padding: 10px;
        }
        QMessageBox QPushButton {
            background-color: #00aa00;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #00cc00;
        }
    """)
    msg.exec_()


class SnapshotsViewerWindow(QMainWindow):
    """
    Janela para visualizar snapshots
    """
    def __init__(self, snapshot_files):
        super().__init__()
        self.snapshot_files = sorted(snapshot_files, key=os.path.getmtime, reverse=True)  # Mais recentes primeiro
        self.current_index = 0
        self.init_ui()

    def init_ui(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle(f"📸 Snapshots ({len(self.snapshot_files)} fotos) - Viva Sergipe!")

        # Configurar para fullscreen
        self.setWindowState(Qt.WindowFullScreen)
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(60, 40, 60, 40)  # Margens maiores para fullscreen
        main_layout.setSpacing(30)

        # Título
        title_label = QLabel("📸 SEUS MELHORES MOMENTOS 📸")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #00aa00;
                font-size: 48px;
                font-weight: bold;
                font-family: 'Arial Black', Arial, sans-serif;
                margin-bottom: 30px;
            }
        """)
        main_layout.addWidget(title_label)

        # Label para mostrar a imagem
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 3px solid #00aa00;
                border-radius: 10px;
                background-color: #f0f0f0;
            }
        """)
        main_layout.addWidget(self.image_label)

        # Informações da foto
        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("""
            QLabel {
                color: #333333;
                font-size: 24px;
                font-weight: bold;
                font-family: Arial, sans-serif;
                margin: 15px;
                background-color: rgba(255, 255, 255, 200);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        main_layout.addWidget(self.info_label)

        # Botões de navegação
        nav_layout = QVBoxLayout()

        # Botões anterior/próximo
        nav_buttons_layout = QVBoxLayout()

        prev_button = QPushButton("⬅️ ANTERIOR")
        prev_button.clicked.connect(self.prev_image)
        prev_button.setStyleSheet(self.get_button_style())

        next_button = QPushButton("➡️ PRÓXIMO")
        next_button.clicked.connect(self.next_image)
        next_button.setStyleSheet(self.get_button_style())

        close_button = QPushButton("❌ FECHAR")
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet(self.get_button_style())

        nav_buttons_layout.addWidget(prev_button)
        nav_buttons_layout.addWidget(next_button)
        nav_buttons_layout.addWidget(close_button)

        nav_layout.addLayout(nav_buttons_layout)
        main_layout.addLayout(nav_layout)

        # Carregar primeira imagem
        self.load_current_image()

        # Centralizar janela
        self.center_window()

    def get_button_style(self):
        """Retorna o estilo dos botões"""
        return """
            QPushButton {
                background-color: #00aa00;
                color: white;
                font-size: 28px;
                font-weight: bold;
                font-family: Arial, sans-serif;
                border: none;
                border-radius: 15px;
                padding: 20px 40px;
                margin: 10px;
                min-height: 60px;
            }
            QPushButton:hover {
                background-color: #00cc00;
            }
            QPushButton:pressed {
                background-color: #008800;
            }
        """

    def load_current_image(self):
        """Carrega a imagem atual"""
        if not self.snapshot_files:
            return

        current_file = self.snapshot_files[self.current_index]

        # Carregar e redimensionar imagem
        pixmap = QPixmap(current_file)
        if not pixmap.isNull():
            # Redimensionar mantendo proporção para fullscreen
            scaled_pixmap = pixmap.scaled(1200, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

        # Atualizar informações
        filename = os.path.basename(current_file)
        file_time = os.path.getmtime(current_file)
        from datetime import datetime
        time_str = datetime.fromtimestamp(file_time).strftime("%d/%m/%Y às %H:%M:%S")

        info_text = f"📸 {filename}\n🕒 Capturado em {time_str}\n📊 Foto {self.current_index + 1} de {len(self.snapshot_files)}"
        self.info_label.setText(info_text)

    def prev_image(self):
        """Vai para a imagem anterior"""
        if self.current_index > 0:
            self.current_index -= 1
            self.load_current_image()

    def next_image(self):
        """Vai para a próxima imagem"""
        if self.current_index < len(self.snapshot_files) - 1:
            self.current_index += 1
            self.load_current_image()

    def center_window(self):
        """Centraliza a janela na tela"""
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2
        self.move(x, y)

    def keyPressEvent(self, event):
        """Trata eventos de teclado - apenas teclas permitidas"""
        # Lista de teclas permitidas
        allowed_keys = [
            Qt.Key_Escape,
            Qt.Key_Up,
            Qt.Key_Down,
            Qt.Key_Left,
            Qt.Key_Right,
            Qt.Key_Return,
            Qt.Key_Enter
        ]

        # Verificar se a tecla é permitida
        if event.key() not in allowed_keys:
            # Bloquear tecla - não fazer nada
            return

        # Processar teclas permitidas
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Left:
            self.prev_image()
        elif event.key() == Qt.Key_Right:
            self.next_image()
        # Up/Down/Enter não fazem nada neste visualizador, mas são permitidas
        else:
            super().keyPressEvent(event)


def show_menu():
    """
    Função de compatibilidade - mantida para não quebrar código existente
    """
    return show_main_menu() == 'play'


if __name__ == "__main__":
    # Teste do menu
    if show_menu():
        print("Usuário escolheu jogar!")
    else:
        print("Usuário escolheu sair!")
