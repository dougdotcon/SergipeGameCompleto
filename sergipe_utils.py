"""
SERGIPE GAME UTILITY FUNCTIONS
Funções específicas para o jogo "Viva Sergipe!"
Adaptado da base do projeto STRIKE A POSE!
"""

##############
### IMPORT ###
##############

import cv2
import numpy as np
import os
import time
from datetime import datetime
import mediapipe as mp

# Import MediaPipe solutions
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Import from utils.py
from utils import draw_bold_text

##################
### FUNCTIONS ###
##################

def load_sergipe_contour(contour_path="assets/sergipe_contour.npy"):
    """
    Loads the Sergipe map contour from image file and converts to binary mask.

    Args:
        contour_path (str): Path to the contour image file

    Returns:
        numpy.ndarray: Binary mask of the contour (255 for contour, 0 for background)
        None if file cannot be loaded
    """
    try:
        # Load image
        contour_img = cv2.imread(contour_path, cv2.IMREAD_GRAYSCALE)

        if contour_img is None:
            print(f"Error: Could not load contour image from {contour_path}")
            return None

        print(f"Contour image loaded: {contour_img.shape}, values: {np.min(contour_img)}-{np.max(contour_img)}")

        # The image has very low values, so we need a different approach
        # Find any non-zero pixels and make them white
        binary_mask = np.zeros_like(contour_img)
        binary_mask[contour_img > 0] = 255

        # If still no contour found, try a very low threshold
        if np.sum(binary_mask) == 0:
            _, binary_mask = cv2.threshold(contour_img, 1, 255, cv2.THRESH_BINARY)

        print(f"Binary mask created: {np.sum(binary_mask > 0)} white pixels")

        return binary_mask

    except Exception as e:
        print(f"Error loading contour: {e}")
        return None


def create_body_mask(results, frame_width, frame_height):
    """
    Creates a binary mask of the detected body from MediaPipe pose landmarks.

    Args:
        results: MediaPipe pose detection results
        frame_width (int): Width of the frame
        frame_height (int): Height of the frame

    Returns:
        numpy.ndarray: Binary mask of the body silhouette
    """
    # Create empty mask
    mask = np.zeros((frame_height, frame_width), dtype=np.uint8)

    if results.pose_landmarks:
        # Get landmark points
        landmarks = results.pose_landmarks.landmark

        # Convert normalized coordinates to pixel coordinates
        points = []
        for landmark in landmarks:
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            # Only add points that are visible and within frame
            if (0 <= x < frame_width and 0 <= y < frame_height and
                landmark.visibility > 0.5):  # Only use visible landmarks
                points.append([x, y])

        print(f"Body detection: {len(points)} valid landmarks found")

        if len(points) > 3:  # Need at least 3 points for convex hull
            points = np.array(points, dtype=np.int32)
            hull = cv2.convexHull(points)
            cv2.fillPoly(mask, [hull], 255)

            # Also draw circles around key body parts for better coverage
            for point in points:
                cv2.circle(mask, tuple(point), 30, 255, -1)  # 30px radius circles

            print(f"Body mask created: {np.sum(mask > 0)} pixels")
        else:
            print("Not enough visible landmarks for body detection")
    else:
        print("No pose landmarks detected")

    return mask


def calculate_fill_percentage(body_mask, contour_mask):
    """
    Calculates the percentage of contour area filled by the body.

    Args:
        body_mask (numpy.ndarray): Binary mask of the body
        contour_mask (numpy.ndarray): Binary mask of the contour

    Returns:
        float: Percentage of contour filled (0-100)
    """
    # Ensure masks are the same size
    if body_mask.shape != contour_mask.shape:
        body_mask = cv2.resize(body_mask, (contour_mask.shape[1], contour_mask.shape[0]))

    # Calculate intersection (overlap between body and contour)
    intersection = cv2.bitwise_and(body_mask, contour_mask)

    # Count pixels
    contour_pixels = np.sum(contour_mask > 0)
    intersection_pixels = np.sum(intersection > 0)
    body_pixels = np.sum(body_mask > 0)

    # Debug information
    print(f"Fill calculation: Contour={contour_pixels}, Body={body_pixels}, Intersection={intersection_pixels}")

    # Calculate percentage
    if contour_pixels > 0:
        percentage = (intersection_pixels / contour_pixels) * 100.0
        print(f"Fill percentage: {percentage:.2f}%")
        return min(percentage, 100.0)  # Cap at 100%
    else:
        print("No contour pixels found!")
        return 0.0


