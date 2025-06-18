#!/usr/bin/env python3
"""
INSTALADOR AUTOMÁTICO - VIVA SERGIPE!
Sistema de instalação e configuração automática
"""

import os
import sys
import subprocess
import platform
import shutil
import urllib.request
import zipfile
from pathlib import Path
import json


class VivaSergiperInstaller:
    """Instalador automático do VIVA SERGIPE!"""
    
    def __init__(self):
        self.system = platform.system().lower()
        self.python_version = sys.version_info
        self.install_dir = Path.home() / "VIVA_SERGIPE"
        self.requirements = [
            "opencv-python>=4.5.0",
            "protobuf==3.20.3",  # Versão específica para compatibilidade
            "mediapipe>=0.8.0",
            "pygame>=2.0.0",
            "PyQt5>=5.15.0",
            "numpy>=1.20.0",
            "psutil>=5.8.0"
        ]
        
    def check_system_requirements(self):
        """Verifica requisitos do sistema"""
        print("🔍 Verificando requisitos do sistema...")
        
        # Verificar Python
        if self.python_version < (3, 7):
            print("❌ Python 3.7+ é necessário")
            return False
        print(f"✅ Python {self.python_version.major}.{self.python_version.minor}")
        
        # Verificar sistema operacional
        supported_systems = ["windows", "linux", "darwin"]
        if self.system not in supported_systems:
            print(f"❌ Sistema {self.system} não suportado")
            return False
        print(f"✅ Sistema operacional: {platform.system()}")
        
        # Verificar câmera
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                print("✅ Câmera detectada")
                cap.release()
            else:
                print("⚠️ Câmera não detectada (pode ser configurada depois)")
        except:
            print("⚠️ OpenCV não instalado (será instalado)")
        
        return True
    
    def install_dependencies(self):
        """Instala dependências necessárias"""
        print("\n📦 Instalando dependências...")
        
        # Atualizar pip
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            print("✅ pip atualizado")
        except subprocess.CalledProcessError:
            print("⚠️ Erro ao atualizar pip")
        
        # Instalar dependências
        for requirement in self.requirements:
            try:
                print(f"📥 Instalando {requirement}...")
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", requirement
                ])
                print(f"✅ {requirement} instalado")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao instalar {requirement}: {e}")
                return False
        
        return True
    
    def create_install_directory(self):
        """Cria diretório de instalação"""
        print(f"\n📁 Criando diretório de instalação: {self.install_dir}")
        
        try:
            self.install_dir.mkdir(parents=True, exist_ok=True)
            
            # Criar subdiretórios
            subdirs = ["assets", "sounds", "snapshots", "logs", "config"]
            for subdir in subdirs:
                (self.install_dir / subdir).mkdir(exist_ok=True)
            
            print("✅ Diretórios criados com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro ao criar diretórios: {e}")
            return False
    
    def copy_game_files(self):
        """Copia arquivos do jogo"""
        print("\n📋 Copiando arquivos do jogo...")
        
        # Lista de arquivos principais
        game_files = [
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
            "fix_opencv.py",
            "start_game.py",
            "VIVA_SERGIPE.bat",
            "requirements.txt"
        ]
        
        # Copiar arquivos principais
        for file in game_files:
            if os.path.exists(file):
                try:
                    shutil.copy2(file, self.install_dir)
                    print(f"✅ {file}")
                except Exception as e:
                    print(f"❌ Erro ao copiar {file}: {e}")
            else:
                print(f"⚠️ {file} não encontrado")
        
        # Copiar assets
        if os.path.exists("assets"):
            try:
                shutil.copytree("assets", self.install_dir / "assets", dirs_exist_ok=True)
                print("✅ Assets copiados")
            except Exception as e:
                print(f"❌ Erro ao copiar assets: {e}")
        
        # Copiar sounds
        if os.path.exists("sounds"):
            try:
                shutil.copytree("sounds", self.install_dir / "sounds", dirs_exist_ok=True)
                print("✅ Sons copiados")
            except Exception as e:
                print(f"❌ Erro ao copiar sons: {e}")
        
        return True
    
    def create_launcher_scripts(self):
        """Cria scripts de lançamento"""
        print("\n🚀 Criando scripts de lançamento...")
        
        # Script para Windows
        if self.system == "windows":
            launcher_content = f"""@echo off
cd /d "{self.install_dir}"
python sergipe_game.py
pause
"""
            launcher_path = self.install_dir / "VIVA_SERGIPE.bat"
            with open(launcher_path, 'w', encoding='utf-8') as f:
                f.write(launcher_content)
            print("✅ Launcher Windows criado")
        
        # Script para Linux/Mac
        else:
            launcher_content = f"""#!/bin/bash
cd "{self.install_dir}"
python3 sergipe_game.py
"""
            launcher_path = self.install_dir / "VIVA_SERGIPE.sh"
            with open(launcher_path, 'w', encoding='utf-8') as f:
                f.write(launcher_content)
            
            # Tornar executável
            os.chmod(launcher_path, 0o755)
            print("✅ Launcher Unix criado")
        
        return True
    
    def create_desktop_shortcut(self):
        """Cria atalho na área de trabalho"""
        print("\n🖥️ Criando atalho na área de trabalho...")
        
        try:
            if self.system == "windows":
                # Atalho Windows (.lnk requer pywin32, então criamos .bat)
                desktop = Path.home() / "Desktop"
                shortcut_path = desktop / "VIVA SERGIPE!.bat"
                
                shortcut_content = f"""@echo off
cd /d "{self.install_dir}"
python sergipe_game.py
"""
                with open(shortcut_path, 'w', encoding='utf-8') as f:
                    f.write(shortcut_content)
                
            elif self.system == "linux":
                # Atalho Linux (.desktop)
                desktop = Path.home() / "Desktop"
                shortcut_path = desktop / "VIVA_SERGIPE.desktop"
                
                shortcut_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=VIVA SERGIPE!
