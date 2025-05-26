"""
CONTROLADOR DO JOGO VIVA SERGIPE!
Sistema para coordenar menu PyQt e jogo OpenCV
"""

import threading
import time
import queue
import os
from enum import Enum
from sync_manager import get_sync_manager

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    VICTORY = "victory"
    SNAPSHOTS = "snapshots"

class GameController:
    """Controlador principal do jogo"""

    def __init__(self):
        self.state = GameState.MENU
        self.command_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.game_thread = None
        self.menu_thread = None
        self.running = True

        # Resultados do jogo
        self.last_fill_percentage = 0.0
        self.game_won = False

    def start(self):
        """Inicia o controlador"""
        print("Iniciando Game Controller...")

        # Inicia o jogo em background (invisível)
        self.game_thread = threading.Thread(target=self._run_game_background, daemon=True)
        self.game_thread.start()

        # Inicia o menu
        self._show_menu()

    def _run_game_background(self):
        """Executa o jogo em background"""
        from sergipe_game_headless import run_game_headless
        run_game_headless(self.command_queue, self.result_queue)

    def _show_menu(self):
        """Mostra o menu principal"""
        while self.running:
            if self.state == GameState.MENU:
                choice = self._show_main_menu()
                if choice == "play":
                    self._start_game()
                elif choice == "exit":
                    self._exit_game()

            elif self.state == GameState.PLAYING:
                # Aguarda resultado do jogo
                self._wait_for_game_result()
                # Pequeno delay para não sobrecarregar
                import time
                time.sleep(0.1)

            elif self.state == GameState.GAME_OVER or self.state == GameState.VICTORY:
                print(f"Mostrando menu pós-jogo - Estado: {self.state}")
                choice = self._show_post_game_menu()
                print(f"Usuário escolheu: {choice}")
                if choice == "play_again":
                    self._start_game()
                elif choice == "snapshots":
                    self._show_snapshots()
                elif choice == "exit":
                    self._exit_game()

            elif self.state == GameState.SNAPSHOTS:
                self._show_snapshots_viewer()
                self.state = GameState.MENU

    def _show_main_menu(self):
        """Mostra menu principal"""
        from menu_gui import show_main_menu
        return show_main_menu()

    def _show_post_game_menu(self):
        """Mostra menu pós-jogo"""
        from menu_gui import show_post_game_menu
        return show_post_game_menu(self.game_won, self.last_fill_percentage)

    def _show_snapshots_viewer(self):
        """Mostra visualizador de snapshots"""
        from menu_gui import show_snapshots_viewer
        show_snapshots_viewer()

    def _start_game(self):
        """Inicia o jogo"""
        print("Iniciando jogo...")
        self.state = GameState.PLAYING

        # Envia comando para mostrar jogo
        self.command_queue.put({"action": "show_game"})

    def _wait_for_game_result(self):
        """Aguarda resultado do jogo sem bloquear o menu"""
        try:
            result = self.result_queue.get(timeout=1)  # Timeout curto para não bloquear
            self.last_fill_percentage = result.get("fill_percentage", 0.0)
            self.game_won = result.get("won", False)

            print(f"Jogo terminou - Vitória: {self.game_won}, Preenchimento: {self.last_fill_percentage:.1f}%")

            if self.game_won:
                self.state = GameState.VICTORY
                print("Estado mudou para VICTORY - menu pós-jogo será mostrado")
            else:
                self.state = GameState.GAME_OVER
                print("Estado mudou para GAME_OVER - menu pós-jogo será mostrado")

        except queue.Empty:
            # Continua aguardando - jogo ainda está rodando
            pass

    def _show_snapshots(self):
        """Mostra snapshots"""
        self.state = GameState.SNAPSHOTS

    def _exit_game(self):
        """Sai do jogo"""
        print("Saindo do jogo...")
        self.running = False
        self.command_queue.put({"action": "exit"})


def main():
    """Função principal"""
    controller = GameController()
    controller.start()


if __name__ == "__main__":
    main()
