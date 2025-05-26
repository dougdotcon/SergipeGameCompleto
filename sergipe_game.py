######################
### VIVA SERGIPE! ###
######################
"""
VIVA SERGIPE!
Jogo interativo de preenchimento corporal baseado no mapa de Sergipe
Adaptado da base do projeto STRIKE A POSE!

Objetivo: Usar o corpo para preencher ≥95% do contorno do mapa de Sergipe em 5 minutos

Controles:
- SPACE: Iniciar/Reiniciar jogo
- Q ou ESC: Sair do jogo
- R: Reiniciar aplicação
- F11: Alternar tela cheia/janela
"""

##############
### IMPORT ###
##############

import cv2  # OpenCV for video capture and processing
import time  # Time-related functions for timing operations
import numpy as np  # NumPy for numerical computations
import sys  # System-specific parameters and functions
import os  # Operating system-related functions
import pygame  # Import pygame for audio processing
from datetime import datetime

# Import PyQt menu
from menu_gui import show_menu

# Import configuration manager
from config_manager import get_config_manager

# Import visual feedback and sync managers
from visual_feedback import get_visual_feedback_manager
from sync_manager import get_sync_manager

# Import performance optimizer and new systems
from performance_optimizer import get_performance_optimizer
from game_modes import get_game_mode_manager
from achievements import get_achievement_manager

# Import custom utility functions
from utils import (
    initialize_pose_model,
    process_frame,
)

# Import Sergipe-specific functions
from sergipe_utils import (
    load_sergipe_contour,
    create_body_mask,
    calculate_fill_percentage,
    save_victory_photo,
    display_sergipe_interface,
    display_victory_message,
    display_game_over_message,
)

##################
### PARAMETERS ###
##################

# Initialize managers
config_manager = get_config_manager()
visual_feedback = get_visual_feedback_manager()
sync_manager = get_sync_manager()
performance_optimizer = get_performance_optimizer()
game_mode_manager = get_game_mode_manager()
achievement_manager = get_achievement_manager()

# Load game settings from configuration (with mode support)
current_mode = config_manager.get('game', 'current_mode', 'classic')
if current_mode != 'classic':
    try:
        from game_modes import GameMode
        mode_enum = GameMode(current_mode)
        game_mode_manager.set_current_mode(mode_enum)
        GAME_SETTINGS = game_mode_manager.get_game_settings_for_mode()
    except:
        GAME_SETTINGS = config_manager.get_game_settings()
else:
    GAME_SETTINGS = config_manager.get_game_settings()

CONTOUR_PATH = "assets/contorno-mapa-SE.png"
SNAPSHOTS_DIR = "snapshots"

# Game states
MENU_MAIN = 0
MENU_CONFIG = 1
GAME_PLAYING = 2

# Create snapshots directory if it doesn't exist
if not os.path.exists(SNAPSHOTS_DIR):
    os.makedirs(SNAPSHOTS_DIR)

#################
### EXECUTION ###
#################

def main():
    """Função principal - usa o novo sistema de controle"""
    try:
        from game_controller import GameController
        controller = GameController()
        controller.start()
    except Exception as e:
        print(f"Erro ao iniciar sistema: {e}")
        # Fallback para o sistema antigo
        print("Usando sistema antigo...")
        try:
            if not show_menu():
                return
            print("Iniciando jogo...")
            start_game()
        except Exception as e2:
            print(f"Erro no sistema antigo: {e2}")
            print("Verifique se PyQt5 está instalado.")


