# TODO - BrJoy Web Optimizer V1

## ✅ Concluído
- [x] RF01 - Scan recursivo de pastas
- [x] RF03 - Presets web (6 presets)
- [x] RF04 - Slider de qualidade (60-100%)
- [x] Estrutura de dados (arquivos como dicts)
- [x] Coluna tamanho na lista
- [x] Botão "Escanear Pasta"
- [x] Filtro de diretórios ignorados

## 🔄 Em Progresso
- [ ] RF02 - Manter estrutura de diretórios
  - Lógica implementada em `_converter_thread`
  - Precisa testar com pasta real
  - Adicionar checkbox "Manter estrutura" na UI

- [ ] RF05 - Relatório HTML
  - Template HTML criado
  - Precisa integrar com `_gerar_relatorio()`
  - Adicionar botão "Abrir Relatório"

- [ ] RF07 - Cálculo de economia
  - Parcialmente implementado
  - Falta exibir economia por arquivo na lista
  - Falta totalizador no rodapé

## ⏳ Pendente (P0 - Crítico)
- [ ] RF06 - Modo não-destrutivo
  - Adicionar checkbox "Manter originais" (sempre marcado)
  - Validar que nunca sobrescreve originais
  - Adicionar opção "Timestamp na pasta"

- [ ] RF08 - Filtros e exclusões
  - Checkbox "Ignorar <50KB"
  - Checkbox "Ignorar >10MB"
  - Campo "Excluir pastas"

- [ ] Corrigir bugs conhecidos:
  - `_add_files()` precisa validar extensões
  - `selecionar_arquivos()` ainda usa lógica antiga
  - `limpar_arquivos()` precisa limpar `pasta_origem`

## ⏳ Pendente (P1 - Alta)
- [ ] Melhorar UX:
  - Loading spinner durante scan
  - Tooltip explicando cada preset
  - Atalho Ctrl+S para escanear
  - Drag & Drop de pastas

- [ ] Performance:
  - Processamento paralelo (threads)
  - Cancelar conversão (botão Stop)

## ⏳ Pendente (P2 - Média)
- [ ] Testes:
  - Testar com 1000+ imagens
  - Testar estrutura de 10 níveis
  - Testar com imagens corrompidas

- [ ] Documentação:
  - Atualizar README com screenshots
  - Criar CHANGELOG.md
  - Vídeo demo 2min

## 🚀 Próximos Passos (Ordem)
1. Completar RF02 (manter estrutura) - 30min
2. Completar RF05 (relatório) - 20min
3. Completar RF06 (não-destrutivo) - 15min
4. Completar RF07 (economia) - 20min
5. Testar com pasta real - 30min
6. Corrigir bugs - 1h
7. Polish UI - 30min
8. **LANÇAR BETA** 🎉

## Estimativa Total
- Tempo restante: ~4h
- Data alvo: 03/03/2026 (hoje!)
