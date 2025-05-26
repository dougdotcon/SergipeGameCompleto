# 🎮 VIVA SERGIPE! - Como Jogar

## 🚀 **Execução Rápida**
```bash
python sergipe_game.py
```

## 🎯 **Objetivo**
- Use seu corpo para **preencher a meta configurada** do contorno do mapa de Sergipe
- O tempo e meta podem ser ajustados nas **CONFIGURAÇÕES**
- Quando conseguir, uma foto será salva automaticamente!

## 🎮 **Controles**

### **Menu Principal**
- **↑↓** ou **W/S**: Navegar entre opções
- **ENTER** ou **SPACE**: Selecionar opção
- **Q** ou **ESC**: Sair do jogo
- **F11**: Alternar tela cheia/janela

### **Menu de Configurações**
- **↑↓** ou **W/S**: Navegar entre configurações
- **←→** ou **A/D**: Ajustar valores
- **ENTER**: Confirmar/Voltar
- **ESC**: Voltar ao menu principal

### **Durante o Jogo**
- **SPACE**: Iniciar/Reiniciar jogo
- **Q** ou **ESC**: Voltar ao menu principal
- **R**: Reiniciar aplicação
- **F11**: Alternar tela cheia/janela

## 📋 **Interface do Jogo**

### **Menu Principal**
- **1. JOGAR**: Inicia o jogo
- **2. CONFIGURAÇÕES**: Abre menu de configurações
- **3. SAIR**: Fecha o aplicativo
- Navegação com setas ou WASD
- Seleção com ENTER ou SPACE

### **Menu de Configurações**
- **Duração do Jogo**: 1:00 a 10:00 minutos (ajuste de 30s)
- **Meta de Preenchimento**: 10% a 100% (ajuste de 5%)
- **Sensibilidade Corporal**: 500 a 5000 pixels (ajuste de 250)
- **VOLTAR**: Retorna ao menu principal
- Ajuste com setas esquerda/direita ou A/D

### **Tela de Jogo**
- Contorno do mapa de Sergipe sobreposto na câmera
- Timer com contagem regressiva
- Percentual de preenchimento em tempo real
- Barra de progresso visual

### **Durante o Jogo**
- **Timer**: Conta regressiva de 5:00 minutos
  - Verde: >1 minuto restante
  - Amarelo: 30s-1min restante
  - Vermelho: <30s restantes
- **Percentual**: Mostra preenchimento atual em tempo real
- **Barra de Progresso**: Visual do progresso com linha de meta em 95%
- **Contorno Verde**: Área do mapa de Sergipe a ser preenchida

### **Vitória (≥95%)**
- Tela verde com "🎉 VIVA SERGIPE! 🎉"
- Percentual final alcançado
- Confirmação de foto salva
- Som de vitória

### **Game Over (Tempo esgotado)**
- Tela vermelha com "GAME OVER"
- Percentual final alcançado
- Mensagem de encorajamento
- Som de game over

## 📸 **Fotos de Vitória**
- Salvas automaticamente em `snapshots/`
- Formato: `vitoria_sergipe_YYYYMMDD_HHMMSS_XX.X%pct.jpg`
- Incluem overlay com texto de vitória e percentual

## 💡 **Dicas para Jogar**

### **Posicionamento**
- Fique a 1-2 metros da câmera
- Certifique-se de que todo seu corpo está visível
- Use boa iluminação (evite contraluz)

### **Estratégia**
- **Movimentos amplos**: Abra braços e pernas para cobrir mais área
- **Observe o mapa**: Veja quais partes ainda precisam ser preenchidas
- **Use o tempo**: 5 minutos é bastante tempo - seja estratégico
- **Mude de posição**: Mova-se pela tela para preencher diferentes áreas

### **Roupas Recomendadas**
- Evite roupas da mesma cor do fundo
- Cores contrastantes ajudam na detecção
- Roupas justas facilitam a detecção da silhueta

## 🔧 **Solução de Problemas**

### **Jogo não abre em tela cheia**
- Pressione **F11** para alternar
- Ou feche e abra novamente

### **Câmera não detectada**
```bash
# Teste a câmera
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK:', cap.isOpened())"
```

### **Performance baixa**
- Feche outros programas que usam a câmera
- Reduza a resolução no código se necessário

### **Detecção corporal ruim**
- Melhore a iluminação
- Use fundo contrastante
- Certifique-se de estar totalmente visível

## 📊 **Sistema de Pontuação**
- **0-49%**: "Continue tentando!"
- **50-94%**: "Bom trabalho! Tente novamente!"
- **95-100%**: "🎉 VIVA SERGIPE! 🎉" + Foto salva

## 🎵 **Áudio**
- **Música de fundo**: Toca continuamente
- **Sons de confirmação**: Ao pressionar SPACE
- **Countdown**: No início do jogo
- **Vitória**: Som especial de 100%
- **Game Over**: Som de encorajamento
- **Despedida**: Ao sair do jogo

---

## 🏆 **Desafios Extras**

### **Fácil**
- Meta: 85% em 5 minutos

### **Normal**
- Meta: 95% em 5 minutos (padrão)

### **Difícil**
- Meta: 98% em 3 minutos

### **Expert**
- Meta: 99% em 2 minutos

*Para alterar a dificuldade, edite `GAME_DURATION` e `WIN_THRESHOLD` no arquivo `sergipe_game.py`*

---

🎉 **Divirta-se representando Sergipe com seu corpo!** 🎉