def save_victory_photo(frame, snapshots_dir, fill_percentage):
    """
    Saves a victory photo when the player wins.

    Args:
        frame (numpy.ndarray): Current video frame
        snapshots_dir (str): Directory to save the photo
        fill_percentage (float): Final fill percentage achieved
    """
    try:
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vitoria_sergipe_{timestamp}_{fill_percentage:.1f}pct.jpg"
        filepath = os.path.join(snapshots_dir, filename)

        # Add victory text overlay to the frame
        victory_frame = frame.copy()
        draw_bold_text(
            victory_frame,
            "🎉 VIVA SERGIPE! 🎉",
            (200, 100),
            font_scale=2,
            color=(0, 255, 0),  # Green
            thickness=3
        )

        draw_bold_text(
            victory_frame,
            f"Preenchimento: {fill_percentage:.1f}%",
            (300, 200),
            font_scale=1.5,
            color=(255, 255, 255),  # White
            thickness=2
        )

        # Save the photo
        cv2.imwrite(filepath, victory_frame)
        print(f"Victory photo saved: {filepath}")

    except Exception as e:
        print(f"Error saving victory photo: {e}")


def display_sergipe_interface(frame, contour_mask, time_left, fill_percentage, game_started, win_threshold=30):
    """
    Displays the main game interface with contour, timer, and progress.

    Args:
        frame (numpy.ndarray): Current video frame
        contour_mask (numpy.ndarray): Sergipe contour mask
        time_left (float): Time remaining in seconds
        fill_percentage (float): Current fill percentage
        game_started (bool): Whether the game has started
        win_threshold (float): Win threshold percentage
    """
    # Make contour more visible
    # Create colored contour overlay with stronger visibility
    contour_overlay = np.zeros_like(frame)

    # Make contour bright green and more visible
    contour_overlay[:, :, 1] = contour_mask  # Green channel
    contour_overlay[:, :, 0] = contour_mask // 2  # Some blue for cyan effect

    # Also draw contour outline for better visibility
    contours, _ = cv2.findContours(contour_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)  # Green outline

    # Blend contour with frame (more visible)
    alpha = 0.4  # Increased transparency for better visibility
    frame_with_contour = cv2.addWeighted(frame, 1 - alpha, contour_overlay, alpha, 0)
    frame[:] = frame_with_contour

    if not game_started:
        # Start screen with improved text formatting
        draw_bold_text(
            frame,
            "VIVA SERGIPE!",
            (400, 150),
            font_scale=3.5,
            color=(0, 255, 0),  # Green
            thickness=6,
            outline_color=(0, 0, 0),  # Black outline
            outline_thickness=12
        )

        draw_bold_text(
            frame,
            "Preencha o mapa com seu corpo!",
            (250, 250),
            font_scale=1.8,
            color=(255, 255, 255),  # White
            thickness=4,
            outline_color=(0, 0, 0),  # Black outline
            outline_thickness=8
        )

        minutes = int(time_left // 60) if time_left > 0 else 5
        draw_bold_text(
            frame,
            f"Meta: {win_threshold:.0f}% em {minutes} minutos",
            (350, 350),
            font_scale=1.5,
            color=(255, 255, 0),  # Yellow
            thickness=3,
            outline_color=(0, 0, 0),  # Black outline
            outline_thickness=7
        )

        # Removed start instruction - game starts automatically

        # Additional controls info with better visibility
        draw_bold_text(
            frame,
            "F11: Tela cheia | Q/ESC: Sair",
            (300, 600),
            font_scale=1.2,
            color=(255, 255, 255),  # White
            thickness=2,
            outline_color=(0, 0, 0),  # Black outline
            outline_thickness=6
        )
    else:
        # Game interface during play with improved text formatting
        # Timer display
        minutes = int(time_left // 60)
        seconds = int(time_left % 60)
        timer_text = f"Tempo: {minutes:02d}:{seconds:02d}"

        # Color timer based on remaining time
        if time_left > 60:
            timer_color = (0, 255, 0)  # Green
        elif time_left > 30:
            timer_color = (0, 255, 255)  # Yellow
        else:
            timer_color = (0, 0, 255)  # Red

        draw_bold_text(
            frame,
            timer_text,
            (50, 80),
            font_scale=2.0,
            color=timer_color,
            thickness=4,
            outline_color=(0, 0, 0),  # Black outline
            outline_thickness=8
        )

        # Fill percentage display with better formatting
        percentage_text = f"Preenchimento: {fill_percentage:.1f}%"

        # Color percentage based on progress
        if fill_percentage >= win_threshold:
            percentage_color = (0, 255, 0)  # Green
        elif fill_percentage >= win_threshold * 0.5:
            percentage_color = (0, 255, 255)  # Yellow
        else:
            percentage_color = (255, 255, 255)  # White

        draw_bold_text(
            frame,
            percentage_text,
            (50, 150),
            font_scale=1.8,
            color=percentage_color,
            thickness=4,
            outline_color=(0, 0, 0),  # Black outline
            outline_thickness=8
        )

        # Progress bar with better visibility
        bar_x, bar_y = 50, 180
        bar_width, bar_height = 400, 25

        # Background bar with border
        cv2.rectangle(frame, (bar_x-2, bar_y-2), (bar_x + bar_width+2, bar_y + bar_height+2), (255, 255, 255), 2)
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)

        # Progress bar
        progress_width = int((fill_percentage / 100.0) * bar_width)
        if progress_width > 0:
            # Gradient effect for progress bar
            if fill_percentage >= win_threshold:
                progress_color = (0, 255, 0)  # Green
            elif fill_percentage >= win_threshold * 0.5:
                progress_color = (0, 255, 255)  # Yellow
            else:
                progress_color = (255, 100, 100)  # Light blue

            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), progress_color, -1)

        # Goal line at win_threshold%
        goal_x = bar_x + int((win_threshold / 100.0) * bar_width)
        cv2.line(frame, (goal_x, bar_y - 10), (goal_x, bar_y + bar_height + 10), (0, 0, 255), 3)

        # Goal text
        draw_bold_text(
            frame,
            f"Meta: {win_threshold:.0f}%",
            (goal_x - 50, bar_y - 20),
            font_scale=0.8,
            color=(255, 255, 255),
            thickness=2,
            outline_color=(0, 0, 0),
            outline_thickness=4
        )


