# Estrutura Organizada do Projeto Viva Sergipe!

## 📁 Estrutura de Pastas

```
SERGIPE-SE/
├── main.py                    # Ponto de entrada principal do jogo
├── VIVA_SERGIPE.bat          # Script de inicialização para Windows
├── requirements.txt           # Dependências do projeto
├── README.md                  # Documentação principal
├── LICENSE                    # Licença do projeto
├── logo.png                   # Logo do jogo
│
├── src/                       # Código fonte principal
│   ├── __init__.py           # Módulo Python
│   ├── sergipe_game.py       # Jogo principal
│   ├── sergipe_game_headless.py  # Versão headless do jogo
│   ├── sergipe_utils.py      # Utilitários do jogo
│   ├── menu_gui.py           # Interface gráfica do menu
│   ├── play.py               # Lógica de jogo
│   ├── game_controller.py    # Controlador do jogo
│   ├── game_modes.py         # Modos de jogo
│   ├── config_window.py      # Janela de configuração
│   ├── config_manager.py     # Gerenciador de configurações
│   ├── visual_feedback.py    # Feedback visual
│   ├── achievements.py       # Sistema de conquistas
│   ├── analytics.py          # Análise de dados
│   ├── performance_optimizer.py  # Otimização de performance
│   ├── sync_manager.py       # Gerenciador de sincronização
│   ├── utils.py              # Utilitários gerais
│   └── start_game.py         # Script de inicialização
│
├── tests/                     # Arquivos de teste
│   ├── test_installation.py
│   ├── test_v1.2_features.py
│   ├── test_visual_feedback.py
│   ├── test_config.py
│   ├── test_final_system.py
│   ├── test_menu.py
│   ├── test_visual.py
│   └── test_sergipe.py
│
├── scripts/                   # Scripts utilitários
│   ├── installer.py          # Instalador do jogo
│   ├── updater.py            # Atualizador
│   ├── fix_opencv.py         # Correção do OpenCV
│   └── collect_data.py       # Coleta de dados
│
├── config/                    # Arquivos de configuração
│   ├── config.json           # Configurações do jogo
│   ├── version.json          # Informações de versão
│   └── system_report.json    # Relatório do sistema
│
├── build/                     # Arquivos de build e release
│   ├── build.py              # Script de build
│   ├── create_final_release.py  # Criação de release
│   ├── validate_release.py   # Validação de release
│   └── release_manifest.json # Manifesto de release
│
├── assets/                    # Recursos visuais
│   ├── background*.webp      # Imagens de fundo
│   ├── contorno-mapa-SE.png  # Mapa de Sergipe
│   └── flag-se.jpg           # Bandeira de Sergipe
│
├── sounds/                    # Arquivos de áudio
│   ├── background.mp3        # Música de fundo
│   ├── point.mp3             # Som de ponto
│   ├── game_over*.mp3        # Sons de fim de jogo
│   └── *.mp3                 # Outros sons
│
├── model/                     # Modelos de IA
│   └── model_strike_a_pose.h5 # Modelo treinado
│
├── train_model/               # Dados de treinamento
│   ├── train_model.ipynb     # Notebook de treinamento
│   ├── training_data/        # Dados de treinamento
│   └── test_data/            # Dados de teste
│
├── docs/                      # Documentação
│   ├── README_SERGIPE.md     # Documentação do jogo
│   ├── MANUAL_TECNICO.md     # Manual técnico
│   ├── COMO_JOGAR.md         # Instruções de jogo
│   └── *.md                  # Outros documentos
│
└── snapshots/                 # Snapshots do sistema
```

## 🚀 Como Executar

### Opção 1: Arquivo Principal
```bash
python main.py
```

### Opção 2: Script Windows
```bash
VIVA_SERGIPE.bat
```

### Opção 3: Execução Direta
```bash
python src/start_game.py
```

## 🔧 Scripts Utilitários

### Instalar Dependências
```bash
python scripts/fix_opencv.py
```

### Atualizar Jogo
```bash
python scripts/updater.py
```

### Coletar Dados
```bash
python scripts/collect_data.py
```

## 🧪 Executar Testes

```bash
# Executar todos os testes
python -m pytest tests/

# Executar teste específico
python tests/test_installation.py
```

## 📦 Build e Release

```bash
# Criar build
python build/build.py

# Criar release final
python build/create_final_release.py

# Validar release
python build/validate_release.py
```

## 📋 Benefícios da Nova Estrutura

1. **Organização Clara**: Separação lógica entre código, testes, scripts e configurações
2. **Manutenibilidade**: Fácil localização e modificação de arquivos
3. **Escalabilidade**: Estrutura preparada para crescimento do projeto
4. **Colaboração**: Melhor organização para trabalho em equipe
5. **Deploy**: Estrutura otimizada para distribuição e instalação

## 🔄 Migração

Todos os imports foram atualizados para funcionar com a nova estrutura. O arquivo `main.py` na raiz serve como ponto de entrada principal, mantendo a compatibilidade com a execução anterior. 