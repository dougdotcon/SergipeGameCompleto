#!/usr/bin/env python3
"""
SCRIPT DE BUILD - VIVA SERGIPE!
Sistema para criar distribuições do jogo
"""

import os
import sys
import shutil
import zipfile
import subprocess
import platform
from pathlib import Path
import json
import time


class BuildManager:
    """Gerenciador de build e distribuição"""
    
    def __init__(self):
        self.project_name = "VIVA_SERGIPE"
        self.version = "1.2.0"
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        self.system = platform.system().lower()
        
        # Arquivos principais do projeto
        self.core_files = [
            "sergipe_game.py",
            "sergipe_game_headless.py",
            "game_controller.py",
            "menu_gui.py",
            "config_manager.py",
            "config_window.py",
            "visual_feedback.py",
            "sync_manager.py",
            "performance_optimizer.py",
            "game_modes.py",
            "achievements.py",
            "sergipe_utils.py",
            "utils.py",
            "analytics.py",
            "updater.py",
            "installer.py",
            "fix_opencv.py"
        ]
        
        # Arquivos de configuração
        self.config_files = [
            "requirements.txt",
            "README.md",
            "README_SERGIPE.md",
            "COMO_JOGAR.md",
            "MANUAL_TECNICO.md",
            "CHECKLIST.md"
        ]
        
        # Diretórios de recursos
        self.resource_dirs = [
            "assets",
            "sounds"
        ]
        
        # Arquivos de teste
        self.test_files = [
            "test_sergipe.py",
            "test_menu.py",
            "test_visual.py",
            "test_config.py",
            "test_visual_feedback.py",
            "test_v1.2_features.py"
        ]
    
    def clean_build(self):
        """Limpa diretórios de build anteriores"""
        print("🧹 Limpando builds anteriores...")
        
        for directory in [self.build_dir, self.dist_dir]:
            if directory.exists():
                shutil.rmtree(directory)
                print(f"  ✅ {directory} removido")
        
        # Criar diretórios
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        print("  ✅ Diretórios criados")
    
    def validate_files(self):
        """Valida se todos os arquivos necessários existem"""
        print("🔍 Validando arquivos do projeto...")
        
        missing_files = []
        
        # Verificar arquivos principais
        for file in self.core_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        # Verificar arquivos de configuração
        for file in self.config_files:
            if not os.path.exists(file):
                print(f"  ⚠️ {file} não encontrado (opcional)")
        
        # Verificar diretórios de recursos
        for directory in self.resource_dirs:
            if not os.path.exists(directory):
                print(f"  ⚠️ {directory}/ não encontrado (opcional)")
        
        if missing_files:
            print("❌ Arquivos obrigatórios não encontrados:")
            for file in missing_files:
                print(f"  - {file}")
            return False
        
        print("✅ Todos os arquivos obrigatórios encontrados")
        return True
    
    def create_portable_build(self):
        """Cria build portável (pasta com todos os arquivos)"""
        print("📦 Criando build portável...")
        
        portable_dir = self.build_dir / f"{self.project_name}_v{self.version}_portable"
        portable_dir.mkdir(exist_ok=True)
        
        # Copiar arquivos principais
        for file in self.core_files:
            if os.path.exists(file):
                shutil.copy2(file, portable_dir)
                print(f"  ✅ {file}")
        
        # Copiar arquivos de configuração
        for file in self.config_files:
            if os.path.exists(file):
                shutil.copy2(file, portable_dir)
        
        # Copiar diretórios de recursos
        for directory in self.resource_dirs:
            if os.path.exists(directory):
                shutil.copytree(directory, portable_dir / directory, dirs_exist_ok=True)
                print(f"  ✅ {directory}/")
        
        # Copiar testes
        test_dir = portable_dir / "tests"
        test_dir.mkdir(exist_ok=True)
        for file in self.test_files:
            if os.path.exists(file):
                shutil.copy2(file, test_dir)
        
        # Criar script de execução
        self.create_run_script(portable_dir)
        
        # Criar arquivo de versão
        self.create_version_file(portable_dir)
        
        print(f"✅ Build portável criado: {portable_dir}")
        return portable_dir
    
    def create_run_script(self, target_dir):
        """Cria script de execução para o build"""
        if self.system == "windows":
            script_content = f"""@echo off
title VIVA SERGIPE! v{self.version}
echo 🎮 VIVA SERGIPE! v{self.version}
echo ================================
echo.
echo Verificando dependências...
python -c "import cv2, mediapipe, pygame, PyQt5, numpy, psutil" 2>nul
if errorlevel 1 (
    echo ❌ Dependências não instaladas!
    echo.
    echo Para instalar:
    echo pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)
echo ✅ Dependências OK
echo.
echo Iniciando jogo...
python sergipe_game.py
if errorlevel 1 (
    echo.
    echo ❌ Erro ao executar o jogo
    pause
)
"""
            script_path = target_dir / "EXECUTAR.bat"
            
        else:  # Linux/Mac
            script_content = f"""#!/bin/bash
echo "🎮 VIVA SERGIPE! v{self.version}"
echo "================================"
echo
echo "Verificando dependências..."
python3 -c "import cv2, mediapipe, pygame, PyQt5, numpy, psutil" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Dependências não instaladas!"
    echo
    echo "Para instalar:"
    echo "pip3 install -r requirements.txt"
    echo
    read -p "Pressione Enter para sair..."
    exit 1
fi
echo "✅ Dependências OK"
echo
echo "Iniciando jogo..."
python3 sergipe_game.py
if [ $? -ne 0 ]; then
    echo
    echo "❌ Erro ao executar o jogo"
    read -p "Pressione Enter para sair..."
fi
"""
            script_path = target_dir / "executar.sh"
            
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        # Tornar executável no Unix
        if self.system != "windows":
            os.chmod(script_path, 0o755)
        
        print(f"  ✅ Script de execução: {script_path.name}")
    
    def create_version_file(self, target_dir):
        """Cria arquivo com informações da versão"""
        version_info = {
            "name": "VIVA SERGIPE!",
            "version": self.version,
            "build_date": time.strftime('%Y-%m-%d %H:%M:%S'),
            "build_system": platform.system(),
            "python_version": platform.python_version(),
            "description": "Jogo interativo de Sergipe com detecção corporal",
            "author": "Equipe VIVA SERGIPE!",
            "license": "MIT",
            "website": "https://github.com/viva-sergipe/game",
            "requirements": {
                "python": ">=3.7",
                "opencv-python": ">=4.5.0",
                "mediapipe": ">=0.8.0",
                "PyQt5": ">=5.15.0",
                "pygame": ">=2.0.0",
                "numpy": ">=1.20.0",
                "psutil": ">=5.8.0"
            }
        }
        
        version_path = target_dir / "version.json"
        with open(version_path, 'w', encoding='utf-8') as f:
            json.dump(version_info, f, indent=4, ensure_ascii=False)
        
        print(f"  ✅ Arquivo de versão: {version_path.name}")
    
    def create_zip_distribution(self, source_dir):
        """Cria distribuição em ZIP"""
        print("📦 Criando distribuição ZIP...")
        
        zip_name = f"{self.project_name}_v{self.version}_{self.system}.zip"
        zip_path = self.dist_dir / zip_name
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = file_path.relative_to(source_dir.parent)
                    zipf.write(file_path, arc_name)
        
        print(f"✅ ZIP criado: {zip_path}")
        return zip_path
    
    def create_installer_package(self, source_dir):
        """Cria pacote com instalador"""
        print("📦 Criando pacote com instalador...")
        
        installer_dir = self.build_dir / f"{self.project_name}_v{self.version}_installer"
        installer_dir.mkdir(exist_ok=True)
        
        # Copiar arquivos do build portável
        for item in source_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, installer_dir)
            else:
                shutil.copytree(item, installer_dir / item.name, dirs_exist_ok=True)
        
        # Criar script de instalação
        install_script_content = f"""#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from installer import VivaSergiperInstaller

if __name__ == "__main__":
    installer = VivaSergiperInstaller()
    installer.install()
"""
        
        install_script_path = installer_dir / "install.py"
        with open(install_script_path, 'w', encoding='utf-8') as f:
            f.write(install_script_content)
        
        print(f"✅ Pacote com instalador: {installer_dir}")
        return installer_dir
    
    def run_tests(self):
        """Executa testes antes do build"""
        print("🧪 Executando testes...")
        
        test_results = []
        
        for test_file in self.test_files:
            if os.path.exists(test_file):
                try:
                    result = subprocess.run([
                        sys.executable, test_file
                    ], capture_output=True, text=True, timeout=60)
                    
                    if result.returncode == 0:
                        print(f"  ✅ {test_file}")
                        test_results.append(True)
                    else:
                        print(f"  ❌ {test_file}: {result.stderr}")
                        test_results.append(False)
                        
                except subprocess.TimeoutExpired:
                    print(f"  ⏰ {test_file}: Timeout")
                    test_results.append(False)
                except Exception as e:
                    print(f"  ❌ {test_file}: {e}")
                    test_results.append(False)
        
        success_rate = sum(test_results) / len(test_results) if test_results else 0
        print(f"📊 Testes: {sum(test_results)}/{len(test_results)} passaram ({success_rate*100:.1f}%)")
        
        return success_rate > 0.8  # 80% dos testes devem passar
    
    def build_all(self, run_tests=True, create_zip=True, create_installer=True):
        """Executa build completo"""
        print(f"🚀 INICIANDO BUILD DO {self.project_name} v{self.version}")
        print("=" * 60)
        
        # Limpar builds anteriores
        self.clean_build()
        
        # Validar arquivos
        if not self.validate_files():
            print("❌ Build cancelado devido a arquivos faltando")
            return False
        
        # Executar testes
        if run_tests:
            if not self.run_tests():
                print("⚠️ Alguns testes falharam, mas continuando build...")
        
        # Criar build portável
        portable_dir = self.create_portable_build()
        
        # Criar distribuições
        distributions = []
        
        if create_zip:
            zip_path = self.create_zip_distribution(portable_dir)
            distributions.append(zip_path)
        
        if create_installer:
            installer_dir = self.create_installer_package(portable_dir)
            installer_zip = self.create_zip_distribution(installer_dir)
            distributions.append(installer_zip)
        
        # Resumo final
        print("\n" + "=" * 60)
        print("🎉 BUILD CONCLUÍDO COM SUCESSO!")
        print(f"📁 Build portável: {portable_dir}")
        print("📦 Distribuições criadas:")
        for dist in distributions:
            file_size = dist.stat().st_size / (1024 * 1024)  # MB
            print(f"  • {dist.name} ({file_size:.1f} MB)")
        
        print(f"\n✅ {self.project_name} v{self.version} pronto para distribuição!")
        return True


def main():
    """Função principal do script de build"""
    builder = BuildManager()
    
    # Argumentos da linha de comando
    import argparse
    parser = argparse.ArgumentParser(description="Build do VIVA SERGIPE!")
    parser.add_argument("--no-tests", action="store_true", help="Pular testes")
    parser.add_argument("--no-zip", action="store_true", help="Não criar ZIP")
    parser.add_argument("--no-installer", action="store_true", help="Não criar instalador")
    
    args = parser.parse_args()
    
    try:
        success = builder.build_all(
            run_tests=not args.no_tests,
            create_zip=not args.no_zip,
            create_installer=not args.no_installer
        )
        
        if success:
            print("\n🎮 Build concluído! O VIVA SERGIPE! está pronto!")
        else:
            print("\n❌ Build falhou!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Build cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado no build: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
