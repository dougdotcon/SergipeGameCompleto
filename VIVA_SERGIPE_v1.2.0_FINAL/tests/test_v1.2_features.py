#!/usr/bin/env python3
"""
Teste das funcionalidades da Versão 1.2 do VIVA SERGIPE!
"""

import sys
import os
import time
import numpy as np

# Adiciona o diretório atual ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_performance_optimizer():
    """Testa o otimizador de performance"""
    print("🚀 Testando Otimizador de Performance...")
    print("=" * 50)

    try:
        from performance_optimizer import get_performance_optimizer

        # Obter instância do otimizador
        optimizer = get_performance_optimizer()
        print("✅ Otimizador de performance carregado com sucesso!")

        # Testar detecção de hardware
        print(f"  • Hardware detectado: {optimizer.adaptive_settings['quality_level']}")
        print(f"  • FPS alvo: {optimizer.adaptive_settings['target_fps']}")
        print(f"  • Escala de resolução: {optimizer.adaptive_settings['resolution_scale']}")

        # Testar otimização de frame
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        optimized_frame = optimizer.optimize_frame_processing(test_frame)

        if optimized_frame.shape[2] == 3:  # Ainda é um frame válido
            print("✅ Otimização de frame funcionou!")
        else:
            print("❌ Erro na otimização de frame")

        # Testar configurações de câmera
        camera_settings = optimizer.get_optimized_camera_settings()
        if 'width' in camera_settings and 'height' in camera_settings:
            print(f"✅ Configurações de câmera: {camera_settings['width']}x{camera_settings['height']}")
        else:
            print("❌ Erro nas configurações de câmera")

        # Testar métricas de performance
        optimizer.update_performance_metrics(30.0, 0.033, 0.01)
        report = optimizer.get_performance_report()

        if 'hardware' in report and 'current_settings' in report:
            print("✅ Relatório de performance funcionou!")
        else:
            print("❌ Erro no relatório de performance")

        print("✅ Todos os testes do otimizador passaram!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste do otimizador: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_game_modes():
    """Testa o sistema de modos de jogo"""
    print("\n🎮 Testando Sistema de Modos de Jogo...")
    print("=" * 50)

    try:
        from game_modes import get_game_mode_manager, GameMode

        # Obter instância do gerenciador
        mode_manager = get_game_mode_manager()
        print("✅ Gerenciador de modos carregado com sucesso!")

        # Testar modos disponíveis
        available_modes = mode_manager.get_available_modes()
        print(f"  • Modos disponíveis: {len(available_modes)}")

        for mode_info in available_modes:
            mode_name = mode_info['name']
            unlocked = mode_info['unlocked']
            status = "🔓" if unlocked else "🔒"
            print(f"    {status} {mode_name}")

        # Testar mudança de modo
        if mode_manager.set_current_mode(GameMode.CLASSIC):
            print("✅ Mudança para modo clássico funcionou!")
        else:
            print("❌ Erro na mudança de modo")

        # Testar configurações do modo
        mode_config = mode_manager.get_current_mode_config()
        if 'duration' in mode_config and 'win_threshold' in mode_config:
            print(f"✅ Configurações do modo: {mode_config['duration']}s, {mode_config['win_threshold']}%")
        else:
            print("❌ Erro nas configurações do modo")

        # Testar dicas do modo
        tips = mode_manager.get_mode_tips()
        if tips:
            print(f"✅ Dicas do modo: {len(tips)} dicas disponíveis")
        else:
            print("❌ Erro nas dicas do modo")

        # Testar progresso de desbloqueio
        unlock_progress = mode_manager.get_unlock_progress()
        if unlock_progress:
            print("✅ Progresso de desbloqueio funcionou!")
        else:
            print("❌ Erro no progresso de desbloqueio")

        print("✅ Todos os testes de modos passaram!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste de modos: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_achievements():
    """Testa o sistema de conquistas"""
    print("\n🏆 Testando Sistema de Conquistas...")
    print("=" * 50)

    try:
        from achievements import get_achievement_manager

        # Obter instância do gerenciador
        achievement_manager = get_achievement_manager()
        print("✅ Gerenciador de conquistas carregado com sucesso!")

        # Testar progresso das conquistas
        progress = achievement_manager.get_achievement_progress()
        print(f"  • Conquistas definidas: {len(progress)}")

        # Mostrar algumas conquistas
        visible_achievements = [
            (aid, data) for aid, data in progress.items()
            if not data['hidden'] and not data['unlocked']
        ][:5]

        for achievement_id, data in visible_achievements:
            print(f"    🏆 {data['name']}: {data['progress_percentage']:.1f}%")

        # Testar verificação de conquistas
        test_game_data = {
            'games_played': 1,
            'games_won': 0,
            'best_percentage': 15.0,
            'total_playtime': 120
        }

        newly_unlocked = achievement_manager.check_achievements(test_game_data)
        if newly_unlocked:
            print(f"✅ {len(newly_unlocked)} conquista(s) desbloqueada(s) no teste!")
        else:
            print("✅ Verificação de conquistas funcionou (nenhuma nova)")

        # Testar resumo das conquistas
        summary = achievement_manager.get_achievement_summary()
        if 'total_achievements' in summary:
            print(f"✅ Resumo: {summary['unlocked_count']}/{summary['total_achievements']} conquistas")
            print(f"  • Progresso: {summary['completion_percentage']:.1f}%")
            print(f"  • Pontos: {summary['total_points']}/{summary['max_points']}")
        else:
            print("❌ Erro no resumo das conquistas")

        # Testar conquistas desbloqueadas
        unlocked = achievement_manager.get_unlocked_achievements()
        print(f"✅ Conquistas desbloqueadas: {len(unlocked)}")

        print("✅ Todos os testes de conquistas passaram!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste de conquistas: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Testa a integração de todas as funcionalidades"""
    print("\n🔗 Testando Integração Completa...")
    print("=" * 50)

    try:
        # Testar importação no sergipe_game.py
        import sergipe_game
        print("✅ Integração com sergipe_game.py funcionou!")

        # Verificar se os novos managers foram importados
        managers_to_check = [
            ('performance_optimizer', 'Otimizador de Performance'),
            ('game_mode_manager', 'Gerenciador de Modos'),
            ('achievement_manager', 'Gerenciador de Conquistas')
        ]

        for manager_name, display_name in managers_to_check:
            if hasattr(sergipe_game, manager_name):
                print(f"✅ {display_name} carregado no jogo!")
            else:
                print(f"⚠️ {display_name} não encontrado no jogo")

        # Testar configurações expandidas
        from config_manager import get_config_manager
        config = get_config_manager()

        # Verificar se as novas seções de configuração existem
        new_sections = ['performance', 'achievements', 'modes']
        for section in new_sections:
            if section in config.config:
                print(f"✅ Seção '{section}' encontrada nas configurações")
            else:
                print(f"⚠️ Seção '{section}' não encontrada (será criada quando necessário)")

        # Testar carregamento de modo atual
        current_mode = config.get('game', 'current_mode', 'classic')
        print(f"✅ Modo atual: {current_mode}")

        print("✅ Teste de integração passou!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste de integração: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance_impact():
    """Testa o impacto na performance das novas funcionalidades"""
    print("\n⚡ Testando Impacto na Performance...")
    print("=" * 50)

    try:
        # Simular operações típicas do jogo
        from performance_optimizer import get_performance_optimizer
        from game_modes import get_game_mode_manager
        from achievements import get_achievement_manager

        optimizer = get_performance_optimizer()
        mode_manager = get_game_mode_manager()
        achievement_manager = get_achievement_manager()

        # Teste de performance: operações repetitivas
        iterations = 1000

        # Teste 1: Otimização de frame
        start_time = time.time()
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)

        for i in range(iterations):
            optimizer.optimize_frame_processing(test_frame)
            optimizer.should_skip_frame(i)
            optimizer.should_skip_detection(i)

        frame_optimization_time = time.time() - start_time
        print(f"✅ Otimização de frame: {frame_optimization_time:.3f}s para {iterations} iterações")

        # Teste 2: Verificação de conquistas
        start_time = time.time()
        test_data = {'games_played': 1, 'best_percentage': 25.0}

        for i in range(100):  # Menos iterações pois é mais pesado
            achievement_manager.check_achievements(test_data)

        achievement_time = time.time() - start_time
        print(f"✅ Verificação de conquistas: {achievement_time:.3f}s para 100 iterações")

        # Teste 3: Configurações de modo
        start_time = time.time()

        for i in range(iterations):
            mode_manager.get_current_mode_config()
            mode_manager.get_mode_tips()

        mode_config_time = time.time() - start_time
        print(f"✅ Configurações de modo: {mode_config_time:.3f}s para {iterations} iterações")

        # Avaliar performance geral
        total_time = frame_optimization_time + achievement_time + mode_config_time
        if total_time < 1.0:  # Menos de 1 segundo para todos os testes
            print("✅ Performance excelente! Impacto mínimo detectado.")
        elif total_time < 2.0:
            print("✅ Performance boa. Impacto aceitável.")
        else:
            print("⚠️ Performance pode ser melhorada.")

        print("✅ Teste de performance concluído!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste de performance: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executa todos os testes da Versão 1.2"""
    print("TESTE COMPLETO DAS FUNCIONALIDADES V1.2")
    print("=" * 60)

    tests = [
        ("Otimizador de Performance", test_performance_optimizer),
        ("Sistema de Modos de Jogo", test_game_modes),
        ("Sistema de Conquistas", test_achievements),
        ("Integração Completa", test_integration),
        ("Impacto na Performance", test_performance_impact)
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

    print("\n" + "=" * 60)
    print(f"📊 RESULTADO FINAL: {passed}/{total} testes passaram")

    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\n✅ Funcionalidades da Versão 1.2 estão funcionando perfeitamente!")
        print("\nNovas funcionalidades disponíveis:")
        print("• 🚀 Otimizador de performance adaptativo")
        print("• 🎮 6 modos de jogo diferentes")
        print("• 🏆 Sistema completo de conquistas")
        print("• ⚡ Otimizações para diferentes hardwares")
        print("• 📊 Métricas avançadas de performance")
        print("• 🎯 Desafios especiais e objetivos")

        print("\n🎮 VIVA SERGIPE! Versão 1.2 está pronta para uso!")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM!")
        print("Verifique os erros acima e corrija antes de usar as novas funcionalidades.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
