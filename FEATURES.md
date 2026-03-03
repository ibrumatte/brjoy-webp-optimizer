# BrJoy Image Converter - Novas Features

## Implementações

### 1. Atalhos de Teclado
- **Ctrl+O**: Adicionar arquivos
- **Delete**: Remover itens selecionados da lista
- **Ctrl+Enter**: Converter (só funciona se houver arquivos e não estiver convertendo)

### 2. Presets Rápidos
Dropdown de presets na seção Configurações:
- **Instagram 4:5**: 1080x1350px com crop 4:5
- **Quadrado 1:1**: 1080x1080px com crop 1:1
- **Story 9:16**: 1080x1920px com crop 9:16
- **Thumb 1280px**: 1280px no lado maior, sem crop

### 3. Drag & Drop
- Arraste arquivos ou pastas diretamente para a lista
- Filtra automaticamente extensões suportadas
- Ignora duplicados
- Visual de hover ao arrastar
- Limite de 100 arquivos por pasta

## Instalação da Dependência (Drag & Drop)

### Linux (Debian/Ubuntu)
```bash
pip3 install tkinterdnd2
```

### Alternativa (se pip3 não funcionar)
```bash
sudo apt install python3-pip
pip3 install --user tkinterdnd2
```

### Verificar instalação
```bash
python3 -c "import tkinterdnd2; print('OK')"
```

**Nota**: O app funciona sem tkinterdnd2, mas o drag & drop não estará disponível.

## Checklist de Testes

### Drag & Drop
- [ ] Arrastar 1 arquivo → deve adicionar
- [ ] Arrastar vários arquivos → deve adicionar todos
- [ ] Arrastar arquivo duplicado → deve ignorar
- [ ] Arrastar arquivo inválido (.txt) → deve ignorar
- [ ] Arrastar pasta com imagens → deve adicionar imagens (max 100)
- [ ] Visual de hover ao arrastar → fundo azul claro

### Atalhos de Teclado
- [ ] Ctrl+O sem arquivos → abre diálogo
- [ ] Ctrl+O com arquivos → adiciona mais
- [ ] Delete sem seleção → não faz nada
- [ ] Delete com 1 item selecionado → remove
- [ ] Delete com múltiplos selecionados → remove todos
- [ ] Ctrl+Enter sem arquivos → não faz nada
- [ ] Ctrl+Enter com arquivos → inicia conversão
- [ ] Atalhos durante conversão → ignorados

### Presets
- [ ] Selecionar "Instagram 4:5" → marca resize, seta 1080x1350, marca crop
- [ ] Selecionar "Quadrado 1:1" → marca resize, seta 1080x1080, marca crop 1:1
- [ ] Selecionar "Story 9:16" → marca resize, seta 1080x1920, marca crop
- [ ] Selecionar "Thumb 1280px" → marca resize, seta 1280, desmarca crop
- [ ] Aplicar preset e ajustar manualmente → deve funcionar normalmente
- [ ] Formato (WebP/PNG) não muda ao aplicar preset

### Estados
- [ ] Vazio: botão converter desabilitado, status "Ctrl+O para adicionar"
- [ ] Com arquivos: botão converter habilitado, status "Ctrl+Enter para converter"
- [ ] Convertendo: inputs bloqueados, atalhos ignorados, progresso atualiza
- [ ] Concluído: inputs liberados, status mostra resultado

## Compatibilidade

- **Linux**: Totalmente funcional
- **Windows**: Funcional (tkinterdnd2 disponível via pip)
- **macOS**: Funcional (tkinterdnd2 disponível via pip)

## Troubleshooting

### Drag & Drop não funciona
```bash
# Reinstalar tkinterdnd2
pip3 uninstall tkinterdnd2
pip3 install tkinterdnd2
```

### Atalhos não funcionam
- Verifique se a janela está em foco
- No Linux, alguns gerenciadores de janela podem capturar Ctrl+O globalmente

### Presets não aplicam corretamente
- Verifique se ImageMagick está instalado: `convert -version`
- Aspect ratios customizados (4:5, 9:16) usam `-extent` do ImageMagick
