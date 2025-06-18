# 🪟 VIVA SERGIPE! - Guia Windows 11

## 🚀 Instalação Rápida no Windows 11

### **Pré-requisitos**
- ✅ Windows 11 (qualquer versão)
- ✅ Python 3.10+ instalado
- ✅ Webcam funcionando
- ✅ Conexão com internet

---

## ⚡ Solução Express (5 minutos)

### **1. Abrir Terminal**
**Método 1 (Recomendado):**
- Pressione `Win + X`
- Clique em "Terminal do Windows"

**Método 2:**
- Pressione `Win + R`
- Digite `wt` e pressione Enter

### **2. Navegar até o projeto**
```bash
cd "C:\Users\[SeuUsuario]\Desktop\SergipeGameCompleto"
```
*Substitua `[SeuUsuario]` pelo seu nome de usuário*

### **3. Corrigir MediaPipe (ESSENCIAL)**
```bash
pip uninstall mediapipe -y
pip install mediapipe==0.10.5
```

### **4. Iniciar o jogo**
```bash
python sergipe_game.py
```

---

## 🛠️ Solução de Problemas Comuns

### **❌ "Python não é reconhecido"**
**Problema:** Terminal não encontra o Python
```bash
# Tente estas alternativas:
py sergipe_game.py
python.exe sergipe_game.py
python3 sergipe_game.py
```

### **❌ "Permissão negada"**
**Problema:** Windows bloqueia a execução
**Solução:**
1. Feche o terminal atual
2. Clique direito no "Terminal do Windows"
3. Selecione "Executar como administrador"
4. Execute os comandos novamente

### **❌ Windows Defender alerta**
**Problema:** "Aplicativo não reconhecido"
**Solução:**
1. Clique em "Mais informações"
2. Clique em "Executar mesmo assim"
3. **É seguro** - Python não é assinado digitalmente

### **❌ "ModuleNotFoundError"**
**Problema:** Dependências faltando
```bash
# Instale todas as dependências:
pip install -r requirements.txt
```

---

## 🎮 Verificação Completa

### **Teste todas as dependências:**
```bash
python -c "import mediapipe as mp; print('✅ MediaPipe:', mp.__version__)"
python -c "import cv2; print('✅ OpenCV:', cv2.__version__)"
python -c "import PyQt5; print('✅ PyQt5: OK')"
python -c "import pygame; print('✅ Pygame: OK')"
python -c "import numpy; print('✅ NumPy: OK')"
```

**Resultado esperado:**
```
✅ MediaPipe: 0.10.5
✅ OpenCV: 4.x.x
✅ PyQt5: OK
✅ Pygame: OK
✅ NumPy: OK
```

---

## 🎯 Como Jogar

### **Inicialização:**
1. Execute: `python sergipe_game.py`
2. Aguarde o menu PyQt5 aparecer (~10-15 segundos)
3. Clique em "🎮 JOGAR"
4. O jogo OpenCV abre em tela cheia

### **Objetivo:**
- Use seu corpo para preencher o contorno verde do mapa de Sergipe
- Meta: 30% de preenchimento em 5 minutos
- Seja criativo com poses!

### **Controles:**
- **Q ou ESC**: Sair do jogo
- **F11**: Alternar tela cheia
- **Mouse**: Navegar no menu

---

## 🔧 Otimizações Windows 11

### **Para melhor performance:**
```bash
# Atualize o pip
python -m pip install --upgrade pip

# Atualize ferramentas
python -m pip install --upgrade setuptools wheel

# Limpe cache (opcional)
pip cache purge
```

### **Configurações recomendadas:**
- **Modo de energia**: Alto desempenho
- **Windows Defender**: Adicionar exceção para a pasta do projeto
- **Webcam**: Permitir acesso para aplicativos desktop

---

## 📱 Atalhos Úteis Windows 11

### **Terminal:**
- `Win + X` → Terminal
- `Ctrl + Shift + T` → Nova aba
- `Ctrl + Shift + W` → Fechar aba

### **Navegação:**
- `cd ..` → Voltar pasta
- `dir` → Listar arquivos
- `cls` → Limpar tela

### **Python:**
- `python --version` → Ver versão
- `pip list` → Ver pacotes instalados
- `pip show mediapipe` → Detalhes do MediaPipe

---

## 🆘 Suporte Emergencial

### **Se nada funcionar:**

#### **Opção 1: Reset completo**
```bash
pip uninstall mediapipe opencv-python PyQt5 pygame numpy -y
pip install mediapipe==0.10.5 opencv-python PyQt5 pygame numpy
```

#### **Opção 2: Ambiente virtual**
```bash
python -m venv viva_sergipe
viva_sergipe\Scripts\activate
pip install -r requirements.txt
pip uninstall mediapipe -y
pip install mediapipe==0.10.5
python sergipe_game.py
```

#### **Opção 3: Usar Python Launcher**
```bash
py -3.10 sergipe_game.py
```

---

## ✅ Checklist Final

Antes de jogar, verifique:

- [ ] Windows 11 atualizado
- [ ] Python 3.10+ instalado
- [ ] Terminal funcionando
- [ ] MediaPipe 0.10.5 instalado
- [ ] Webcam conectada e funcionando
- [ ] Pasta do projeto acessível
- [ ] Permissões adequadas

**Se todos os itens estão ✅, execute:**
```bash
python sergipe_game.py
```

---

## 🎉 Sucesso!

Se você chegou até aqui e o jogo está funcionando:

🎮 **PARABÉNS!** Você está pronto para jogar VIVA SERGIPE!

🇧🇷 **Divirta-se** explorando o mapa de Sergipe com seu corpo!

📸 **Suas vitórias** serão salvas automaticamente em `snapshots/`

---

*Guia específico para Windows 11 - Versão 1.0*  
*Criado em: 30/05/2025*  
*Testado em: Windows 11 Pro/Home*



___________________________________________________

pip uninstall mediapipe -y
pip uninstall protobuf -y
pip install protobuf==3.20.3
pip install mediapipe==0.10.5
python sergipe_game.py