"""
VIVA SERGIPE! - Versão Headless
Jogo que pode ser controlado externamente via queue
"""

import cv2
import time
import numpy as np
import pygame
import queue
from sergipe_utils import *
from utils import initialize_pose_model, process_frame

# Game settings
GAME_SETTINGS = {
    'duration': 300,  # 5 minutes in seconds
    'win_threshold': 30,  # 30% fill to win
    'min_body_pixels': 1000  # Minimum pixels to consider body detection
}

CONTOUR_PATH = "assets/contorno-mapa-SE.png"
SNAPSHOTS_DIR = "snapshots"

def run_game_headless(command_queue, result_queue):
    """
    Executa o jogo em modo headless, controlado por queues
    """
    # Initialize game components
    contour_mask = load_sergipe_contour(CONTOUR_PATH)
    if contour_mask is None:
        print("Error: Could not load Sergipe contour.")
        return

    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("Error: Could not open camera.")
        return

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # Initialize MediaPipe
    pose = initialize_pose_model()

    # Initialize pygame for audio
    pygame.init()
    pygame.mixer.init()

    # Load sounds
    try:
        victory_sound = pygame.mixer.Sound("./sounds/game_over_100.mp3")
        game_over_sound = pygame.mixer.Sound("./sounds/game_over_50.mp3")
    except:
        victory_sound = None
        game_over_sound = None

    # Game state
    game_visible = False
    game_started = False
    start_time = None
    fill_percentage = 0.0
    game_won = False
    game_over = False

    print("Game headless initialized, waiting for commands...")

    while True:
        # Check for commands
        try:
            command = command_queue.get_nowait()
            action = command.get("action")

            if action == "show_game":
                game_visible = True
                game_started = True
                start_time = time.time()
                fill_percentage = 0.0
                game_won = False
                game_over = False
                print("Game started!")

                # Create window
                cv2.namedWindow("VIVA SERGIPE!", cv2.WINDOW_NORMAL)
                cv2.setWindowProperty("VIVA SERGIPE!", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            elif action == "hide_game":
                game_visible = False
                cv2.destroyAllWindows()

            elif action == "exit":
                break

        except queue.Empty:
            pass

        if not game_visible:
            time.sleep(0.1)
            continue

        # Game loop
        success, frame = capture.read()
        if not success:
            continue

        # Process frame
        results, frame = process_frame(frame, pose)
        frame = cv2.flip(frame, 1)

        # Get screen size and resize
        screen_width = 1920
        screen_height = 1080
        frame = cv2.resize(frame, (screen_width, screen_height))

        # Resize contour mask
        frame_height, frame_width = frame.shape[:2]
        contour_resized = cv2.resize(contour_mask, (frame_width, frame_height))

        if game_started and not game_over and not game_won:
            # Calculate time left
            elapsed_time = time.time() - start_time
            time_left = max(0, GAME_SETTINGS['duration'] - elapsed_time)

            # Create body mask
            body_mask = create_body_mask(results, frame_width, frame_height)
            body_pixels = np.sum(body_mask > 0)

            # Show body overlay
            if body_pixels > 0:
                body_overlay = np.zeros_like(frame)
                body_overlay[:, :, 0] = body_mask
                frame = cv2.addWeighted(frame, 0.8, body_overlay, 0.2, 0)

            # Calculate fill percentage
            if body_pixels >= GAME_SETTINGS['min_body_pixels']:
                fill_percentage = calculate_fill_percentage(body_mask, contour_resized)

                # Check win condition
                if fill_percentage >= GAME_SETTINGS['win_threshold']:
                    game_won = True
                    if victory_sound:
                        victory_sound.play()
                    save_victory_photo(frame, SNAPSHOTS_DIR, fill_percentage)
            else:
                if body_pixels == 0:
                    fill_percentage = 0.0

            # Check game over
            if time_left <= 0:
                game_over = True
                if game_over_sound:
                    game_over_sound.play()

        # Display interface
        if game_won:
            display_victory_message(frame, fill_percentage)
        elif game_over:
            display_game_over_message(frame, fill_percentage)
        else:
            display_sergipe_interface(
                frame, contour_resized,
                GAME_SETTINGS['duration'] - (time.time() - start_time) if start_time else GAME_SETTINGS['duration'],
                fill_percentage, game_started, GAME_SETTINGS['win_threshold']
            )

        # Show frame
        if game_visible:
            cv2.imshow("VIVA SERGIPE!", frame)

        # Handle keys - apenas teclas permitidas
        key = cv2.waitKey(5) & 0xFF

        # Lista de teclas permitidas (códigos ASCII e especiais)
        allowed_keys = [
            27,    # ESC
            81,    # Q maiúsculo
            113,   # q minúsculo
            0,     # Nenhuma tecla
            255    # Nenhuma tecla (máscara)
        ]

        # Verificar se a tecla é permitida
        if key != 255 and key != 0 and key not in allowed_keys:
            # Bloquear tecla - não fazer nada
            continue

        # Processar teclas permitidas
        if key == ord('q') or key == ord('Q') or key == 27:  # Q or ESC
            game_over = True

        # Check if game ended
        if (game_won or game_over) and game_started:
            # Show final screen for a few seconds
            final_screen_start = time.time()
            while time.time() - final_screen_start < 3.0:
                # Keep showing the final screen
                if game_visible:
                    cv2.imshow("VIVA SERGIPE!", frame)
                    key = cv2.waitKey(100) & 0xFF
                    if key == ord('q') or key == 27:
                        break

            # Send result
            result = {
                "won": game_won,
                "fill_percentage": fill_percentage
            }
            result_queue.put(result)
            print(f"Game ended - Won: {game_won}, Fill: {fill_percentage:.1f}%")

            # Hide game
            game_visible = False
            game_started = False
            cv2.destroyAllWindows()

    # Cleanup
    capture.release()
    cv2.destroyAllWindows()
    pygame.quit()
