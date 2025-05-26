# 🎛️ DEMONSTRAÇÃO - SISTEMA DE CONFIGURAÇÕES

## 🆕 **NOVIDADES DA VERSÃO 1.1**

O **VIVA SERGIPE!** agora possui um sistema completo de configurações persistentes! 

### ✨ **Principais Melhorias:**

1. **🎮 Configurações de Jogo Personalizáveis**
   - Duração do jogo (1-10 minutos)
   - Meta de preenchimento (10-100%)
   - Sensibilidade corporal (500-5000 pixels)
   - Modo tela cheia automático
   - Salvamento automático de fotos

2. **🔊 Controles de Áudio Avançados**
   - Volume geral (0-100%)
   - Volume da música de fundo
   - Volume dos efeitos sonoros
   - Volume dos comandos de voz
   - Opção "Silenciar Tudo"

3. **🎨 Configurações Visuais**
   - Mostrar/ocultar percentual
   - Mostrar/ocultar timer
   - Mostrar/ocultar barra de progresso
   - Espelhar câmera
   - Espessura do contorno (1-10 pixels)

4. **📊 Estatísticas do Jogador**
   - Jogos jogados e vencidos
   - Melhor percentual alcançado
   - Melhor tempo para alcançar meta
   - Tempo total jogado
   - Número de fotos salvas

---

## 🚀 **COMO USAR**

### **1. Acessar Configurações**
```bash
# Execute o jogo
python sergipe_game.py

# No menu principal, clique em:
⚙️ CONFIGURAÇÕES
```

### **2. Navegar pelas Abas**
- **🎮 Jogo**: Configurações principais do gameplay
- **🔊 Áudio**: Controles de volume e som
- **🎨 Visual**: Aparência e interface
- **📊 Stats**: Suas estatísticas pessoais

### **3. Ajustar Configurações**
- Use os **controles deslizantes** para volumes
- Use os **campos numéricos** para valores específicos
- Use as **caixas de seleção** para ativar/desativar recursos

### **4. Salvar Alterações**
- Clique em **💾 Salvar** para aplicar as mudanças
- As configurações são salvas automaticamente em `config.json`
- Clique em **🔄 Restaurar Padrões** se necessário

---

## 📁 **ARQUIVOS CRIADOS**

### **config.json** (Criado automaticamente)
```json
{
    "game": {
        "duration": 300,
        "win_threshold": 30.0,
        "min_body_pixels": 1000,
        "fullscreen": true,
        "auto_save_photos": true
    },
    "audio": {
        "master_volume": 0.7,
        "music_volume": 0.5,
        "effects_volume": 0.8,
        "voice_volume": 0.9,
        "mute_all": false
    },
    "visual": {
        "show_percentage": true,
        "show_timer": true,
        "show_progress_bar": true,
        "camera_mirror": true,
        "contour_thickness": 3
    },
    "stats": {
        "games_played": 0,
        "games_won": 0,
        "best_percentage": 0.0,
        "best_time": 0.0,
        "total_playtime": 0.0,
        "photos_saved": 0
    }
}
```

---

## 🧪 **TESTAR O SISTEMA**

### **Teste Automático**
```bash
# Execute o teste completo
python test_config.py

# Resultado esperado:
# 🎉 TODOS OS TESTES PASSARAM!
```

### **Teste Manual**
1. **Execute o jogo**: `python sergipe_game.py`
2. **Acesse configurações**: Clique em "⚙️ CONFIGURAÇÕES"
3. **Altere algumas configurações**:
   - Mude a duração para 4 minutos
   - Ajuste a meta para 25%
   - Diminua o volume da música
4. **Salve as configurações**: Clique em "💾 Salvar"
5. **Feche e reabra o jogo**
6. **Verifique se as configurações persistiram**

---

## 🎯 **EXEMPLOS DE USO**

### **Configuração Fácil**
```
Duração: 6 minutos
Meta: 25%
Sensibilidade: 750 pixels
```

### **Configuração Normal (Padrão)**
```
Duração: 5 minutos
Meta: 30%
Sensibilidade: 1000 pixels
```

### **Configuração Difícil**
```
Duração: 3 minutos
Meta: 40%
Sensibilidade: 1500 pixels
```

### **Configuração Expert**
```
Duração: 2 minutos
Meta: 50%
Sensibilidade: 2000 pixels
```

---

## 🔧 **SOLUÇÃO DE PROBLEMAS**

### **Configurações não salvam**
```bash
# Verifique permissões de escrita
ls -la config.json

# Execute como administrador se necessário
sudo python sergipe_game.py
```

### **Arquivo config.json corrompido**
```bash
# Remova o arquivo para recriar com padrões
rm config.json

# Execute o jogo novamente
python sergipe_game.py
```

### **Interface de configurações não abre**
```bash
# Verifique se PyQt5 está instalado
pip install PyQt5

# Teste a interface isoladamente
python config_window.py
```

---

## 📈 **ESTATÍSTICAS AUTOMÁTICAS**

O sistema agora rastreia automaticamente:

- **Jogos Jogados**: Incrementado a cada partida
- **Jogos Vencidos**: Incrementado quando você alcança a meta
- **Melhor Percentual**: Atualizado quando você supera seu recorde
- **Melhor Tempo**: Menor tempo para alcançar a meta
- **Tempo Total**: Soma de todas as sessões de jogo
- **Fotos Salvas**: Número de vitórias registradas

### **Resetar Estatísticas**
1. Acesse **📊 Stats** nas configurações
2. Clique em **🗑️ Resetar Estatísticas**
3. Confirme a ação (irreversível)

---

## 🎉 **BENEFÍCIOS**

### **Para o Jogador**
- ✅ **Personalização completa** da experiência
- ✅ **Configurações salvas** entre sessões
- ✅ **Acompanhamento do progresso** com estatísticas
- ✅ **Interface intuitiva** e fácil de usar

### **Para o Desenvolvedor**
- ✅ **Código modular** e bem organizado
- ✅ **Sistema extensível** para novas configurações
- ✅ **Testes automatizados** garantem qualidade
- ✅ **Documentação completa** facilita manutenção

---

## 🚀 **PRÓXIMOS PASSOS**

Com o sistema de configurações implementado, as próximas melhorias incluem:

1. **🎮 Modos de Jogo Adicionais**
   - Modo Relaxado (sem timer)
   - Modo Speedrun (tempo limitado)
   - Modo Precisão (meta alta)

2. **🏆 Sistema de Conquistas**
   - Badges por marcos alcançados
   - Desafios especiais
   - Recompensas por consistência

3. **📊 Analytics Avançados**
   - Gráficos de progresso
   - Análise de performance
   - Relatórios detalhados

---

**🎮 Divirta-se explorando as novas configurações do VIVA SERGIPE! 🎮**
