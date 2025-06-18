# 🎮 VIVA SERGIPE! - Guia de Instalação

## 📋 Requisitos do Sistema

### Mínimos
- **Sistema Operacional**: Windows 10/11, Linux Ubuntu 18+, macOS 10.14+
- **Python**: 3.7 ou superior
- **RAM**: 4 GB
- **Câmera**: Webcam USB ou integrada
- **Espaço em disco**: 500 MB

### Recomendados
- **Python**: 3.8 ou superior
- **RAM**: 8 GB ou mais
- **Processador**: Intel i5 ou AMD Ryzen 5
- **Câmera**: HD (720p) ou superior

## 🚀 Instalação Rápida

### Método 1: Script Automático (Recomendado)

1. **Baixe todos os arquivos** do projeto
2. **Abra o terminal/prompt** no diretório do jogo
3. **Execute o corretor de dependências**:
   ```bash
   python fix_opencv.py
   ```
4. **Inicie o jogo**:
   ```bash
   python start_game.py
   ```
   
   **Ou no Windows, clique duas vezes em**:
   ```
   VIVA_SERGIPE.bat
   ```

### Método 2: Instalação Manual

1. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Corrija o protobuf** (se necessário):
   ```bash
   pip install protobuf==3.20.3
   ```

3. **Defina a variável de ambiente** (Windows):
   ```cmd
   set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
   ```

4. **Execute o jogo**:
   ```bash
   python sergipe_game.py
   ```

## 🔧 Solução de Problemas

### Erro: "Descriptors cannot be created directly"
**Solução**:
```bash
pip install protobuf==3.20.3
set PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
```

### Erro: "Could not open camera"
**Possíveis causas**:
- Câmera em uso por outro programa
- Drivers da câmera desatualizados
- Permissões de câmera negadas

**Soluções**:
1. Feche outros programas que usam câmera
2. Verifique permissões de câmera no sistema
3. Teste a câmera em outro aplicativo

### Erro: "OpenCV não funciona"
**Solução**:
```bash
python fix_opencv.py
```

### Erro: "ModuleNotFoundError"
**Solução**:
```bash
pip install --force-reinstall -r requirements.txt
```

## 📁 Estrutura de Arquivos

```
VIVA_SERGIPE/
├── sergipe_game.py          # Jogo principal
├── start_game.py            # Inicializador automático
├── VIVA_SERGIPE.bat         # Launcher Windows
├── fix_opencv.py            # Corretor de dependências
├── requirements.txt         # Lista de dependências
├── assets/                  # Recursos visuais
│   └── contorno-mapa-SE.png
├── sounds/                  # Arquivos de áudio
└── snapshots/              # Fotos de vitória
```

## 🎯 Como Jogar

1. **Posicione-se** em frente à câmera
2. **Pressione SPACE** para iniciar
3. **Use seu corpo** para preencher o mapa de Sergipe
4. **Meta**: Preencher ≥30% em 5 minutos

### Controles
- **SPACE**: Iniciar/Reiniciar
- **Q ou ESC**: Sair
- **R**: Reiniciar aplicação
- **F11**: Tela cheia/janela

## 🆘 Suporte

### Logs de Erro
Os logs são salvos automaticamente. Em caso de erro:
1. Verifique a saída do terminal
2. Execute `python fix_opencv.py`
3. Reinicie o computador se necessário

### Contato
- Verifique a documentação completa
- Execute os testes: `python test_sergipe.py`

## 📊 Versões Testadas

| Componente | Versão Testada | Status |
|------------|----------------|--------|
| Python     | 3.8-3.11      | ✅     |
| OpenCV     | 4.8.0.76      | ✅     |
| MediaPipe  | 0.10.5        | ✅     |
| Protobuf   | 3.20.3        | ✅     |
| PyQt5      | 5.15.11       | ✅     |

## 🔄 Atualizações

Para atualizar o jogo:
1. Baixe a nova versão
2. Execute `python fix_opencv.py`
3. Suas configurações serão preservadas

---

**🎮 Divirta-se com o VIVA SERGIPE!** 🏆