def start_game():
    """Inicia o jogo diretamente"""
    # Initialize game variables
    game_started = True  # Start immediately
    start_time = time.time()
    game_start_time = start_time  # Para calcular tempo total de jogo
    time_left = GAME_SETTINGS['duration']
    fill_percentage = 0.0
    game_won = False
    game_over = False
    fullscreen = config_manager.get('game', 'fullscreen', True)  # Load from config

    # Load Sergipe contour
    contour_mask = load_sergipe_contour(CONTOUR_PATH)
    if contour_mask is None:
        print("Error: Could not load Sergipe contour. Please check the file path.")
        return

    capture = cv2.VideoCapture(0)  # Opens the camera

    # Check if camera opened successfully
    if not capture.isOpened():
        print("Error: Could not open camera.")
        return

    # Set camera resolution for better performance
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    print("Camera initialized successfully")

    # Get screen resolution for fullscreen mode
    screen_width = 1920  # Default values
    screen_height = 1080
    try:
        import tkinter as tk
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()
    except:
        pass  # Use default values if tkinter fails

    # Create fullscreen window
    cv2.namedWindow("VIVA SERGIPE!", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("VIVA SERGIPE!", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Initialize MediaPipe's pose landmark detection
    print("Initializing MediaPipe pose model...")
    pose = initialize_pose_model()
    print("MediaPipe pose model initialized")

    # Initialize pygame for audio processing
    pygame.init()
    pygame.mixer.init()

    # Load sounds (using existing STRIKE A POSE sounds)
    try:
        press_space_sound = pygame.mixer.Sound("./sounds/confirmation.mp3")
        countdown_sound = pygame.mixer.Sound("./sounds/countdown.mp3")
        victory_sound = pygame.mixer.Sound("./sounds/game_over_100.mp3")
        game_over_sound = pygame.mixer.Sound("./sounds/game_over_50.mp3")
        bye_sound = pygame.mixer.Sound("./sounds/bye.mp3")

        # Load background music
        pygame.mixer.music.load("./sounds/background.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)  # Loop background music

    except pygame.error as e:
        print(f"Warning: Could not load audio files: {e}")
        # Create dummy sound objects to prevent errors
        press_space_sound = None
        countdown_sound = None
        victory_sound = None
        game_over_sound = None
        bye_sound = None

    print("Jogo iniciado!")

    # Variables for FPS calculation and performance
    fps_counter = 0
    fps_start_time = time.time()
    current_fps = 0.0
    frame_count = 0

    # Game loop
    try:
        while True:
            frame_start_time = time.time()
            frame_count += 1

            success, frame = capture.read()

            if not success:
                print("Error: Could not read from camera.")
                break

            # Apply performance optimizations
            frame = performance_optimizer.optimize_frame_processing(frame)

            # Skip frame processing if needed for performance
            if performance_optimizer.should_skip_frame(frame_count):
                cv2.imshow("VIVA SERGIPE!", frame)
                cv2.waitKey(1)
                continue

            # Process frame with MediaPipe (skip detection if needed)
            if performance_optimizer.should_skip_detection(frame_count):
                # Use previous results or create empty results
                class EmptyResults:
                    pose_landmarks = None
                results = EmptyResults()
            else:
                detection_start = time.time()
                results, frame = process_frame(frame, pose)
                detection_time = time.time() - detection_start

            # Mirror the frame for better user experience if configured
            if config_manager.get('visual', 'camera_mirror', True):
                frame = cv2.flip(frame, 1)

            # Resize frame to fullscreen if needed
            if fullscreen:
                frame = cv2.resize(frame, (screen_width, screen_height))

            # Resize contour mask to match frame size
            frame_height, frame_width = frame.shape[:2]
            contour_resized = cv2.resize(contour_mask, (frame_width, frame_height))

            if game_started and not game_over and not game_won:
                # Calculate time left
                elapsed_time = time.time() - start_time
                time_left = max(0, GAME_SETTINGS['duration'] - elapsed_time)

                # Create body mask from MediaPipe results
                body_mask = create_body_mask(results, frame_width, frame_height)
                body_pixels = np.sum(body_mask > 0)

                # Analyze detection quality
                detection_analysis = visual_feedback.analyze_detection_quality(frame, results, body_pixels)

                # Show feedback messages based on analysis
                if detection_analysis["status"] == "none":
                    visual_feedback.show_temporary_message("Posicione-se em frente à câmera", 2.0)
                elif detection_analysis["status"] == "poor":
                    if detection_analysis["issues"]:
                        visual_feedback.show_temporary_message(detection_analysis["issues"][0], 3.0)

                # Show body mask for debugging (overlay in blue) - only if configured
                if config_manager.get('visual', 'show_body_overlay', False) and body_pixels > 0:
                    body_overlay = np.zeros_like(frame)
                    body_overlay[:, :, 0] = body_mask  # Blue channel for body
                    frame = cv2.addWeighted(frame, 0.8, body_overlay, 0.2, 0)

                # Calculate fill percentage only if body is detected
                if body_pixels >= GAME_SETTINGS['min_body_pixels']:
                    fill_percentage = calculate_fill_percentage(body_mask, contour_resized)

                    # Check win condition (only if body is properly detected)
                    if fill_percentage >= GAME_SETTINGS['win_threshold']:
                        game_won = True
                        if victory_sound:
                            victory_sound.play()
                        # Save victory photo
                        save_victory_photo(frame, SNAPSHOTS_DIR, fill_percentage)
                        # Update photo count in config
                        config_manager.update_stats(photos_saved=1)
                else:
                    # No valid body detection, keep previous percentage or set to 0
                    if body_pixels == 0:
                        fill_percentage = 0.0

                # Check game over condition
                if time_left <= 0:
                    game_over = True
                    if game_over_sound:
                        game_over_sound.play()

                # Calculate and update FPS
                fps_counter += 1
                if time.time() - fps_start_time >= 1.0:
                    current_fps = fps_counter / (time.time() - fps_start_time)
                    fps_counter = 0
                    fps_start_time = time.time()

                # Update performance metrics
                frame_processing_time = time.time() - frame_start_time
                detection_time_value = detection_time if 'detection_time' in locals() else 0.0
                performance_optimizer.update_performance_metrics(current_fps, frame_processing_time, detection_time_value)

            # Apply visual feedback enhancements
            if config_manager.get('visual', 'show_detection_feedback', True):
                detection_analysis = visual_feedback.analyze_detection_quality(frame, results, body_pixels if 'body_pixels' in locals() else 0)
                frame = visual_feedback.draw_detection_feedback(frame, detection_analysis)

            # Show calibration guide if detection is poor and game not started
            if not game_started and 'detection_analysis' in locals():
                if detection_analysis["status"] in ["none", "poor"]:
                    frame = visual_feedback.draw_calibration_guide(frame)

            # Enhanced pose landmarks
            frame = visual_feedback.draw_pose_landmarks_enhanced(frame, results)

            # Draw temporary messages
            frame = visual_feedback.draw_messages(frame)

            # Draw performance info if enabled
            if config_manager.get('visual', 'show_debug_info', False):
                frame = visual_feedback.draw_performance_info(frame, current_fps, fill_percentage, body_pixels if 'body_pixels' in locals() else 0)

            # Display game interface
            if game_won:
                display_victory_message(frame, fill_percentage)
            elif game_over:
                display_game_over_message(frame, fill_percentage)
            else:
                display_sergipe_interface(
                    frame,
                    contour_resized,
                    time_left,
                    fill_percentage,
                    game_started,
                    GAME_SETTINGS['win_threshold']
                )

            # Display the frame
            cv2.imshow("VIVA SERGIPE!", frame)

            # Handle key presses
            key = cv2.waitKey(5) & 0xFF

            # Toggle fullscreen with F11 (key code 122)
            if key == 122:  # F11
                fullscreen = not fullscreen
                if fullscreen:
                    cv2.setWindowProperty("VIVA SERGIPE!", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                else:
                    cv2.setWindowProperty("VIVA SERGIPE!", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
                    cv2.resizeWindow("VIVA SERGIPE!", 1280, 720)

            # Handle game controls
            elif key == ord(' '):  # Space bar - start/restart game
                if press_space_sound:
                    press_space_sound.play()
                if countdown_sound:
                    countdown_sound.play()
                    while pygame.mixer.get_busy():
                        pygame.time.wait(100)

                # Reset game state
                game_started = True
                start_time = time.time()
                time_left = GAME_SETTINGS['duration']
                fill_percentage = 0.0
                game_won = False
                game_over = False

            elif key == ord('r'):  # R - restart application
                capture.release()
                cv2.destroyAllWindows()
                main()
                return

            elif key == ord('q') or key == 27:  # Q or ESC - exit game
                if bye_sound:
                    bye_sound.play()
                    while pygame.mixer.get_busy():
                        pygame.time.wait(100)
                break

    except Exception as e:
        print(f"Error in game loop: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Salvar estatísticas do jogo
        try:
            total_game_time = time.time() - game_start_time

            # Atualizar estatísticas
            stats_update = {
                'games_played': 1,
                'total_playtime': total_game_time,
                'best_percentage': fill_percentage
            }

            if game_won:
                stats_update['games_won'] = 1
                # Calcular tempo para alcançar a meta
                time_to_win = GAME_SETTINGS['duration'] - time_left
                stats_update['best_time'] = time_to_win

            config_manager.update_stats(**stats_update)

            # Check achievements
            game_result = {
                'won': game_won,
                'game_time': total_game_time,
                'best_percentage': fill_percentage,
                'completion_time': GAME_SETTINGS['duration'] - time_left if game_won else 0
            }

            newly_unlocked = achievement_manager.check_achievements(game_result)
            if newly_unlocked:
                print(f"🏆 {len(newly_unlocked)} nova(s) conquista(s) desbloqueada(s)!")

        except Exception as e:
            print(f"Erro ao salvar estatísticas: {e}")

        # Cleanup
        performance_optimizer.stop_monitoring()
        capture.release()
        cv2.destroyAllWindows()
        pygame.quit()

if __name__ == "__main__":
    main()
