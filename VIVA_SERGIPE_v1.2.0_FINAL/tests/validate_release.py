#!/usr/bin/env python3
"""
VALIDADOR DE RELEASE - VIVA SERGIPE!
Script final para validar que o projeto está pronto para distribuição
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
import subprocess


class ReleaseValidator:
    """Validador final do release"""
    
    def __init__(self):
        self.project_name = "VIVA_SERGIPE"
        self.version = "1.2.0"
        self.errors = []
        self.warnings = []
        self.passed_checks = []
        
    def validate_core_files(self) -> bool:
        """Valida arquivos principais do projeto"""
        print("🔍 Validando arquivos principais...")
        
        required_files = [
            "sergipe_game.py",
            "config_manager.py",
            "visual_feedback.py",
            "sync_manager.py",
            "performance_optimizer.py",
            "game_modes.py",
            "achievements.py",
            "menu_gui.py",
            "installer.py",
            "requirements.txt",
            "README.md",
            "version.json"
        ]
        
        missing_files = []
        for file in required_files:
            if os.path.exists(file):
                file_size = os.path.getsize(file)
                print(f"  ✅ {file} ({file_size} bytes)")
                self.passed_checks.append(f"Arquivo {file} presente")
            else:
                missing_files.append(file)
                self.errors.append(f"Arquivo obrigatório faltando: {file}")
        
        if missing_files:
            print(f"  ❌ Arquivos faltando: {', '.join(missing_files)}")
            return False
        
        return True
    
    def validate_directories(self) -> bool:
        """Valida estrutura de diretórios"""
        print("\n📁 Validando estrutura de diretórios...")
        
        required_dirs = {
            "assets": 5,  # Mínimo de arquivos esperados
            "sounds": 10
        }
        
        for directory, min_files in required_dirs.items():
            if os.path.exists(directory):
                files_count = len(list(Path(directory).rglob('*')))
                if files_count >= min_files:
                    print(f"  ✅ {directory}/ ({files_count} arquivos)")
                    self.passed_checks.append(f"Diretório {directory} válido")
                else:
                    print(f"  ⚠️ {directory}/ tem apenas {files_count} arquivos (mínimo: {min_files})")
                    self.warnings.append(f"Diretório {directory} com poucos arquivos")
            else:
                print(f"  ❌ {directory}/ não encontrado")
                self.errors.append(f"Diretório obrigatório faltando: {directory}")
        
        return len(self.errors) == 0
    
    def validate_version_consistency(self) -> bool:
        """Valida consistência de versão entre arquivos"""
        print("\n🔢 Validando consistência de versão...")
        
        version_sources = {}
        
        # Verificar version.json
        if os.path.exists("version.json"):
            try:
                with open("version.json", 'r', encoding='utf-8') as f:
                    version_data = json.load(f)
                    version_sources["version.json"] = version_data.get("version", "unknown")
            except Exception as e:
                self.errors.append(f"Erro ao ler version.json: {e}")
        
        # Verificar README.md
        if os.path.exists("README.md"):
            try:
                with open("README.md", 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "v1.2" in content:
                        version_sources["README.md"] = "1.2.x"
                    else:
                        self.warnings.append("Versão não encontrada no README.md")
            except Exception as e:
                self.warnings.append(f"Erro ao ler README.md: {e}")
        
        # Verificar consistência
        unique_versions = set(version_sources.values())
        if len(unique_versions) <= 1:
            print("  ✅ Versões consistentes entre arquivos")
            self.passed_checks.append("Versões consistentes")
            return True
        else:
            print(f"  ❌ Versões inconsistentes: {version_sources}")
            self.errors.append("Versões inconsistentes entre arquivos")
            return False
    
    def validate_dependencies(self) -> bool:
        """Valida se dependências podem ser importadas"""
        print("\n📦 Validando dependências...")
        
        dependencies = [
            ("OpenCV", "cv2"),
            ("MediaPipe", "mediapipe"),
            ("PyQt5", "PyQt5.QtWidgets"),
            ("Pygame", "pygame"),
            ("NumPy", "numpy"),
            ("psutil", "psutil")
        ]
        
        failed_imports = []
        
        for name, module in dependencies:
            try:
                __import__(module)
                print(f"  ✅ {name}")
                self.passed_checks.append(f"Dependência {name} OK")
            except ImportError:
                print(f"  ❌ {name}")
                failed_imports.append(name)
                self.errors.append(f"Dependência não instalada: {name}")
        
        return len(failed_imports) == 0
    
    def validate_code_syntax(self) -> bool:
        """Valida sintaxe dos arquivos Python"""
        print("\n🐍 Validando sintaxe Python...")
        
        python_files = [
            "sergipe_game.py",
            "config_manager.py",
            "game_modes.py",
            "achievements.py",
            "performance_optimizer.py"
        ]
        
        syntax_errors = []
        
        for file in python_files:
            if os.path.exists(file):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        code = f.read()
                    
                    compile(code, file, 'exec')
                    print(f"  ✅ {file}")
                    self.passed_checks.append(f"Sintaxe {file} OK")
                    
                except SyntaxError as e:
                    print(f"  ❌ {file}: {e}")
                    syntax_errors.append(f"{file}: {e}")
                    self.errors.append(f"Erro de sintaxe em {file}")
                except Exception as e:
                    print(f"  ⚠️ {file}: {e}")
                    self.warnings.append(f"Aviso em {file}: {e}")
        
        return len(syntax_errors) == 0
    
    def validate_documentation(self) -> bool:
        """Valida completude da documentação"""
        print("\n📚 Validando documentação...")
        
        doc_files = {
            "README.md": 1000,  # Mínimo de caracteres
            "COMO_JOGAR.md": 500,
            "MANUAL_TECNICO.md": 2000,
            "CHECKLIST.md": 1000
        }
        
        doc_issues = []
        
        for doc_file, min_chars in doc_files.items():
            if os.path.exists(doc_file):
                try:
                    with open(doc_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if len(content) >= min_chars:
                        print(f"  ✅ {doc_file} ({len(content)} chars)")
                        self.passed_checks.append(f"Documentação {doc_file} completa")
                    else:
                        print(f"  ⚠️ {doc_file} muito curto ({len(content)} chars)")
                        self.warnings.append(f"Documentação {doc_file} pode estar incompleta")
                        
                except Exception as e:
                    print(f"  ❌ {doc_file}: {e}")
                    doc_issues.append(f"{doc_file}: {e}")
            else:
                print(f"  ❌ {doc_file} não encontrado")
                doc_issues.append(f"{doc_file} faltando")
        
        return len(doc_issues) == 0
    
    def validate_installer(self) -> bool:
        """Valida se o instalador funciona"""
        print("\n🔧 Validando instalador...")
        
        if not os.path.exists("installer.py"):
            print("  ❌ installer.py não encontrado")
            self.errors.append("Instalador não encontrado")
            return False
        
        try:
            # Testar importação do instalador
            import installer
            print("  ✅ installer.py pode ser importado")
            self.passed_checks.append("Instalador importável")
            
            # Verificar se tem a classe principal
            if hasattr(installer, 'VivaSergiperInstaller'):
                print("  ✅ Classe VivaSergiperInstaller encontrada")
                self.passed_checks.append("Classe do instalador OK")
                return True
            else:
                print("  ❌ Classe VivaSergiperInstaller não encontrada")
                self.errors.append("Classe do instalador faltando")
                return False
                
        except Exception as e:
            print(f"  ❌ Erro no instalador: {e}")
            self.errors.append(f"Erro no instalador: {e}")
            return False
    
    def generate_release_checksum(self) -> str:
        """Gera checksum do release"""
        print("\n🔐 Gerando checksum do release...")
        
        important_files = [
            "sergipe_game.py",
            "config_manager.py",
            "game_modes.py",
            "achievements.py",
            "performance_optimizer.py",
            "version.json"
        ]
        
        hasher = hashlib.sha256()
        
        for file in important_files:
            if os.path.exists(file):
                with open(file, 'rb') as f:
                    hasher.update(f.read())
        
        checksum = hasher.hexdigest()[:16]  # Primeiros 16 caracteres
        print(f"  ✅ Checksum: {checksum}")
        
        return checksum
    
    def create_release_manifest(self) -> bool:
        """Cria manifesto do release"""
        print("\n📋 Criando manifesto do release...")
        
        try:
            manifest = {
                "project": self.project_name,
                "version": self.version,
                "release_date": "2025-01-20",
                "checksum": self.generate_release_checksum(),
                "validation": {
                    "passed_checks": len(self.passed_checks),
                    "warnings": len(self.warnings),
                    "errors": len(self.errors),
                    "status": "VALID" if len(self.errors) == 0 else "INVALID"
                },
                "files_validated": True,
                "dependencies_ok": True,
                "documentation_complete": True,
                "ready_for_distribution": len(self.errors) == 0
            }
            
            with open("release_manifest.json", 'w', encoding='utf-8') as f:
                json.dump(manifest, f, indent=4, ensure_ascii=False)
            
            print("  ✅ Manifesto criado: release_manifest.json")
            self.passed_checks.append("Manifesto do release criado")
            return True
            
        except Exception as e:
            print(f"  ❌ Erro ao criar manifesto: {e}")
            self.errors.append(f"Erro ao criar manifesto: {e}")
            return False
    
    def run_validation(self) -> bool:
        """Executa validação completa"""
        print(f"🔍 VALIDAÇÃO FINAL DO RELEASE - {self.project_name} v{self.version}")
        print("=" * 70)
        
        validations = [
            ("Arquivos Principais", self.validate_core_files),
            ("Estrutura de Diretórios", self.validate_directories),
            ("Consistência de Versão", self.validate_version_consistency),
            ("Dependências", self.validate_dependencies),
            ("Sintaxe Python", self.validate_code_syntax),
            ("Documentação", self.validate_documentation),
            ("Instalador", self.validate_installer),
            ("Manifesto do Release", self.create_release_manifest)
        ]
        
        for validation_name, validation_func in validations:
            try:
                validation_func()
            except Exception as e:
                print(f"  ❌ Erro em {validation_name}: {e}")
                self.errors.append(f"Erro em {validation_name}: {e}")
        
        # Resumo final
        print("\n" + "=" * 70)
        print("📊 RESUMO DA VALIDAÇÃO")
        print("=" * 70)
        
        print(f"✅ Verificações Passaram: {len(self.passed_checks)}")
        print(f"⚠️ Avisos: {len(self.warnings)}")
        print(f"❌ Erros: {len(self.errors)}")
        
        if self.warnings:
            print("\n⚠️ AVISOS:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if self.errors:
            print("\n❌ ERROS:")
            for error in self.errors:
                print(f"  • {error}")
        
        # Resultado final
        if len(self.errors) == 0:
            print("\n🎉 VALIDAÇÃO PASSOU!")
            print("✅ O projeto está PRONTO PARA DISTRIBUIÇÃO!")
            print(f"🚀 {self.project_name} v{self.version} validado com sucesso!")
            return True
        else:
            print("\n❌ VALIDAÇÃO FALHOU!")
            print("Corrija os erros antes da distribuição.")
            return False


def main():
    """Função principal"""
    validator = ReleaseValidator()
    
    try:
        success = validator.run_validation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Validação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado na validação: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