def display_main_menu(frame, selected_option):
    """
    Displays the main menu with options.

    Args:
        frame (numpy.ndarray): Current video frame
        selected_option (int): Currently selected menu option
    """
    # Semi-transparent overlay
    overlay = np.zeros_like(frame)
    overlay[:] = (20, 20, 20)  # Dark background
    alpha = 0.8
    frame[:] = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)

    # Title
    draw_bold_text(
        frame,
        "VIVA SERGIPE!",
        (400, 150),
        font_scale=4,
        color=(0, 255, 0),  # Green
        thickness=5
    )

    draw_bold_text(
        frame,
        "Jogo de Preenchimento Corporal",
        (300, 220),
        font_scale=1.5,
        color=(255, 255, 255),  # White
        thickness=2
    )

    # Menu options
    menu_options = [
        "1. JOGAR",
        "2. CONFIGURAÇÕES",
        "3. SAIR"
    ]

    start_y = 350
    for i, option in enumerate(menu_options):
        color = (0, 255, 255) if i == selected_option else (255, 255, 255)  # Yellow if selected
        thickness = 3 if i == selected_option else 2

        draw_bold_text(
            frame,
            option,
            (450, start_y + i * 80),
            font_scale=2,
            color=color,
            thickness=thickness
        )

    # Instructions
    draw_bold_text(
        frame,
        "Use ↑↓ para navegar | ENTER para selecionar",
        (250, 650),
        font_scale=1.2,
        color=(200, 200, 200),  # Light gray
        thickness=1
    )


def display_config_menu(frame, config_option, game_settings):
    """
    Displays the configuration menu.

    Args:
        frame (numpy.ndarray): Current video frame
        config_option (int): Currently selected config option
        game_settings (dict): Current game settings
    """
    # Semi-transparent overlay
    overlay = np.zeros_like(frame)
    overlay[:] = (20, 20, 40)  # Dark blue background
    alpha = 0.8
    frame[:] = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)

    # Title
    draw_bold_text(
        frame,
        "CONFIGURAÇÕES",
        (400, 100),
        font_scale=3,
        color=(0, 255, 255),  # Cyan
        thickness=4
    )

    # Configuration options
    config_items = [
        f"Duração do Jogo: {game_settings['duration']//60}:{game_settings['duration']%60:02d}",
        f"Meta de Preenchimento: {game_settings['win_threshold']:.0f}%",
        f"Sensibilidade Corporal: {game_settings['min_body_pixels']}",
        "VOLTAR"
    ]

    start_y = 250
    for i, item in enumerate(config_items):
        color = (255, 255, 0) if i == config_option else (255, 255, 255)  # Yellow if selected
        thickness = 3 if i == config_option else 2

        draw_bold_text(
            frame,
            item,
            (200, start_y + i * 80),
            font_scale=1.8,
            color=color,
            thickness=thickness
        )

        # Show adjustment hints for selected option
        if i == config_option and i < 3:  # Not the "VOLTAR" option
            draw_bold_text(
                frame,
                "← → para ajustar",
                (800, start_y + i * 80),
                font_scale=1,
                color=(200, 200, 200),
                thickness=1
            )

    # Instructions
    draw_bold_text(
        frame,
        "↑↓: Navegar | ←→: Ajustar | ENTER: Confirmar | ESC: Voltar",
        (150, 650),
        font_scale=1.2,
        color=(200, 200, 200),
        thickness=1
    )


