"""
GERENCIADOR DE SINCRONIZAÇÃO - VIVA SERGIPE!
Sistema para melhorar a sincronização entre PyQt e OpenCV
"""

import threading
import time
import queue
import signal
import sys
import os
from typing import Optional, Dict, Any, Callable
from enum import Enum
import weakref


class ProcessState(Enum):
    """Estados dos processos"""
    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"


class SyncManager:
    """Gerenciador de sincronização entre componentes"""
    
    def __init__(self):
        self.processes = {}
        self.command_queues = {}
        self.result_queues = {}
        self.state_callbacks = {}
        self.cleanup_callbacks = []
        self.running = True
        self.lock = threading.RLock()
        
        # Configurar handler para sinais do sistema
        self._setup_signal_handlers()
        
        # Thread de monitoramento
        self.monitor_thread = None
        self.start_monitoring()
    
    def _setup_signal_handlers(self):
        """Configura handlers para sinais do sistema"""
        def signal_handler(signum, frame):
            print(f"Recebido sinal {signum}, iniciando shutdown...")
            self.shutdown()
            sys.exit(0)
        
        # Registrar handlers para diferentes sinais
        try:
            signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
            signal.signal(signal.SIGTERM, signal_handler)  # Termination
            if hasattr(signal, 'SIGBREAK'):  # Windows
                signal.signal(signal.SIGBREAK, signal_handler)
        except Exception as e:
            print(f"Aviso: Não foi possível configurar signal handlers: {e}")
    
    def register_process(self, process_id: str, command_queue: queue.Queue, 
                        result_queue: queue.Queue, state_callback: Optional[Callable] = None):
        """
        Registra um processo para monitoramento
        
        Args:
            process_id: ID único do processo
            command_queue: Fila de comandos para o processo
            result_queue: Fila de resultados do processo
            state_callback: Callback para mudanças de estado
        """
        with self.lock:
            self.processes[process_id] = {
                "state": ProcessState.IDLE,
                "thread": None,
                "last_heartbeat": time.time(),
                "start_time": None,
                "error_count": 0
            }
            
            self.command_queues[process_id] = command_queue
            self.result_queues[process_id] = result_queue
            
            if state_callback:
                self.state_callbacks[process_id] = state_callback
            
            print(f"Processo '{process_id}' registrado no SyncManager")
    
    def start_process(self, process_id: str, target_function: Callable, 
                     args: tuple = (), daemon: bool = True) -> bool:
        """
        Inicia um processo registrado
        
        Args:
            process_id: ID do processo
            target_function: Função para executar
            args: Argumentos para a função
            daemon: Se a thread deve ser daemon
            
        Returns:
            bool: True se iniciou com sucesso
        """
        with self.lock:
            if process_id not in self.processes:
                print(f"Erro: Processo '{process_id}' não registrado")
                return False
            
            process_info = self.processes[process_id]
            
            if process_info["state"] in [ProcessState.RUNNING, ProcessState.STARTING]:
                print(f"Processo '{process_id}' já está rodando")
                return True
            
            try:
                # Criar e iniciar thread
                thread = threading.Thread(
                    target=self._process_wrapper,
                    args=(process_id, target_function, args),
                    daemon=daemon,
                    name=f"Process-{process_id}"
                )
                
                process_info["thread"] = thread
                process_info["state"] = ProcessState.STARTING
                process_info["start_time"] = time.time()
                process_info["error_count"] = 0
                
                thread.start()
                
                # Notificar callback
                self._notify_state_change(process_id, ProcessState.STARTING)
                
                print(f"Processo '{process_id}' iniciado")
                return True
                
            except Exception as e:
                print(f"Erro ao iniciar processo '{process_id}': {e}")
                process_info["state"] = ProcessState.ERROR
                self._notify_state_change(process_id, ProcessState.ERROR)
                return False
    
    def stop_process(self, process_id: str, timeout: float = 5.0) -> bool:
        """
        Para um processo registrado
        
        Args:
            process_id: ID do processo
            timeout: Timeout em segundos
            
        Returns:
            bool: True se parou com sucesso
        """
        with self.lock:
            if process_id not in self.processes:
                print(f"Processo '{process_id}' não encontrado")
                return False
            
            process_info = self.processes[process_id]
            
            if process_info["state"] in [ProcessState.STOPPED, ProcessState.STOPPING]:
                return True
            
            try:
                # Enviar comando de parada
                command_queue = self.command_queues.get(process_id)
                if command_queue:
                    command_queue.put({"action": "stop"})
                
                process_info["state"] = ProcessState.STOPPING
                self._notify_state_change(process_id, ProcessState.STOPPING)
                
                # Aguardar thread terminar
                thread = process_info["thread"]
                if thread and thread.is_alive():
                    thread.join(timeout)
                    
                    if thread.is_alive():
                        print(f"Aviso: Processo '{process_id}' não terminou no timeout")
                        return False
                
                process_info["state"] = ProcessState.STOPPED
                process_info["thread"] = None
                self._notify_state_change(process_id, ProcessState.STOPPED)
                
                print(f"Processo '{process_id}' parado")
                return True
                
            except Exception as e:
                print(f"Erro ao parar processo '{process_id}': {e}")
                return False
    
    def send_command(self, process_id: str, command: Dict[str, Any], 
                    timeout: Optional[float] = None) -> bool:
        """
        Envia comando para um processo
        
        Args:
            process_id: ID do processo
            command: Comando para enviar
            timeout: Timeout opcional
            
        Returns:
            bool: True se enviou com sucesso
        """
        try:
            command_queue = self.command_queues.get(process_id)
            if not command_queue:
                print(f"Fila de comandos não encontrada para '{process_id}'")
                return False
            
            if timeout:
                command_queue.put(command, timeout=timeout)
            else:
                command_queue.put(command)
            
            return True
            
        except queue.Full:
            print(f"Fila de comandos cheia para '{process_id}'")
            return False
        except Exception as e:
            print(f"Erro ao enviar comando para '{process_id}': {e}")
            return False
    
    def get_result(self, process_id: str, timeout: float = 1.0) -> Optional[Dict[str, Any]]:
        """
        Obtém resultado de um processo
        
        Args:
            process_id: ID do processo
            timeout: Timeout em segundos
            
        Returns:
            Dict com resultado ou None
        """
        try:
            result_queue = self.result_queues.get(process_id)
            if not result_queue:
                return None
            
            return result_queue.get(timeout=timeout)
            
        except queue.Empty:
            return None
        except Exception as e:
            print(f"Erro ao obter resultado de '{process_id}': {e}")
            return None
    
    def get_process_state(self, process_id: str) -> Optional[ProcessState]:
        """
        Obtém estado de um processo
        
        Args:
            process_id: ID do processo
            
        Returns:
            ProcessState ou None
        """
        with self.lock:
            process_info = self.processes.get(process_id)
            return process_info["state"] if process_info else None
    
    def is_process_running(self, process_id: str) -> bool:
        """
        Verifica se um processo está rodando
        
        Args:
            process_id: ID do processo
            
        Returns:
            bool: True se está rodando
        """
        state = self.get_process_state(process_id)
        return state == ProcessState.RUNNING
    
    def _process_wrapper(self, process_id: str, target_function: Callable, args: tuple):
        """
        Wrapper para executar processo com monitoramento
        
        Args:
            process_id: ID do processo
            target_function: Função para executar
            args: Argumentos da função
        """
        try:
            with self.lock:
                self.processes[process_id]["state"] = ProcessState.RUNNING
            
            self._notify_state_change(process_id, ProcessState.RUNNING)
            
            # Executar função
            target_function(*args)
            
        except Exception as e:
            print(f"Erro no processo '{process_id}': {e}")
            with self.lock:
                self.processes[process_id]["state"] = ProcessState.ERROR
                self.processes[process_id]["error_count"] += 1
            
            self._notify_state_change(process_id, ProcessState.ERROR)
            
        finally:
            with self.lock:
                if self.processes[process_id]["state"] != ProcessState.ERROR:
                    self.processes[process_id]["state"] = ProcessState.STOPPED
                self.processes[process_id]["thread"] = None
            
            if self.processes[process_id]["state"] != ProcessState.ERROR:
                self._notify_state_change(process_id, ProcessState.STOPPED)
    
    def _notify_state_change(self, process_id: str, new_state: ProcessState):
        """
        Notifica callback sobre mudança de estado
        
        Args:
            process_id: ID do processo
            new_state: Novo estado
        """
        callback = self.state_callbacks.get(process_id)
        if callback:
            try:
                callback(process_id, new_state)
            except Exception as e:
                print(f"Erro no callback de estado para '{process_id}': {e}")
    
    def start_monitoring(self):
        """Inicia thread de monitoramento"""
        if self.monitor_thread and self.monitor_thread.is_alive():
            return
        
        self.monitor_thread = threading.Thread(
            target=self._monitor_processes,
            daemon=True,
            name="SyncManager-Monitor"
        )
        self.monitor_thread.start()
    
    def _monitor_processes(self):
        """Loop de monitoramento dos processos"""
        while self.running:
            try:
                with self.lock:
                    current_time = time.time()
                    
                    for process_id, process_info in self.processes.items():
                        # Verificar se thread ainda está viva
                        thread = process_info["thread"]
                        if thread and not thread.is_alive():
                            if process_info["state"] == ProcessState.RUNNING:
                                print(f"Processo '{process_id}' terminou inesperadamente")
                                process_info["state"] = ProcessState.STOPPED
                                process_info["thread"] = None
                                self._notify_state_change(process_id, ProcessState.STOPPED)
                        
                        # Verificar timeout de inicialização
                        if (process_info["state"] == ProcessState.STARTING and 
                            process_info["start_time"] and
                            current_time - process_info["start_time"] > 30):
                            print(f"Timeout na inicialização do processo '{process_id}'")
                            process_info["state"] = ProcessState.ERROR
                            self._notify_state_change(process_id, ProcessState.ERROR)
                
                time.sleep(1.0)  # Verificar a cada segundo
                
            except Exception as e:
                print(f"Erro no monitoramento: {e}")
                time.sleep(5.0)
    
    def add_cleanup_callback(self, callback: Callable):
        """
        Adiciona callback para limpeza
        
        Args:
            callback: Função para chamar na limpeza
        """
        self.cleanup_callbacks.append(callback)
    
    def shutdown(self):
        """Para todos os processos e faz limpeza"""
        print("Iniciando shutdown do SyncManager...")
        
        self.running = False
        
        # Parar todos os processos
        with self.lock:
            process_ids = list(self.processes.keys())
        
        for process_id in process_ids:
            print(f"Parando processo '{process_id}'...")
            self.stop_process(process_id, timeout=3.0)
        
        # Executar callbacks de limpeza
        for callback in self.cleanup_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Erro no callback de limpeza: {e}")
        
        # Parar thread de monitoramento
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=2.0)
        
        print("Shutdown do SyncManager concluído")
    
    def get_status_report(self) -> Dict[str, Any]:
        """
        Obtém relatório de status de todos os processos
        
        Returns:
            Dict com status de todos os processos
        """
        with self.lock:
            report = {
                "running": self.running,
                "processes": {}
            }
            
            for process_id, process_info in self.processes.items():
                thread = process_info["thread"]
                report["processes"][process_id] = {
                    "state": process_info["state"].value,
                    "thread_alive": thread.is_alive() if thread else False,
                    "error_count": process_info["error_count"],
                    "start_time": process_info["start_time"]
                }
            
            return report


# Instância global do gerenciador de sincronização
sync_manager = SyncManager()


def get_sync_manager() -> SyncManager:
    """
    Obtém a instância global do gerenciador de sincronização
    
    Returns:
        SyncManager: Instância do gerenciador
    """
    return sync_manager


def cleanup_on_exit():
    """Função para limpeza automática na saída"""
    sync_manager.shutdown()


# Registrar limpeza automática
import atexit
atexit.register(cleanup_on_exit)
