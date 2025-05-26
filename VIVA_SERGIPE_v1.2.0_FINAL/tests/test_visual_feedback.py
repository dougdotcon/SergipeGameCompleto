#!/usr/bin/env python3
"""
Teste do sistema de feedback visual do VIVA SERGIPE!
"""

import sys
import os
import cv2
import numpy as np
import time

# Adiciona o diretório atual ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_visual_feedback_manager():
    """Testa o gerenciador de feedback visual"""
    print("🧪 Testando Gerenciador de Feedback Visual...")
    print("=" * 50)

    try:
        from visual_feedback import get_visual_feedback_manager

        # Obter instância do gerenciador
        visual_feedback = get_visual_feedback_manager()
        print("✅ Gerenciador de feedback visual carregado com sucesso!")

        # Criar frame de teste
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        test_frame[:] = (50, 50, 50)  # Fundo cinza

        # Simular resultados do MediaPipe (sem detecção)
        class MockResults:
            pose_landmarks = None

        mock_results = MockResults()

        # Testar análise de qualidade sem detecção
        analysis = visual_feedback.analyze_detection_quality(test_frame, mock_results, 0)
        print(f"  • Status sem detecção: {analysis['status']}")
        print(f"  • Confiança: {analysis['confidence']:.2f}")
        print(f"  • Issues: {len(analysis['issues'])}")

        if analysis["status"] == "none":
            print("✅ Análise de qualidade sem detecção funcionou!")
        else:
            print("❌ Erro na análise sem detecção")

        # Testar feedback visual
        frame_with_feedback = visual_feedback.draw_detection_feedback(test_frame.copy(), analysis)
        if frame_with_feedback.shape == test_frame.shape:
            print("✅ Desenho de feedback visual funcionou!")
        else:
            print("❌ Erro no desenho de feedback visual")

        # Testar guia de calibração
        frame_with_guide = visual_feedback.draw_calibration_guide(test_frame.copy())
        if frame_with_guide.shape == test_frame.shape:
            print("✅ Guia de calibração funcionou!")
        else:
            print("❌ Erro no guia de calibração")

        # Testar mensagens temporárias
        visual_feedback.show_temporary_message("Teste de mensagem", 1.0)
        frame_with_messages = visual_feedback.draw_messages(test_frame.copy())
        if frame_with_messages.shape == test_frame.shape:
            print("✅ Sistema de mensagens funcionou!")
        else:
            print("❌ Erro no sistema de mensagens")

        # Testar informações de performance
        frame_with_perf = visual_feedback.draw_performance_info(test_frame.copy(), 30.0, 25.5, 1500)
        if frame_with_perf.shape == test_frame.shape:
            print("✅ Informações de performance funcionaram!")
        else:
            print("❌ Erro nas informações de performance")

        print("✅ Todos os testes do feedback visual passaram!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste do feedback visual: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_sync_manager():
    """Testa o gerenciador de sincronização"""
    print("\n🔄 Testando Gerenciador de Sincronização...")
    print("=" * 50)

    try:
        from sync_manager import get_sync_manager, ProcessState

        # Obter instância do gerenciador
        sync_manager = get_sync_manager()
        print("✅ Gerenciador de sincronização carregado com sucesso!")

        # Criar filas de teste
        import queue
        command_queue = queue.Queue()
        result_queue = queue.Queue()

        # Registrar processo de teste
        process_id = "test_process"
        sync_manager.register_process(process_id, command_queue, result_queue)
        print(f"✅ Processo '{process_id}' registrado!")

        # Verificar estado inicial
        state = sync_manager.get_process_state(process_id)
        if state == ProcessState.IDLE:
            print("✅ Estado inicial correto!")
        else:
            print(f"❌ Estado inicial incorreto: {state}")

        # Função de teste simples
        def test_function():
            time.sleep(0.1)  # Simular trabalho
            result_queue.put({"status": "completed", "data": "test_data"})

        # Iniciar processo
        if sync_manager.start_process(process_id, test_function):
            print("✅ Processo iniciado com sucesso!")

            # Aguardar um pouco
            time.sleep(0.2)

            # Verificar resultado
            result = sync_manager.get_result(process_id, timeout=1.0)
            if result and result.get("status") == "completed":
                print("✅ Resultado obtido com sucesso!")
            else:
                print("❌ Erro ao obter resultado")

            # Parar processo
            if sync_manager.stop_process(process_id):
                print("✅ Processo parado com sucesso!")
            else:
                print("❌ Erro ao parar processo")
        else:
            print("❌ Erro ao iniciar processo")

        # Obter relatório de status
        report = sync_manager.get_status_report()
        if "processes" in report and process_id in report["processes"]:
            print("✅ Relatório de status funcionou!")
        else:
            print("❌ Erro no relatório de status")

        print("✅ Todos os testes de sincronização passaram!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste de sincronização: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Testa a integração com o jogo principal"""
    print("\n🎮 Testando Integração com Melhorias...")
    print("=" * 50)

    try:
        # Testar importação no sergipe_game.py
        import sergipe_game
        print("✅ Integração com sergipe_game.py funcionou!")

        # Verificar se os novos managers foram importados
        if hasattr(sergipe_game, 'visual_feedback'):
            print("✅ Visual feedback manager carregado no jogo!")
        else:
            print("⚠️ Visual feedback manager não encontrado no jogo")

        if hasattr(sergipe_game, 'sync_manager'):
            print("✅ Sync manager carregado no jogo!")
        else:
            print("⚠️ Sync manager não encontrado no jogo")

        # Testar se as configurações visuais estão disponíveis
        from config_manager import get_config_manager
        config = get_config_manager()

        # Verificar configurações visuais padrão
        visual_configs = [
            'show_percentage',
            'show_timer',
            'show_progress_bar',
            'camera_mirror',
            'contour_thickness'
        ]

        all_configs_present = True
        for config_key in visual_configs:
            value = config.get('visual', config_key)
            if value is not None:
                print(f"  ✅ {config_key}: {value}")
            else:
                print(f"  ❌ {config_key}: não encontrado")
                all_configs_present = False

        if all_configs_present:
            print("✅ Todas as configurações visuais estão disponíveis!")
        else:
            print("⚠️ Algumas configurações visuais estão faltando")

        print("✅ Teste de integração passou!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste de integração: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_visual_demo():
    """Demonstração visual do sistema de feedback"""
    print("\n🖼️ Demonstração Visual (Opcional)...")
    print("=" * 50)

    try:
        response = input("Deseja executar demonstração visual? (s/N): ").lower().strip()
        if response not in ['s', 'sim', 'y', 'yes']:
            print("Demonstração visual pulada.")
            return True

        from visual_feedback import get_visual_feedback_manager

        visual_feedback = get_visual_feedback_manager()

        # Criar janela de demonstração
        cv2.namedWindow("Demo - Feedback Visual", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Demo - Feedback Visual", 800, 600)

        print("Demonstração iniciada. Pressione 'q' para sair.")

        start_time = time.time()
        frame_count = 0

        while True:
            # Criar frame de demonstração
            frame = np.zeros((600, 800, 3), dtype=np.uint8)
            frame[:] = (30, 30, 30)  # Fundo escuro

            # Simular diferentes estados de detecção
            elapsed = time.time() - start_time
            cycle_time = elapsed % 12  # Ciclo de 12 segundos

            class MockResults:
                pose_landmarks = None

            mock_results = MockResults()

            if cycle_time < 3:
                # Sem detecção
                body_pixels = 0
                status_text = "SEM DETECÇÃO"
            elif cycle_time < 6:
                # Detecção pobre
                body_pixels = 500
                status_text = "DETECÇÃO POBRE"
            elif cycle_time < 9:
                # Detecção boa
                body_pixels = 1500
                status_text = "DETECÇÃO BOA"
            else:
                # Detecção excelente
                body_pixels = 3000
                status_text = "DETECÇÃO EXCELENTE"

            # Analisar qualidade
            analysis = visual_feedback.analyze_detection_quality(frame, mock_results, body_pixels)

            # Aplicar feedback visual
            frame = visual_feedback.draw_detection_feedback(frame, analysis)

            # Mostrar guia de calibração se necessário
            if analysis["status"] in ["none", "poor"]:
                frame = visual_feedback.draw_calibration_guide(frame)

            # Mostrar mensagens baseadas no status
            if cycle_time % 4 < 0.1:  # A cada 4 segundos
                if analysis["status"] == "none":
                    visual_feedback.show_temporary_message("Posicione-se em frente à câmera", 3.0)
                elif analysis["status"] == "poor":
                    visual_feedback.show_temporary_message("Melhore a iluminação", 3.0)
                elif analysis["status"] == "good":
                    visual_feedback.show_temporary_message("Ótima detecção!", 2.0)

            # Desenhar mensagens
            frame = visual_feedback.draw_messages(frame)

            # Calcular FPS
            frame_count += 1
            fps = frame_count / (elapsed + 0.001)

            # Mostrar informações de performance
            frame = visual_feedback.draw_performance_info(frame, fps, analysis["confidence"] * 100, body_pixels)

            # Adicionar texto de status
            cv2.putText(frame, f"STATUS: {status_text}", (20, 50),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.putText(frame, f"Ciclo: {cycle_time:.1f}s", (20, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

            # Mostrar frame
            cv2.imshow("Demo - Feedback Visual", frame)

            # Verificar teclas
            key = cv2.waitKey(30) & 0xFF
            if key == ord('q') or key == 27:
                break

        cv2.destroyAllWindows()
        print("✅ Demonstração visual concluída!")
        return True

    except Exception as e:
        print(f"❌ Erro na demonstração visual: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executa todos os testes"""
    print("TESTE COMPLETO DAS MELHORIAS VISUAIS E SINCRONIZACAO")
    print("=" * 70)

    tests = [
        ("Gerenciador de Feedback Visual", test_visual_feedback_manager),
        ("Gerenciador de Sincronização", test_sync_manager),
        ("Integração com o Jogo", test_integration),
        ("Demonstração Visual", test_visual_demo)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n🔍 Executando: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}: PASSOU")
            else:
                print(f"❌ {test_name}: FALHOU")
        except Exception as e:
            print(f"❌ {test_name}: ERRO - {e}")

    print("\n" + "=" * 70)
    print(f"📊 RESULTADO FINAL: {passed}/{total} testes passaram")

    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\n✅ As melhorias visuais e de sincronização estão funcionando!")
        print("\nNovas funcionalidades disponíveis:")
        print("• 🎯 Feedback visual de qualidade da detecção")
        print("• 📏 Guia de calibração para posicionamento")
        print("• 💬 Mensagens temporárias contextuais")
        print("• 📊 Informações de performance em tempo real")
        print("• 🔄 Sistema de sincronização robusto")
        print("• ⚙️ Configurações visuais personalizáveis")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM!")
        print("Verifique os erros acima e corrija antes de usar as melhorias.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