def display_game_interface_updated(frame, contour_mask, time_left, fill_percentage, game_started, win_threshold=30, countdown_started=False):
    """
    Updated game interface that works with the menu system.
    """
    display_sergipe_interface(frame, contour_mask, time_left, fill_percentage, game_started, win_threshold, countdown_started)


# Keep the original display_sergipe_interface but fix the indentation issue
def display_sergipe_interface_original(frame, contour_mask, time_left, fill_percentage, game_started):
    """
    Original interface function - keeping for reference
    """
    if not game_started:
        # Game interface
        # Timer
        minutes = int(time_left // 60)
        seconds = int(time_left % 60)
        timer_text = f"Tempo: {minutes:02d}:{seconds:02d}"

        # Color timer based on remaining time
        if time_left > 60:
            timer_color = (0, 255, 0)  # Green
        elif time_left > 30:
            timer_color = (0, 255, 255)  # Yellow
        else:
            timer_color = (0, 0, 255)  # Red

        draw_bold_text(
            frame,
            timer_text,
            (50, 50),
            font_scale=1.5,
            color=timer_color,
            thickness=2
        )

        # Fill percentage
        percentage_text = f"Preenchimento: {fill_percentage:.1f}%"

        # Color percentage based on progress
        if fill_percentage >= 30:
            percentage_color = (0, 255, 0)  # Green
        elif fill_percentage >= 15:
            percentage_color = (0, 255, 255)  # Yellow
        else:
            percentage_color = (255, 255, 255)  # White

        draw_bold_text(
            frame,
            percentage_text,
            (50, 100),
            font_scale=1.2,
            color=percentage_color,
            thickness=2
        )

        # Progress bar
        bar_x, bar_y = 50, 130
        bar_width, bar_height = 300, 20

        # Background bar
        cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (100, 100, 100), -1)

        # Progress bar
        progress_width = int((fill_percentage / 100.0) * bar_width)
        if progress_width > 0:
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), (0, 255, 0), -1)

        # Goal line at 30%
        goal_x = bar_x + int(0.30 * bar_width)
        cv2.line(frame, (goal_x, bar_y - 5), (goal_x, bar_y + bar_height + 5), (0, 0, 255), 2)


def display_victory_message(frame, fill_percentage):
    """
    Displays victory message when player wins.

    Args:
        frame (numpy.ndarray): Current video frame
        fill_percentage (float): Final fill percentage achieved
    """
    # Semi-transparent overlay
    overlay = np.zeros_like(frame)
    overlay[:] = (0, 255, 0)  # Green
    alpha = 0.3
    frame[:] = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)

    # Victory messages
    draw_bold_text(
        frame,
        "🎉 VIVA SERGIPE! 🎉",
        (200, 200),
        font_scale=3,
        color=(255, 255, 255),  # White
        thickness=4
    )

    draw_bold_text(
        frame,
        f"Parabéns! {fill_percentage:.1f}% preenchido!",
        (250, 300),
        font_scale=1.8,
        color=(255, 255, 255),  # White
        thickness=3
    )

    draw_bold_text(
        frame,
        "Foto salva! 📸",
        (400, 400),
        font_scale=1.5,
        color=(255, 255, 0),  # Yellow
        thickness=2
    )

    # Restart instructions
    if int(time.time() * 2) % 2 == 0:
        draw_bold_text(
            frame,
            "",
            (200, 500),
            font_scale=1.2,
            color=(0, 0, 255),  # Red
            thickness=2
        )


def display_game_over_message(frame, fill_percentage):
    """
    Displays game over message when time runs out.

    Args:
        frame (numpy.ndarray): Current video frame
        fill_percentage (float): Final fill percentage achieved
    """
    # Semi-transparent overlay
    overlay = np.zeros_like(frame)
    overlay[:] = (0, 0, 255)  # Red
    alpha = 0.3
    frame[:] = cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)

    # Game over messages
    draw_bold_text(
        frame,
        "GAME OVER",
        (350, 200),
        font_scale=3,
        color=(255, 255, 255),  # White
        thickness=4
    )

    draw_bold_text(
        frame,
        f"Preenchimento final: {fill_percentage:.1f}%",
        (250, 300),
        font_scale=1.5,
        color=(255, 255, 255),  # White
        thickness=2
    )

    if fill_percentage >= 50:
        message = "Bom trabalho! Tente novamente!"
    else:
        message = "Continue tentando!"

    draw_bold_text(
        frame,
        message,
        (300, 400),
        font_scale=1.2,
        color=(255, 255, 0),  # Yellow
        thickness=2
    )

    # Restart instructions
    if int(time.time() * 2) % 2 == 0:
        draw_bold_text(
            frame,
            "SPACE: Jogar novamente | Q: Sair",
            (200, 500),
            font_scale=1.2,
            color=(0, 0, 255),  # Red
            thickness=2
        )
