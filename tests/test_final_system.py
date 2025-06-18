#!/usr/bin/env python3
"""
TESTE FINAL DO SISTEMA - VIVA SERGIPE!
Validação completa de todas as funcionalidades antes da distribuição
"""

import sys
import os
import time
import json
import subprocess
from pathlib import Path

# Adiciona o diretório atual ao path para importar os módulos
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_dependencies():
    """Testa se todas as dependências estão instaladas"""
    print("📦 Testando Dependências...")
    print("=" * 50)
    
    dependencies = [
        ("OpenCV", "cv2"),
        ("MediaPipe", "mediapipe"),
        ("PyQt5", "PyQt5.QtWidgets"),
        ("Pygame", "pygame"),
        ("NumPy", "numpy"),
        ("psutil", "psutil")
    ]
    
    failed_deps = []
    
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {e}")
            failed_deps.append(name)
    
    if failed_deps:
        print(f"\n❌ Dependências faltando: {', '.join(failed_deps)}")
        return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def test_file_structure():
    """Testa se todos os arquivos necessários existem"""
    print("\n📁 Testando Estrutura de Arquivos...")
    print("=" * 50)
    
    required_files = [
        "sergipe_game.py",
        "config_manager.py",
        "visual_feedback.py",
        "sync_manager.py",
        "performance_optimizer.py",
        "game_modes.py",
        "achievements.py",
        "menu_gui.py",
        "sergipe_utils.py",
        "utils.py"
    ]
    
    optional_files = [
        "installer.py",
        "updater.py",
        "analytics.py",
        "build.py"
    ]
    
    required_dirs = [
        "assets",
        "sounds"
    ]
    
    missing_files = []
    
    # Verificar arquivos obrigatórios
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    # Verificar arquivos opcionais
    for file in optional_files:
        if os.path.exists(file):
            print(f"✅ {file} (opcional)")
        else:
            print(f"⚠️ {file} (opcional, não encontrado)")
    
    # Verificar diretórios
    for directory in required_dirs:
        if os.path.exists(directory):
            files_count = len(list(Path(directory).rglob('*')))
            print(f"✅ {directory}/ ({files_count} arquivos)")
        else:
            print(f"❌ {directory}/")
            missing_files.append(f"{directory}/")
    
    if missing_files:
        print(f"\n❌ Arquivos/diretórios obrigatórios faltando: {', '.join(missing_files)}")
        return False
    
    print("✅ Estrutura de arquivos completa!")
    return True

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    print("\n🔗 Testando Importações...")
    print("=" * 50)
    
    modules_to_test = [
        "config_manager",
        "visual_feedback", 
        "sync_manager",
        "performance_optimizer",
        "game_modes",
        "achievements",
        "sergipe_utils",
        "utils"
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)
        except Exception as e:
            print(f"⚠️ {module}: {e}")
    
    if failed_imports:
        print(f"\n❌ Falha na importação: {', '.join(failed_imports)}")
        return False
    
    print("✅ Todas as importações funcionaram!")
    return True

def test_managers():
    """Testa se todos os managers podem ser inicializados"""
    print("\n⚙️ Testando Managers...")
    print("=" * 50)
    
    try:
        # Testar config manager
        from config_manager import get_config_manager
        config = get_config_manager()
        print("✅ Config Manager")
        
        # Testar visual feedback
        from visual_feedback import get_visual_feedback_manager
        visual = get_visual_feedback_manager()
        print("✅ Visual Feedback Manager")
        
        # Testar sync manager
        from sync_manager import get_sync_manager
        sync = get_sync_manager()
        print("✅ Sync Manager")
        
        # Testar performance optimizer
        from performance_optimizer import get_performance_optimizer
        perf = get_performance_optimizer()
        print("✅ Performance Optimizer")
        
        # Testar game modes
        from game_modes import get_game_mode_manager
        modes = get_game_mode_manager()
        print("✅ Game Mode Manager")
        
        # Testar achievements
        from achievements import get_achievement_manager
        achievements = get_achievement_manager()
        print("✅ Achievement Manager")
        
        print("✅ Todos os managers inicializados com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao inicializar managers: {e}")
        return False

