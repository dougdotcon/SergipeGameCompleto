"""
Teste simples para verificar se as funções do jogo Sergipe estão funcionando
"""

import cv2
import numpy as np
from sergipe_utils import load_sergipe_contour, create_body_mask, calculate_fill_percentage

def test_contour_loading():
    """Testa o carregamento do contorno de Sergipe"""
    print("Testando carregamento do contorno...")
    
    contour_mask = load_sergipe_contour("assets/contorno-mapa-SE.png")
    
    if contour_mask is not None:
        print(f"✓ Contorno carregado com sucesso! Shape: {contour_mask.shape}")
        print(f"✓ Pixels do contorno: {np.sum(contour_mask > 0)}")
        return True
    else:
        print("✗ Erro ao carregar contorno")
        return False

def test_body_mask():
    """Testa a criação de máscara corporal simulada"""
    print("\nTestando criação de máscara corporal...")
    
    # Simular resultados do MediaPipe (sem landmarks reais)
    class MockResults:
        def __init__(self):
            self.pose_landmarks = None
    
    results = MockResults()
    
    # Teste sem landmarks
    mask = create_body_mask(results, 640, 480)
    print(f"✓ Máscara sem landmarks criada. Shape: {mask.shape}")
    print(f"✓ Pixels da máscara: {np.sum(mask > 0)}")
    
    return True

def test_fill_calculation():
    """Testa o cálculo de preenchimento"""
    print("\nTestando cálculo de preenchimento...")
    
    # Criar máscaras de teste
    contour = np.zeros((100, 100), dtype=np.uint8)
    cv2.rectangle(contour, (25, 25), (75, 75), 255, -1)  # Quadrado branco
    
    body = np.zeros((100, 100), dtype=np.uint8)
    cv2.rectangle(body, (30, 30), (70, 70), 255, -1)  # Quadrado menor
    
    percentage = calculate_fill_percentage(body, contour)
    print(f"✓ Percentual calculado: {percentage:.2f}%")
    
    # Teste com sobreposição total
    body_full = contour.copy()
    percentage_full = calculate_fill_percentage(body_full, contour)
    print(f"✓ Percentual com sobreposição total: {percentage_full:.2f}%")
    
    return True

def main():
    """Executa todos os testes"""
    print("=== TESTE DO JOGO VIVA SERGIPE! ===\n")
    
    tests = [
        test_contour_loading,
        test_body_mask,
        test_fill_calculation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Erro no teste: {e}")
    
    print(f"\n=== RESULTADO ===")
    print(f"Testes passaram: {passed}/{total}")
    
    if passed == total:
        print("✓ Todos os testes passaram! O jogo deve funcionar corretamente.")
        print("\nPara jogar, execute: python sergipe_game.py")
        print("Controles:")
        print("- SPACE: Iniciar/Reiniciar jogo")
        print("- Q ou ESC: Sair")
        print("- R: Reiniciar aplicação")
    else:
        print("✗ Alguns testes falharam. Verifique os erros acima.")

if __name__ == "__main__":
    main()
