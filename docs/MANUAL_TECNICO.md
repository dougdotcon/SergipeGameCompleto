# 📖 MANUAL TÉCNICO - VIVA SERGIPE!

## 📋 **VISÃO GERAL**

O **VIVA SERGIPE!** é um jogo interativo desenvolvido em Python que utiliza visão computacional e detecção corporal para criar uma experiência única de preenchimento do mapa de Sergipe usando movimentos corporais.

### 🎯 **Arquitetura do Sistema**

```
VIVA SERGIPE! v1.2
├── 🎮 Core Game Engine
│   ├── sergipe_game.py (Jogo principal)
│   ├── sergipe_game_headless.py (Versão controlável)
│   └── game_controller.py (Coordenador)
├── 🖼️ Interface & UX
│   ├── menu_gui.py (Interface PyQt5)
│   ├── config_window.py (Configurações)
│   └── visual_feedback.py (Feedback visual)
├── ⚙️ Core Systems
│   ├── config_manager.py (Configurações)
│   ├── sync_manager.py (Sincronização)
│   └── performance_optimizer.py (Performance)
├── 🎮 Game Features
│   ├── game_modes.py (Modos de jogo)
│   ├── achievements.py (Conquistas)
│   └── analytics.py (Telemetria)
├── 🛠️ Utilities
│   ├── sergipe_utils.py (Funções específicas)
│   ├── utils.py (Funções base)
│   └── updater.py (Atualizações)
└── 📦 Distribution
    └── installer.py (Instalador)
```

---

## 🔧 **COMPONENTES PRINCIPAIS**

### **1. Core Game Engine**

#### **sergipe_game.py**
- **Função**: Ponto de entrada principal do jogo
- **Responsabilidades**:
  - Inicialização do MediaPipe
  - Loop principal do jogo
  - Processamento de frames da câmera
  - Cálculo de preenchimento do mapa
  - Gerenciamento de estados (menu, jogo, vitória)

#### **sergipe_game_headless.py**
- **Função**: Versão controlável do jogo para integração
- **Responsabilidades**:
  - Mesma lógica do jogo principal
  - Interface via filas de comando
  - Controle externo de estados

#### **game_controller.py**
- **Função**: Coordenador entre menu PyQt e jogo OpenCV
- **Responsabilidades**:
  - Gerenciamento de processos
  - Comunicação entre componentes
  - Estados do sistema

### **2. Interface & UX**

#### **menu_gui.py**
- **Função**: Interface principal em PyQt5
- **Responsabilidades**:
  - Menu principal
  - Navegação por teclado
  - Integração com configurações
  - Tela cheia automática

#### **config_window.py**
- **Função**: Interface de configurações avançada
- **Responsabilidades**:
  - 4 abas de configuração
  - Validação de entrada
  - Salvamento automático

#### **visual_feedback.py**
- **Função**: Sistema de feedback visual avançado
- **Responsabilidades**:
  - Análise de qualidade da detecção
  - Indicadores visuais
  - Guias de calibração
  - Mensagens temporárias

### **3. Core Systems**

#### **config_manager.py**
- **Função**: Gerenciamento de configurações persistentes
- **Responsabilidades**:
  - Carregamento/salvamento em JSON
  - Configurações padrão
  - Estatísticas do jogador
  - Validação de dados

#### **sync_manager.py**
- **Função**: Sincronização robusta entre componentes
- **Responsabilidades**:
  - Gerenciamento de processos
  - Prevenção de processos órfãos
  - Cleanup automático
  - Monitoramento de threads

#### **performance_optimizer.py**
- **Função**: Otimização adaptativa de performance
- **Responsabilidades**:
  - Detecção de hardware
  - Ajuste dinâmico de qualidade
  - Monitoramento de recursos
  - Otimização de frames

---

## 🏗️ **FLUXO DE EXECUÇÃO**

### **1. Inicialização**
```python
1. sergipe_game.py inicia
2. Carrega config_manager
3. Inicializa todos os managers
4. Detecta hardware (performance_optimizer)
5. Carrega modo de jogo atual
6. Inicializa MediaPipe
7. Configura câmera
8. Inicia loop principal
```

### **2. Loop Principal**
```python
while True:
    1. Captura frame da câmera
    2. Aplica otimizações de performance
    3. Processa com MediaPipe (se não skip)
    4. Cria máscara corporal
    5. Calcula preenchimento
    6. Aplica feedback visual
    7. Verifica condições de vitória/derrota
    8. Atualiza interface
    9. Processa eventos de teclado
```

### **3. Finalização**
```python
1. Salva estatísticas
2. Verifica conquistas
3. Finaliza analytics
4. Cleanup de recursos
5. Para monitoramento
6. Fecha OpenCV/Pygame
```

---

## 📊 **ESTRUTURA DE DADOS**

### **Configurações (config.json)**
```json
{
    "game": {
        "duration": 300,
        "win_threshold": 30.0,
        "min_body_pixels": 1000,
        "current_mode": "classic"
    },
    "audio": {
        "master_volume": 0.7,
        "music_volume": 0.5
    },
    "visual": {
        "show_percentage": true,
        "camera_mirror": true
    },
    "stats": {
        "games_played": 0,
        "games_won": 0
    }
}
```

### **Modos de Jogo**
```python
GameMode.CLASSIC: {
    "duration": 300,
    "win_threshold": 30.0,
    "difficulty": "normal"
}
```

### **Conquistas**
```python
Achievement: {
    "name": "Título",
    "description": "Descrição",
    "condition": {"games_won": 5},
    "reward_points": 75
}
```

---

## 🔌 **APIs E INTERFACES**