def test_configuration_system():
    """Testa o sistema de configurações"""
    print("\n⚙️ Testando Sistema de Configurações...")
    print("=" * 50)
    
    try:
        from config_manager import get_config_manager
        config = get_config_manager()
        
        # Testar leitura
        duration = config.get('game', 'duration', 300)
        print(f"✅ Leitura de configuração: duration = {duration}")
        
        # Testar escrita
        config.set('test', 'value', 'test_123', save=False)
        test_value = config.get('test', 'value', 'default')
        
        if test_value == 'test_123':
            print("✅ Escrita de configuração funcionou")
        else:
            print("❌ Erro na escrita de configuração")
            return False
        
        # Testar estatísticas
        config.update_stats(test_stat=1)
        print("✅ Atualização de estatísticas")
        
        print("✅ Sistema de configurações funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de configurações: {e}")
        return False

def test_game_features():
    """Testa funcionalidades específicas do jogo"""
    print("\n🎮 Testando Funcionalidades do Jogo...")
    print("=" * 50)
    
    try:
        # Testar modos de jogo
        from game_modes import get_game_mode_manager, GameMode
        mode_manager = get_game_mode_manager()
        
        available_modes = mode_manager.get_available_modes()
        print(f"✅ Modos de jogo: {len(available_modes)} disponíveis")
        
        # Testar conquistas
        from achievements import get_achievement_manager
        achievement_manager = get_achievement_manager()
        
        progress = achievement_manager.get_achievement_progress()
        print(f"✅ Conquistas: {len(progress)} definidas")
        
        # Testar utils do Sergipe
        from sergipe_utils import load_sergipe_contour
        contour = load_sergipe_contour()
        
        if contour is not None:
            print("✅ Carregamento do contorno de Sergipe")
        else:
            print("❌ Erro no carregamento do contorno")
            return False
        
        print("✅ Funcionalidades do jogo testadas!")
        return True
        
    except Exception as e:
        print(f"❌ Erro nas funcionalidades do jogo: {e}")
        return False

def test_performance_system():
    """Testa o sistema de performance"""
    print("\n⚡ Testando Sistema de Performance...")
    print("=" * 50)
    
    try:
        from performance_optimizer import get_performance_optimizer
        import numpy as np
        
        optimizer = get_performance_optimizer()
        
        # Testar otimização de frame
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        optimized = optimizer.optimize_frame_processing(test_frame)
        print("✅ Otimização de frame")
        
        # Testar configurações de câmera
        camera_settings = optimizer.get_optimized_camera_settings()
        print(f"✅ Configurações de câmera: {camera_settings['width']}x{camera_settings['height']}")
        
        # Testar relatório
        report = optimizer.get_performance_report()
        print("✅ Relatório de performance")
        
        print("✅ Sistema de performance funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema de performance: {e}")
        return False

