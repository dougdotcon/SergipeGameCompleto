# 🕹️ VIVA SERGIPE!

**Jogo interativo de preenchimento corporal baseado no mapa de Sergipe**
*Adaptado da base do projeto STRIKE A POSE!*

<p align="center">
    🎯 <strong>Objetivo:</strong> Use seu corpo para preencher ≥30% do contorno do mapa de Sergipe em 5 minutos!
</p>

## ✨ **NOVIDADES - Versão 2.0**
- **🎨 Menu PyQt Elegante**: Interface gráfica moderna com background da bandeira de Sergipe
- **📝 Texto Melhorado**: Formatação aprimorada com contornos e sombras para melhor legibilidade
- **🎮 Interface Intuitiva**: Menu principal com botões interativos e animações
- **📖 Instruções Integradas**: Tutorial completo acessível diretamente do menu
- **🎵 Áudio Aprimorado**: Sons de menu e feedback sonoro melhorados
- **🎯 Meta Ajustada**: Objetivo reduzido para 30% (mais acessível)

---

## 🎮 **Como Jogar**

### **Objetivo do Jogo**
- Posicione-se em frente à câmera
- Use movimentos corporais para "preencher" o contorno do mapa de Sergipe
- Alcance **95% de preenchimento** em **5 minutos** para vencer!
- Quando vencer, uma foto será automaticamente salva

### **Controles**
- **SPACE**: Iniciar/Reiniciar jogo
- **Q** ou **ESC**: Sair do jogo
- **R**: Reiniciar aplicação

---

## 🚀 **Instalação e Execução**

### **Pré-requisitos**
```bash
pip install -r requirements.txt
# ou manualmente:
pip install opencv-python mediapipe numpy pygame PyQt5
```

### **Executar o Jogo**
```bash
python sergipe_game.py
```

### **Testar Menu PyQt**
```bash
python test_menu.py
```

### **Testar Funcionalidades**
```bash
python test_sergipe.py
```

---

## 🏗️ **Arquitetura Técnica**

### **Base Tecnológica**
- **OpenCV**: Captura e processamento de vídeo
- **MediaPipe**: Detecção de poses corporais em tempo real
- **NumPy**: Cálculos de máscaras e sobreposição
- **Pygame**: Sistema de áudio e interface

### **Algoritmo Principal**
1. **Detecção Corporal**: MediaPipe identifica landmarks do corpo
2. **Criação de Máscara**: Convex hull dos landmarks forma silhueta corporal
3. **Cálculo de Sobreposição**: Interseção entre máscara corporal e contorno do mapa
4. **Percentual de Preenchimento**: `(pixels_sobrepostos / pixels_contorno) × 100`

### **Estrutura de Arquivos**
```
SERGIPE-SE/
├── sergipe_game.py          # Arquivo principal do jogo
├── menu_gui.py              # Interface PyQt do menu principal
├── sergipe_utils.py         # Funções específicas do Sergipe
├── utils.py                 # Funções base (texto melhorado)
├── test_sergipe.py          # Testes das funcionalidades
├── test_menu.py             # Teste do menu PyQt
├── requirements.txt         # Dependências (incluindo PyQt5)
├── assets/
│   ├── contorno-mapa-SE.png # Contorno do mapa de Sergipe
│   ├── flag-se.jpg          # Bandeira de Sergipe (background do menu)
│   └── background*.webp     # Imagens de fundo
├── snapshots/               # Fotos de vitória salvas aqui
└── sounds/                  # Arquivos de áudio
```

---

## 🎯 **Funcionalidades Implementadas**

### ✅ **MVP Completo**
- [x] Detecção corporal em tempo real via MediaPipe
- [x] Carregamento e exibição do contorno de Sergipe
- [x] Cálculo de preenchimento por sobreposição de máscaras
- [x] Timer regressivo de 5 minutos
- [x] Barra de progresso visual
- [x] Condição de vitória (≥95% preenchimento)
- [x] Condição de derrota (tempo esgotado)
- [x] Captura automática de foto na vitória
- [x] Sistema de áudio (sons de vitória, game over, etc.)
- [x] Interface visual completa
- [x] Controles de teclado funcionais

### 🎨 **Interface Visual**
- **Tela Inicial**: Logo "VIVA SERGIPE!" com instruções
- **Durante o Jogo**:
  - Contorno do mapa sobreposto ao vídeo
  - Timer colorido (verde → amarelo → vermelho)
  - Percentual de preenchimento em tempo real
  - Barra de progresso com linha de meta (95%)
- **Vitória**: Overlay verde com "🎉 VIVA SERGIPE! 🎉"
- **Game Over**: Overlay vermelho com estatísticas finais

### 🔊 **Sistema de Áudio**
- Música de fundo contínua
- Sons de confirmação (SPACE pressionado)
- Countdown sonoro no início
- Som de vitória (100% do STRIKE A POSE)
- Som de game over
- Som de despedida (sair do jogo)

---

## 🧪 **Testes e Validação**

### **Executar Testes**
```bash
python test_sergipe.py
```

### **Testes Implementados**
1. **Carregamento do Contorno**: Verifica se o mapa de Sergipe é carregado corretamente
2. **Criação de Máscara Corporal**: Testa geração de silhueta a partir de landmarks
3. **Cálculo de Preenchimento**: Valida algoritmo de sobreposição

---

## 📸 **Capturas de Vitória**

As fotos de vitória são salvas automaticamente em `snapshots/` com o formato:
```
vitoria_sergipe_YYYYMMDD_HHMMSS_XX.X%pct.jpg
```

Exemplo: `vitoria_sergipe_20241222_143052_97.3pct.jpg`

---

## 🎮 **Dicas de Gameplay**

### **Para Maximizar o Preenchimento:**
1. **Posicionamento**: Fique a uma distância adequada da câmera
2. **Movimentos Amplos**: Use braços e pernas para cobrir mais área
3. **Estratégia**: Observe quais partes do mapa ainda precisam ser preenchidas
4. **Tempo**: Você tem 5 minutos - use-os estrategicamente!

### **Configurações Recomendadas:**
- **Iluminação**: Ambiente bem iluminado para melhor detecção
- **Fundo**: Fundo contrastante (evite roupas da mesma cor do fundo)
- **Espaço**: Área livre para movimentação ampla

---

## 🔧 **Personalização**

### **Ajustar Dificuldade**
No arquivo `sergipe_game.py`, modifique:
```python
GAME_DURATION = 300  # Tempo em segundos (300 = 5 min)
WIN_THRESHOLD = 95.0  # Percentual necessário para vencer
```

### **Trocar Contorno**
Substitua `assets/contorno-mapa-SE.png` por qualquer imagem em preto e branco:
- **Branco**: Área a ser preenchida
- **Preto**: Fundo

---

## 🏆 **Créditos**

**Baseado em**: [STRIKE A POSE!](https://github.com/alx-sch/STRIKE_A_POSE_Body_Pose_Classification_Game)
**Adaptado para**: Jogo "Viva Sergipe!" com mecânica de preenchimento corporal
**Tecnologias**: OpenCV, MediaPipe, NumPy, Pygame

---

## 🐛 **Solução de Problemas**

### **Câmera não detectada**
```bash
# Teste a câmera separadamente
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK:', cap.isOpened())"
```

### **Erro de importação**
```bash
# Reinstale as dependências
pip install --upgrade opencv-python mediapipe numpy pygame
```

### **Performance baixa**
- Feche outros aplicativos que usam a câmera
- Reduza a resolução da câmera no código (linhas 76-77 do `sergipe_game.py`)

---

🎉 **Divirta-se jogando VIVA SERGIPE!** 🎉
