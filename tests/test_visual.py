"""
Teste visual para verificar se o contorno de Sergipe está aparecendo corretamente
"""

import cv2
import numpy as np
from sergipe_utils import load_sergipe_contour

def test_contour_visualization():
    """Testa a visualização do contorno"""
    print("Carregando contorno de Sergipe...")
    
    # Carregar contorno
    contour_mask = load_sergipe_contour("assets/contorno-mapa-SE.png")
    
    if contour_mask is None:
        print("Erro: Não foi possível carregar o contorno")
        return
    
    # Criar uma imagem de teste (simulando webcam)
    test_frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    test_frame[:] = (50, 50, 50)  # Fundo cinza escuro
    
    # Redimensionar contorno para o tamanho do frame
    contour_resized = cv2.resize(contour_mask, (1280, 720))
    
    # Criar overlay do contorno
    contour_overlay = np.zeros_like(test_frame)
    contour_overlay[:, :, 1] = contour_resized  # Canal verde
    contour_overlay[:, :, 0] = contour_resized // 2  # Um pouco de azul
    
    # Desenhar contorno como linha
    contours, _ = cv2.findContours(contour_resized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        cv2.drawContours(test_frame, [contour], -1, (0, 255, 0), 3)  # Linha verde
    
    # Misturar com o frame
    alpha = 0.4
    result = cv2.addWeighted(test_frame, 1 - alpha, contour_overlay, alpha, 0)
    
    # Adicionar texto informativo
    cv2.putText(result, "CONTORNO DE SERGIPE - TESTE VISUAL", (50, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(result, f"Pixels do contorno: {np.sum(contour_resized > 0)}", (50, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(result, "Pressione qualquer tecla para fechar", (50, 150), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Mostrar resultado
    cv2.imshow("Teste Visual - Contorno Sergipe", result)
    print("Janela aberta. Pressione qualquer tecla para fechar.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print("Teste visual concluído!")

if __name__ == "__main__":
    test_contour_visualization()