### **Config Manager API**
```python
# Obter configuração
value = config_manager.get('section', 'key', default)

# Definir configuração
config_manager.set('section', 'key', value, save=True)

# Atualizar estatísticas
config_manager.update_stats(games_played=1, games_won=1)
```

### **Game Mode Manager API**
```python
# Definir modo
game_mode_manager.set_current_mode(GameMode.SPEEDRUN)

# Obter configurações do modo
settings = game_mode_manager.get_game_settings_for_mode()

# Verificar desbloqueio
unlocked = game_mode_manager.is_mode_unlocked(mode, stats)
```

### **Achievement Manager API**
```python
# Verificar conquistas
newly_unlocked = achievement_manager.check_achievements(game_data)

# Obter progresso
progress = achievement_manager.get_achievement_progress()
```

### **Performance Optimizer API**
```python
# Otimizar frame
optimized_frame = optimizer.optimize_frame_processing(frame)

# Verificar skip
should_skip = optimizer.should_skip_frame(frame_count)

# Atualizar métricas
optimizer.update_performance_metrics(fps, processing_time)
```

---

## 🧪 **SISTEMA DE TESTES**

### **Estrutura de Testes**
```
tests/
├── test_sergipe.py (Funcionalidades principais)
├── test_config.py (Sistema de configurações)
├── test_visual_feedback.py (Feedback visual)
├── test_v1.2_features.py (Funcionalidades v1.2)
└── test_integration.py (Testes de integração)
```

### **Executar Testes**
```bash
# Teste individual
python test_config.py

# Todos os testes
python -m pytest tests/

# Com cobertura
python -m pytest --cov=. tests/
```

---

## 📦 **DEPENDÊNCIAS**

### **Principais**
- **OpenCV** (>=4.5.0): Processamento de imagem e câmera
- **MediaPipe** (>=0.8.0): Detecção corporal
- **PyQt5** (>=5.15.0): Interface gráfica
- **Pygame** (>=2.0.0): Áudio e eventos
- **NumPy** (>=1.20.0): Operações matemáticas
- **psutil** (>=5.8.0): Monitoramento do sistema

### **Instalação**
```bash
pip install -r requirements.txt
```

---

## 🚀 **DEPLOYMENT**

### **Instalação Automática**
```bash
python installer.py
```

### **Distribuição Manual**
1. Copiar todos os arquivos .py
2. Copiar diretórios assets/ e sounds/
3. Instalar dependências
4. Executar sergipe_game.py

### **Empacotamento (PyInstaller)**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed sergipe_game.py
```

---

## 🔧 **CONFIGURAÇÃO DE DESENVOLVIMENTO**

### **Ambiente de Desenvolvimento**
```bash
# Clonar projeto
git clone <repository>

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar testes
python test_config.py
```

### **Estrutura de Diretórios**
```
VIVA_SERGIPE/
├── *.py (Arquivos principais)
├── assets/ (Imagens e recursos)
├── sounds/ (Arquivos de áudio)
├── snapshots/ (Fotos de vitória)
├── backup/ (Backups automáticos)
├── logs/ (Logs do sistema)
└── config/ (Configurações)
```

---

## 🐛 **DEBUGGING E TROUBLESHOOTING**

### **Logs do Sistema**
- Logs automáticos em `logs/`
- Verbose mode: `python sergipe_game.py --verbose`

### **Problemas Comuns**

#### **Câmera não detectada**
```python
# Verificar câmeras disponíveis
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Câmera {i} disponível")
        cap.release()
```

#### **Performance baixa**
- Verificar hardware com `performance_optimizer`
- Ajustar qualidade nas configurações
- Reduzir resolução da câmera

#### **Erro de importação**
```bash
# Reinstalar dependências
pip install --force-reinstall -r requirements.txt
```

---

## 📈 **MÉTRICAS E MONITORAMENTO**

### **Performance Metrics**
- FPS médio/mínimo/máximo
- Tempo de processamento de frame
- Uso de CPU e memória
- Qualidade de detecção

### **Analytics (Opcional)**
- Sessões de jogo
- Conquistas desbloqueadas
- Uso de funcionalidades
- Métricas de performance

---

## 🔮 **EXTENSIBILIDADE**

### **Adicionar Novo Modo de Jogo**
```python
# Em game_modes.py
NEW_MODE = {
    "name": "🆕 Novo Modo",
    "description": "Descrição do modo",
    "duration": 180,
    "win_threshold": 40.0,
    "unlock_condition": {"games_won": 15}
}
```

### **Adicionar Nova Conquista**
```python
# Em achievements.py
"new_achievement": {
    "name": "🏆 Nova Conquista",
    "description": "Descrição da conquista",
    "condition": {"custom_metric": 100},
    "reward_points": 150
}
```

### **Adicionar Nova Configuração**
```python
# Em config_manager.py - default_config
"new_section": {
    "new_setting": "default_value"
}
```

---

## 📚 **RECURSOS ADICIONAIS**

### **Documentação**
- `README.md` - Visão geral do projeto
- `COMO_JOGAR.md` - Manual do usuário
- `CHECKLIST.md` - Status do projeto
- `VERSAO_1.2_FINAL.md` - Resumo da versão

### **Ferramentas de Desenvolvimento**
- `fix_opencv.py` - Correção de problemas do OpenCV
- `installer.py` - Instalador automático
- `updater.py` - Sistema de atualizações

### **Suporte**
- Issues no GitHub
- Documentação técnica
- Exemplos de código
- Testes automatizados

---

*Manual Técnico v1.2 - Janeiro 2025*
*Para desenvolvedores do VIVA SERGIPE!*