Comment=Jogo interativo de Sergipe
Exec=python3 "{self.install_dir}/sergipe_game.py"
Icon={self.install_dir}/assets/flag-se.jpg
Terminal=false
Categories=Game;
"""
                with open(shortcut_path, 'w', encoding='utf-8') as f:
                    f.write(shortcut_content)
                
                os.chmod(shortcut_path, 0o755)
            
            print("✅ Atalho criado na área de trabalho")
            return True
            
        except Exception as e:
            print(f"⚠️ Não foi possível criar atalho: {e}")
            return False
    
    def create_uninstaller(self):
        """Cria script de desinstalação"""
        print("\n🗑️ Criando desinstalador...")
        
        uninstaller_content = f"""#!/usr/bin/env python3
import shutil
import os
from pathlib import Path

def uninstall():
    install_dir = Path("{self.install_dir}")
    
    print("🗑️ Desinstalando VIVA SERGIPE!...")
    
    if install_dir.exists():
        try:
            shutil.rmtree(install_dir)
            print("✅ Arquivos removidos com sucesso")
        except Exception as e:
            print(f"❌ Erro ao remover arquivos: {{e}}")
    
    # Remover atalho da área de trabalho
    desktop = Path.home() / "Desktop"
    shortcuts = [
        desktop / "VIVA SERGIPE!.bat",
        desktop / "VIVA_SERGIPE.desktop"
    ]
    
    for shortcut in shortcuts:
        if shortcut.exists():
            try:
                shortcut.unlink()
                print("✅ Atalho removido")
            except:
                pass
    
    print("🎉 Desinstalação concluída!")
    input("Pressione Enter para sair...")

if __name__ == "__main__":
    uninstall()
"""
        
        uninstaller_path = self.install_dir / "uninstall.py"
        with open(uninstaller_path, 'w', encoding='utf-8') as f:
            f.write(uninstaller_content)
        
        print("✅ Desinstalador criado")
        return True
    
    def create_config_file(self):
        """Cria arquivo de configuração inicial"""
        print("\n⚙️ Criando configuração inicial...")
        
        initial_config = {
            "installation": {
                "version": "1.2",
                "install_date": str(Path.ctime(Path.now())),
                "install_path": str(self.install_dir),
                "system": self.system
            },
            "first_run": True,
            "auto_update_check": True
        }
        
        config_path = self.install_dir / "config" / "installation.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(initial_config, f, indent=4, ensure_ascii=False)
        
        print("✅ Configuração inicial criada")
        return True
    
    def run_post_install_tests(self):
        """Executa testes pós-instalação"""
        print("\n🧪 Executando testes pós-instalação...")
        
        # Mudar para diretório de instalação
        original_dir = os.getcwd()
        os.chdir(self.install_dir)
        
        try:
            # Testar importações
            test_imports = [
                "import cv2",
                "import mediapipe",
                "import pygame",
                "import numpy",
                "import psutil"
            ]
            
            for test_import in test_imports:
                try:
                    exec(test_import)
                    module_name = test_import.split()[1]
                    print(f"✅ {module_name}")
                except ImportError as e:
                    print(f"❌ {test_import}: {e}")
                    return False
            
            # Testar arquivos principais
            required_files = ["sergipe_game.py", "config_manager.py"]
            for file in required_files:
                if os.path.exists(file):
                    print(f"✅ {file}")
                else:
                    print(f"❌ {file} não encontrado")
                    return False
            
            print("✅ Todos os testes passaram!")
            return True
            
        except Exception as e:
            print(f"❌ Erro nos testes: {e}")
            return False
        finally:
            os.chdir(original_dir)
    
    def install(self):
        """Executa instalação completa"""
        print("🎮 INSTALADOR DO VIVA SERGIPE! v1.2")
        print("=" * 50)
        
        steps = [
            ("Verificar requisitos", self.check_system_requirements),
            ("Instalar dependências", self.install_dependencies),
            ("Criar diretórios", self.create_install_directory),
            ("Copiar arquivos", self.copy_game_files),
            ("Criar launchers", self.create_launcher_scripts),
            ("Criar atalho", self.create_desktop_shortcut),
            ("Criar desinstalador", self.create_uninstaller),
            ("Configuração inicial", self.create_config_file),
            ("Testes finais", self.run_post_install_tests)
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            if not step_func():
                print(f"❌ Falha em: {step_name}")
                return False
        
        print("\n" + "=" * 50)
        print("🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"📁 Instalado em: {self.install_dir}")
        print("🚀 Use o atalho na área de trabalho para jogar")
        print("📖 Leia a documentação para mais informações")
        print("🎮 Divirta-se com o VIVA SERGIPE!")
        
        return True


def main():
    """Função principal do instalador"""
    installer = VivaSergiperInstaller()
    
    try:
        success = installer.install()
        if success:
            input("\nPressione Enter para sair...")
        else:
            print("\n❌ Instalação falhou!")
            input("Pressione Enter para sair...")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Instalação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
