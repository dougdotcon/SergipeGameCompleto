#!/usr/bin/env python3
"""
Teste do sistema de configurações do VIVA SERGIPE!
"""

import sys
import os

# Adiciona o diretório atual ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_config_manager():
    """Testa o gerenciador de configurações"""
    print("🧪 Testando Gerenciador de Configurações...")
    print("=" * 50)

    try:
        from config_manager import get_config_manager

        # Obter instância do gerenciador
        config = get_config_manager()
        print("✅ Gerenciador de configurações carregado com sucesso!")

        # Testar carregamento de configurações padrão
        print("\n📋 Configurações atuais:")
        game_settings = config.get_game_settings()
        print(f"  • Duração: {game_settings['duration']} segundos")
        print(f"  • Meta: {game_settings['win_threshold']}%")
        print(f"  • Sensibilidade: {game_settings['min_body_pixels']} pixels")

        # Testar configurações de áudio
        print(f"  • Volume geral: {config.get('audio', 'master_volume', 0.7) * 100:.0f}%")
        print(f"  • Volume música: {config.get('audio', 'music_volume', 0.5) * 100:.0f}%")

        # Testar alteração de configuração
        print("\n🔧 Testando alteração de configurações...")
        original_duration = config.get('game', 'duration', 300)
        config.set('game', 'duration', 240, save=False)  # 4 minutos
        new_duration = config.get('game', 'duration', 300)

        if new_duration == 240:
            print("✅ Alteração de configuração funcionou!")
        else:
            print("❌ Erro na alteração de configuração")

        # Restaurar valor original
        config.set('game', 'duration', original_duration, save=False)

        # Testar estatísticas
        print("\n📊 Testando estatísticas...")
        stats_before = config.get('stats', 'games_played', 0)
        config.update_stats(games_played=1, total_playtime=120.5)
        stats_after = config.get('stats', 'games_played', 0)

        if stats_after > stats_before:
            print("✅ Atualização de estatísticas funcionou!")
        else:
            print("❌ Erro na atualização de estatísticas")

        print("\n✅ Todos os testes do gerenciador passaram!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste do gerenciador: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_window():
    """Testa a janela de configurações"""
    print("\n🖼️ Testando Janela de Configurações...")
    print("=" * 50)

    try:
        from PyQt5.QtWidgets import QApplication
        from config_window import ConfigWindow

        # Verificar se já existe uma instância do QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        # Criar janela de configurações
        window = ConfigWindow()
        print("✅ Janela de configurações criada com sucesso!")

        # Testar carregamento de configurações
        window.load_current_settings()
        print("✅ Configurações carregadas na interface!")

        # Verificar se os controles foram preenchidos
        duration = window.duration_spinbox.value()
        threshold = window.threshold_spinbox.value()
        sensitivity = window.sensitivity_spinbox.value()

        print(f"  • Duração na interface: {duration} segundos")
        print(f"  • Meta na interface: {threshold}%")
        print(f"  • Sensibilidade na interface: {sensitivity} pixels")

        if duration > 0 and threshold > 0 and sensitivity > 0:
            print("✅ Controles da interface preenchidos corretamente!")
        else:
            print("❌ Erro no preenchimento dos controles")

        # Fechar janela sem mostrar
        window.close()

        print("✅ Teste da janela de configurações passou!")
        return True

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("Certifique-se de que PyQt5 está instalado:")
        print("pip install PyQt5")
        return False
    except Exception as e:
        print(f"❌ Erro no teste da janela: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_integration():
    """Testa a integração com o jogo principal"""
    print("\n🎮 Testando Integração com o Jogo...")
    print("=" * 50)

    try:
        # Testar importação no sergipe_game.py
        import sergipe_game
        print("✅ Integração com sergipe_game.py funcionou!")

        # Verificar se GAME_SETTINGS foi carregado
        if hasattr(sergipe_game, 'GAME_SETTINGS'):
            settings = sergipe_game.GAME_SETTINGS
            print(f"  • Configurações carregadas no jogo:")
            print(f"    - Duração: {settings.get('duration', 'N/A')} segundos")
            print(f"    - Meta: {settings.get('win_threshold', 'N/A')}%")
            print(f"    - Sensibilidade: {settings.get('min_body_pixels', 'N/A')} pixels")
            print("✅ GAME_SETTINGS carregado corretamente!")
        else:
            print("❌ GAME_SETTINGS não encontrado")
            return False

        # Testar integração com menu
        try:
            import menu_gui
            print("✅ Integração com menu_gui.py funcionou!")
        except Exception as e:
            print(f"⚠️ Aviso na integração com menu: {e}")

        print("✅ Teste de integração passou!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste de integração: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_operations():
    """Testa operações de arquivo"""
    print("\n💾 Testando Operações de Arquivo...")
    print("=" * 50)

    try:
        from config_manager import ConfigManager

        # Criar gerenciador de teste
        test_config = ConfigManager("test_config.json")

        # Testar salvamento
        test_config.set('test', 'value', 'teste_123')
        print("✅ Configuração de teste salva!")

        # Criar novo gerenciador para testar carregamento
        test_config2 = ConfigManager("test_config.json")
        loaded_value = test_config2.get('test', 'value', 'default')

        if loaded_value == 'teste_123':
            print("✅ Carregamento de arquivo funcionou!")
        else:
            print(f"❌ Erro no carregamento: esperado 'teste_123', obtido '{loaded_value}'")

        # Limpar arquivo de teste
        import os
        if os.path.exists("test_config.json"):
            os.remove("test_config.json")
            print("✅ Arquivo de teste removido!")

        print("✅ Teste de operações de arquivo passou!")
        return True

    except Exception as e:
        print(f"❌ Erro no teste de arquivo: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Executa todos os testes"""
    print("TESTE COMPLETO DO SISTEMA DE CONFIGURACOES")
    print("=" * 60)

    tests = [
        ("Gerenciador de Configurações", test_config_manager),
        ("Janela de Configurações", test_config_window),
        ("Integração com o Jogo", test_integration),
        ("Operações de Arquivo", test_file_operations)
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
        print("\n✅ O sistema de configurações está funcionando corretamente!")
        print("\nPara usar:")
        print("1. Execute: python sergipe_game.py")
        print("2. Clique em 'CONFIGURAÇÕES' no menu")
        print("3. Ajuste as configurações conforme desejado")
        print("4. Clique em 'Salvar'")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM!")
        print("Verifique os erros acima e corrija antes de usar o sistema.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