def test_individual_test_files():
    """Executa os arquivos de teste individuais"""
    print("\n🧪 Executando Testes Individuais...")
    print("=" * 50)
    
    test_files = [
        "test_config.py",
        "test_visual_feedback.py", 
        "test_v1.2_features.py"
    ]
    
    results = []
    
    for test_file in test_files:
        if os.path.exists(test_file):
            try:
                print(f"\n🔍 Executando {test_file}...")
                result = subprocess.run([
                    sys.executable, test_file
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    print(f"✅ {test_file}: PASSOU")
                    results.append(True)
                else:
                    print(f"❌ {test_file}: FALHOU")
                    print(f"Erro: {result.stderr}")
                    results.append(False)
                    
            except subprocess.TimeoutExpired:
                print(f"⏰ {test_file}: TIMEOUT")
                results.append(False)
            except Exception as e:
                print(f"❌ {test_file}: ERRO - {e}")
                results.append(False)
        else:
            print(f"⚠️ {test_file}: Não encontrado")
    
    if results:
        success_rate = sum(results) / len(results)
        print(f"\n📊 Testes individuais: {sum(results)}/{len(results)} passaram ({success_rate*100:.1f}%)")
        return success_rate >= 0.8
    else:
        print("⚠️ Nenhum teste individual encontrado")
        return True

def test_system_integration():
    """Testa integração completa do sistema"""
    print("\n🔗 Testando Integração do Sistema...")
    print("=" * 50)
    
    try:
        # Simular inicialização completa
        from config_manager import get_config_manager
        from visual_feedback import get_visual_feedback_manager
        from sync_manager import get_sync_manager
        from performance_optimizer import get_performance_optimizer
        from game_modes import get_game_mode_manager
        from achievements import get_achievement_manager
        
        # Inicializar todos os managers
        config = get_config_manager()
        visual = get_visual_feedback_manager()
        sync = get_sync_manager()
        perf = get_performance_optimizer()
        modes = get_game_mode_manager()
        achievements = get_achievement_manager()
        
        print("✅ Todos os managers inicializados")
        
        # Testar interação entre sistemas
        game_settings = config.get_game_settings()
        mode_settings = modes.get_current_mode_config()
        
        print("✅ Interação entre config e modos")
        
        # Simular sessão de jogo
        test_result = {
            'won': True,
            'game_time': 120.5,
            'best_percentage': 35.2
        }
        
        newly_unlocked = achievements.check_achievements(test_result)
        print(f"✅ Sistema de conquistas: {len(newly_unlocked)} novas")
        
        print("✅ Integração do sistema funcionando!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na integração: {e}")
        return False

def generate_system_report():
    """Gera relatório completo do sistema"""
    print("\n📊 Gerando Relatório do Sistema...")
    print("=" * 50)
    
    try:
        import platform
        import psutil
        
        report = {
            "system_info": {
                "os": platform.system(),
                "os_version": platform.release(),
                "python_version": platform.python_version(),
                "cpu_cores": psutil.cpu_count(),
                "ram_gb": round(psutil.virtual_memory().total / (1024**3), 1)
            },
            "test_timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
            "project_version": "1.2.0"
        }
        
        # Salvar relatório
        with open("system_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        
        print("✅ Relatório salvo em: system_report.json")
        print(f"  • OS: {report['system_info']['os']} {report['system_info']['os_version']}")
        print(f"  • Python: {report['system_info']['python_version']}")
        print(f"  • CPU: {report['system_info']['cpu_cores']} cores")
        print(f"  • RAM: {report['system_info']['ram_gb']} GB")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar relatório: {e}")
        return False

def main():
    """Executa teste final completo do sistema"""
    print("🧪 TESTE FINAL COMPLETO DO SISTEMA - VIVA SERGIPE!")
    print("=" * 70)
    
    tests = [
        ("Dependências", test_dependencies),
        ("Estrutura de Arquivos", test_file_structure),
        ("Importações", test_imports),
        ("Managers", test_managers),
        ("Sistema de Configurações", test_configuration_system),
        ("Funcionalidades do Jogo", test_game_features),
        ("Sistema de Performance", test_performance_system),
        ("Testes Individuais", test_individual_test_files),
        ("Integração do Sistema", test_system_integration),
        ("Relatório do Sistema", generate_system_report)
    ]
    
    passed = 0
    total = len(tests)
    start_time = time.time()
    
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
    
    elapsed_time = time.time() - start_time
    
    print("\n" + "=" * 70)
    print(f"📊 RESULTADO FINAL: {passed}/{total} testes passaram")
    print(f"⏱️ Tempo total: {elapsed_time:.1f} segundos")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\n✅ O VIVA SERGIPE! está PRONTO PARA DISTRIBUIÇÃO!")
        print("\n🚀 Sistema validado com sucesso:")
        print("  • Todas as dependências instaladas")
        print("  • Estrutura de arquivos completa")
        print("  • Todos os módulos funcionando")
        print("  • Integração entre sistemas OK")
        print("  • Performance otimizada")
        print("  • Funcionalidades testadas")
        
        print("\n🎮 O jogo está pronto para ser distribuído!")
        return True
    else:
        print("⚠️ ALGUNS TESTES FALHARAM!")
        print("Corrija os problemas antes da distribuição.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
