"""
SISTEMA DE ATUALIZAÇÕES - VIVA SERGIPE!
Sistema para verificar e aplicar atualizações automaticamente
"""

import os
import json
import urllib.request
import urllib.error
import shutil
import zipfile
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import hashlib
import time
from config_manager import get_config_manager


class UpdateManager:
    """Gerenciador de atualizações"""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.current_version = "1.2.0"
        self.update_server = "https://api.github.com/repos/viva-sergipe/releases"  # Exemplo
        self.local_version_file = "version.json"
        self.backup_dir = Path("backup")
        
    def get_current_version(self) -> str:
        """Obtém versão atual do jogo"""
        try:
            if os.path.exists(self.local_version_file):
                with open(self.local_version_file, 'r', encoding='utf-8') as f:
                    version_data = json.load(f)
                    return version_data.get('version', self.current_version)
        except:
            pass
        
        return self.current_version
    
    def save_version_info(self, version: str, changelog: str = ""):
        """Salva informações da versão atual"""
        version_data = {
            'version': version,
            'update_date': time.strftime('%Y-%m-%d %H:%M:%S'),
            'changelog': changelog
        }
        
        try:
            with open(self.local_version_file, 'w', encoding='utf-8') as f:
                json.dump(version_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar informações da versão: {e}")
    
    def check_for_updates(self) -> Optional[Dict[str, Any]]:
        """
        Verifica se há atualizações disponíveis
        
        Returns:
            Dict com informações da atualização ou None se não houver
        """
        try:
            print("🔍 Verificando atualizações...")
            
            # Simular verificação de atualização (em produção, consultaria servidor real)
            # Por enquanto, retorna None (sem atualizações)
            
            # Exemplo de como seria a implementação real:
            """
            request = urllib.request.Request(self.update_server)
            request.add_header('User-Agent', 'VIVA-SERGIPE-Updater/1.0')
            
            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data and len(data) > 0:
                    latest_release = data[0]
                    latest_version = latest_release['tag_name'].lstrip('v')
                    
                    if self._is_newer_version(latest_version, self.get_current_version()):
                        return {
                            'version': latest_version,
                            'download_url': latest_release['zipball_url'],
                            'changelog': latest_release['body'],
                            'release_date': latest_release['published_at']
                        }
            """
            
            print("✅ Nenhuma atualização disponível")
            return None
            
        except urllib.error.URLError:
            print("⚠️ Não foi possível verificar atualizações (sem conexão)")
            return None
        except Exception as e:
            print(f"⚠️ Erro ao verificar atualizações: {e}")
            return None
    
    def _is_newer_version(self, remote_version: str, local_version: str) -> bool:
        """
        Compara versões para determinar se a remota é mais nova
        
        Args:
            remote_version: Versão remota (ex: "1.3.0")
            local_version: Versão local (ex: "1.2.0")
            
        Returns:
            True se a versão remota for mais nova
        """
        try:
            remote_parts = [int(x) for x in remote_version.split('.')]
            local_parts = [int(x) for x in local_version.split('.')]
            
            # Normalizar tamanhos
            max_len = max(len(remote_parts), len(local_parts))
            remote_parts.extend([0] * (max_len - len(remote_parts)))
            local_parts.extend([0] * (max_len - len(local_parts)))
            
            return remote_parts > local_parts
            
        except ValueError:
            return False
    
    def create_backup(self) -> bool:
        """
        Cria backup da instalação atual
        
        Returns:
            True se o backup foi criado com sucesso
        """
        try:
            print("💾 Criando backup da versão atual...")
            
            # Criar diretório de backup
            self.backup_dir.mkdir(exist_ok=True)
            
            # Lista de arquivos importantes para backup
            important_files = [
                "sergipe_game.py",
                "config_manager.py",
                "config.json",
                "version.json"
            ]
            
            backup_timestamp = time.strftime('%Y%m%d_%H%M%S')
            backup_subdir = self.backup_dir / f"backup_{backup_timestamp}"
            backup_subdir.mkdir(exist_ok=True)
            
            # Copiar arquivos importantes
            for file in important_files:
                if os.path.exists(file):
                    shutil.copy2(file, backup_subdir)
            
            # Copiar diretórios importantes
            important_dirs = ["assets", "sounds", "snapshots"]
            for dir_name in important_dirs:
                if os.path.exists(dir_name):
                    shutil.copytree(dir_name, backup_subdir / dir_name, dirs_exist_ok=True)
            
            print(f"✅ Backup criado em: {backup_subdir}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return False
    
    def download_update(self, update_info: Dict[str, Any]) -> Optional[Path]:
        """
        Baixa atualização do servidor
        
        Args:
            update_info: Informações da atualização
            
        Returns:
            Caminho do arquivo baixado ou None se falhou
        """
        try:
            download_url = update_info['download_url']
            version = update_info['version']
            
            print(f"📥 Baixando versão {version}...")
            
            # Criar diretório temporário
            temp_dir = Path(tempfile.mkdtemp())
            download_path = temp_dir / f"viva_sergipe_v{version}.zip"
            
            # Baixar arquivo
            urllib.request.urlretrieve(download_url, download_path)
            
            print("✅ Download concluído")
            return download_path
            
        except Exception as e:
            print(f"❌ Erro no download: {e}")
            return None
    
    def apply_update(self, update_file: Path, update_info: Dict[str, Any]) -> bool:
        """
        Aplica atualização baixada
        
        Args:
            update_file: Caminho do arquivo de atualização
            update_info: Informações da atualização
            
        Returns:
            True se a atualização foi aplicada com sucesso
        """
        try:
            print("🔄 Aplicando atualização...")
            
            # Extrair atualização
            with zipfile.ZipFile(update_file, 'r') as zip_ref:
                temp_extract_dir = update_file.parent / "extracted"
                zip_ref.extractall(temp_extract_dir)
            
            # Encontrar diretório principal extraído
            extracted_dirs = [d for d in temp_extract_dir.iterdir() if d.is_dir()]
            if not extracted_dirs:
                print("❌ Estrutura de atualização inválida")
                return False
            
            source_dir = extracted_dirs[0]
            
            # Copiar arquivos atualizados
            for item in source_dir.rglob('*'):
                if item.is_file():
                    relative_path = item.relative_to(source_dir)
                    target_path = Path(relative_path)
                    
                    # Criar diretórios se necessário
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copiar arquivo
                    shutil.copy2(item, target_path)
            
            # Atualizar informações da versão
            self.save_version_info(
                update_info['version'],
                update_info.get('changelog', '')
            )
            
            print("✅ Atualização aplicada com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao aplicar atualização: {e}")
            return False
    
    def restore_backup(self, backup_path: Path) -> bool:
        """
        Restaura backup em caso de falha na atualização
        
        Args:
            backup_path: Caminho do backup
            
        Returns:
            True se o backup foi restaurado com sucesso
        """
        try:
            print("🔄 Restaurando backup...")
            
            # Copiar arquivos do backup
            for item in backup_path.rglob('*'):
                if item.is_file():
                    relative_path = item.relative_to(backup_path)
                    target_path = Path(relative_path)
                    
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, target_path)
            
            print("✅ Backup restaurado com sucesso")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao restaurar backup: {e}")
            return False
    
    def cleanup_old_backups(self, keep_count: int = 5):
        """
        Remove backups antigos, mantendo apenas os mais recentes
        
        Args:
            keep_count: Número de backups para manter
        """
        try:
            if not self.backup_dir.exists():
                return
            
            # Listar backups ordenados por data
            backups = sorted(
                [d for d in self.backup_dir.iterdir() if d.is_dir()],
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            # Remover backups antigos
            for backup in backups[keep_count:]:
                shutil.rmtree(backup)
                print(f"🗑️ Backup antigo removido: {backup.name}")
                
        except Exception as e:
            print(f"⚠️ Erro ao limpar backups: {e}")
    
    def auto_update(self) -> bool:
        """
        Executa processo completo de atualização automática
        
        Returns:
            True se a atualização foi bem-sucedida ou não era necessária
        """
        try:
            # Verificar se atualizações automáticas estão habilitadas
            auto_update_enabled = self.config_manager.get('updates', 'auto_update', True)
            if not auto_update_enabled:
                print("🔒 Atualizações automáticas desabilitadas")
                return True
            
            # Verificar atualizações
            update_info = self.check_for_updates()
            if not update_info:
                return True  # Sem atualizações
            
            print(f"🆕 Nova versão disponível: {update_info['version']}")
            
            # Criar backup
            if not self.create_backup():
                print("❌ Falha ao criar backup, cancelando atualização")
                return False
            
            # Baixar atualização
            update_file = self.download_update(update_info)
            if not update_file:
                print("❌ Falha no download, cancelando atualização")
                return False
            
            # Aplicar atualização
            if self.apply_update(update_file, update_info):
                print("🎉 Atualização aplicada com sucesso!")
                
                # Limpar arquivos temporários
                shutil.rmtree(update_file.parent)
                
                # Limpar backups antigos
                self.cleanup_old_backups()
                
                return True
            else:
                print("❌ Falha ao aplicar atualização")
                return False
                
        except Exception as e:
            print(f"❌ Erro na atualização automática: {e}")
            return False
    
    def manual_update_check(self) -> Dict[str, Any]:
        """
        Verificação manual de atualizações com mais detalhes
        
        Returns:
            Dict com informações sobre atualizações
        """
        result = {
            'current_version': self.get_current_version(),
            'update_available': False,
            'update_info': None,
            'last_check': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        update_info = self.check_for_updates()
        if update_info:
            result['update_available'] = True
            result['update_info'] = update_info
        
        # Salvar informações da última verificação
        self.config_manager.set('updates', 'last_check', result['last_check'])
        
        return result


# Instância global do gerenciador de atualizações
update_manager = UpdateManager()


def get_update_manager() -> UpdateManager:
    """
    Obtém a instância global do gerenciador de atualizações
    
    Returns:
        UpdateManager: Instância do gerenciador
    """
    return update_manager


def check_updates_on_startup():
    """Verifica atualizações na inicialização do jogo"""
    try:
        # Verificar se deve verificar atualizações
        config = get_config_manager()
        last_check = config.get('updates', 'last_check', '')
        
        # Verificar apenas uma vez por dia
        if last_check:
            from datetime import datetime, timedelta
            try:
                last_check_date = datetime.strptime(last_check, '%Y-%m-%d %H:%M:%S')
                if datetime.now() - last_check_date < timedelta(days=1):
                    return  # Já verificou hoje
            except:
                pass
        
        # Verificar atualizações em background
        import threading
        
        def background_check():
            update_manager.manual_update_check()
        
        thread = threading.Thread(target=background_check, daemon=True)
        thread.start()
        
    except Exception as e:
        print(f"Erro na verificação de atualizações: {e}")
