# PRD - BrJoy Web Optimizer V1

**Versão:** 1.0  
**Data:** 03/03/2026  
**Autor:** BrJoy Team  
**Status:** Em Desenvolvimento

---

## 1. Visão do Produto

### 1.1 Problema
Sites e aplicações web sofrem com imagens pesadas (JPG/PNG) que impactam negativamente:
- Core Web Vitals (LCP, CLS)
- Tempo de carregamento
- Custos de banda/CDN
- Experiência mobile

Times de desenvolvimento precisam migrar milhares de imagens para WebP mas enfrentam:
- Falta de ferramentas que preservem estrutura de diretórios
- Ausência de relatórios de impacto
- Medo de quebrar URLs e SEO
- Processo manual e demorado

### 1.2 Solução
Pipeline desktop de otimização de imagens que:
- Converte JPG/PNG → WebP em lote
- Mantém estrutura de diretórios intacta
- Gera relatórios de economia de espaço
- Oferece presets específicos para web
- Modo não-destrutivo (preserva originais)

### 1.3 Público-Alvo (V1)
- **Primário:** Desenvolvedores frontend (Next.js, Astro, Hugo, Vite)
- **Secundário:** Agências web e freelancers
- **Terciário:** Times de marketing com sites estáticos

### 1.4 Proposta de Valor
"Converta milhares de imagens para WebP em minutos, preserve sua estrutura de pastas e veja quanto espaço economizou. Sem quebrar URLs, sem complicação."

---

## 2. Objetivos e Métricas

### 2.1 Objetivos de Negócio
- Validar demanda por ferramenta de otimização web
- Estabelecer base de usuários (100 downloads em 30 dias)
- Coletar feedback para V2 (CLI)

### 2.2 Objetivos de Produto
- Reduzir tempo de conversão em lote de horas para minutos
- Garantir 0% de perda de arquivos (modo não-destrutivo)
- Economia média de 60-80% no tamanho dos arquivos

### 2.3 Métricas de Sucesso
- **Adoção:** 100+ downloads/mês
- **Engajamento:** 70%+ dos usuários convertem >50 imagens
- **Satisfação:** NPS >40
- **Performance:** Conversão de 1000 imagens em <5min

---

## 3. Requisitos Funcionais

### 3.1 RF01 - Scan Recursivo de Pastas
**Prioridade:** P0 (Crítico)

**Descrição:**  
Usuário seleciona pasta raiz e o sistema escaneia recursivamente todos os subdiretórios.

**Critérios de Aceite:**
- [ ] Botão "Escanear Pasta" abre seletor de diretórios
- [ ] Escaneia até 10 níveis de profundidade
- [ ] Filtra apenas extensões suportadas (.jpg, .jpeg, .png, .bmp, .tiff, .gif)
- [ ] Ignora pastas: `node_modules`, `.git`, `dist`, `build`, `.cache`, `__pycache__`
- [ ] Exibe contador em tempo real: "Encontradas: 247 imagens"
- [ ] Limite de 10.000 arquivos por scan (com aviso se exceder)

**Fluxo:**
1. Usuário clica "Escanear Pasta"
2. Seleciona diretório raiz (ex: `/projeto/public`)
3. Sistema escaneia e popula lista com paths relativos
4. Exibe total encontrado e tamanho total em MB

---

### 3.2 RF02 - Manter Estrutura de Diretórios
**Prioridade:** P0 (Crítico)

**Descrição:**  
Ao converter, replicar estrutura de pastas da origem no destino.

**Critérios de Aceite:**
- [ ] Se origem: `/public/images/blog/post1.jpg`
- [ ] Destino: `/output/images/blog/post1.webp`
- [ ] Cria subpastas automaticamente se não existirem
- [ ] Preserva nomes de arquivos (apenas muda extensão)
- [ ] Opção "Flatten" (opcional): salvar tudo em pasta única

**Exemplo:**
```
Origem:
/projeto/public/
  ├── hero.jpg
  └── blog/
      ├── post1.png
      └── thumbs/
          └── thumb1.jpg

Destino:
/output/
  ├── hero.webp
  └── blog/
      ├── post1.webp
      └── thumbs/
          └── thumb1.webp
```

---

### 3.3 RF03 - Presets Web
**Prioridade:** P0 (Crítico)

**Descrição:**  
Presets otimizados para casos de uso web comuns.

**Presets:**

| Nome | Dimensões | Formato | Qualidade | Uso |
|------|-----------|---------|-----------|-----|
| **Hero Image** | 1920x1080 | WebP | 85% | Banners, headers |
| **Blog Post** | 1200x630 | WebP | 85% | Open Graph, artigos |
| **Thumbnail** | 400x300 | WebP | 80% | Listagens, grids |
| **Mobile Optimized** | 800px (largura) | WebP | 80% | Mobile-first |
| **Avatar/Icon** | 256x256 | WebP/PNG | 90% | Perfis, ícones |
| **Original Quality** | Mantém | WebP | 95% | Conversão sem perda visual |

**Critérios de Aceite:**
- [ ] Dropdown "Presets Web" na UI
- [ ] Ao selecionar preset, preenche automaticamente: formato, dimensões, qualidade
- [ ] Usuário pode ajustar manualmente após aplicar preset
- [ ] Preset "Custom" permite configuração livre

---

### 3.4 RF04 - Slider de Qualidade
**Prioridade:** P1 (Alta)

**Descrição:**  
Controle fino de qualidade de compressão WebP.

**Critérios de Aceite:**
- [ ] Slider horizontal: 60% a 100%
- [ ] Valor padrão: 85%
- [ ] Label mostra valor atual: "Qualidade: 85%"
- [ ] Tooltip explica: "60-70%: Agressivo | 80-90%: Balanceado | 95-100%: Alta fidelidade"
- [ ] Aplica a todas as imagens do lote

**Referência:**
- 60-70%: Economia máxima, perda visual perceptível
- 80-85%: Sweet spot (economia + qualidade)
- 90-95%: Quase sem perda visual
- 100%: Lossless (apenas para PNG com transparência)

---

### 3.5 RF05 - Relatório de Economia
**Prioridade:** P0 (Crítico)

**Descrição:**  
Após conversão, gerar relatório HTML/CSV com estatísticas.

**Critérios de Aceite:**
- [ ] Abre automaticamente após conversão
- [ ] Exibe:
  - Total de arquivos processados
  - Tamanho original total (MB)
  - Tamanho final total (MB)
  - Economia absoluta (MB) e percentual (%)
  - Tempo total de processão
  - Top 10 imagens que mais economizaram
- [ ] Botão "Exportar CSV" para análise
- [ ] Botão "Salvar HTML" para compartilhar

**Exemplo de Relatório:**
```
═══════════════════════════════════════
  BrJoy Web Optimizer - Relatório
═══════════════════════════════════════

📊 Resumo
─────────────────────────────────────
✓ Arquivos processados: 247
✓ Tamanho original: 156.8 MB
✓ Tamanho final: 42.3 MB
✓ Economia: 114.5 MB (73%)
⏱ Tempo: 2min 34s

🏆 Top 10 Maiores Economias
─────────────────────────────────────
1. hero-banner.jpg → 8.2 MB → 1.9 MB (77%)
2. product-photo.png → 6.5 MB → 1.2 MB (82%)
...

💡 Recomendações
─────────────────────────────────────
• 12 imagens ainda >1MB (considere redimensionar)
• 5 imagens falharam (verifique logs)
```

---

### 3.6 RF06 - Modo Não-Destrutivo
**Prioridade:** P0 (Crítico)

**Descrição:**  
Nunca sobrescrever arquivos originais.

**Critérios de Aceite:**
- [ ] Sempre salva em pasta separada (padrão: `./brjoy-output/`)
- [ ] Checkbox "Manter originais" (sempre marcado, não pode desmarcar)
- [ ] Aviso se pasta de saída já existe: "Sobrescrever arquivos existentes?"
- [ ] Opção "Adicionar timestamp" ao nome da pasta: `brjoy-output-2026-03-03_00-20/`

---

### 3.7 RF07 - Cálculo de Tamanho Antes/Depois
**Prioridade:** P0 (Crítico)

**Descrição:**  
Exibir tamanho de cada arquivo antes e depois da conversão.

**Critérios de Aceite:**
- [ ] Coluna "Tamanho Original" na lista
- [ ] Coluna "Tamanho Final" (atualiza após conversão)
- [ ] Coluna "Economia" (% e MB)
- [ ] Rodapé com totais: "Total: 156.8 MB → 42.3 MB (73%)"
- [ ] Cores: verde se economia >50%, amarelo 30-50%, vermelho <30%

---

### 3.8 RF08 - Filtros e Exclusões
**Prioridade:** P2 (Média)

**Descrição:**  
Permitir filtrar/excluir arquivos antes de converter.

**Critérios de Aceite:**
- [ ] Checkbox "Ignorar imagens <50KB" (já otimizadas)
- [ ] Checkbox "Ignorar imagens >10MB" (muito grandes, travam)
- [ ] Campo "Excluir pastas" (ex: `thumbs, cache, temp`)
- [ ] Botão "Remover selecionados" (Delete key)

---

## 4. Requisitos Não-Funcionais

### 4.1 Performance
- Conversão de 1000 imagens (100MB total) em <5min
- UI responsiva durante conversão (não travar)
- Uso de threads para processamento paralelo

### 4.2 Usabilidade
- Onboarding: tooltip no primeiro uso explicando fluxo
- Atalhos de teclado mantidos (Ctrl+O, Delete, Ctrl+Enter)
- Drag & Drop funcional para pastas inteiras

### 4.3 Compatibilidade
- Linux (Ubuntu 20.04+)
- Windows 10/11 (futuro)
- macOS 11+ (futuro)
- Requer: Python 3.8+, ImageMagick 7+

### 4.4 Confiabilidade
- 0% de perda de dados (modo não-destrutivo)
- Logs de erro detalhados
- Rollback automático se conversão falhar >50%

### 4.5 Segurança
- Não enviar dados para servidores externos
- Strip EXIF por padrão (privacidade)
- Opção "Manter metadados" para fotógrafos

---

## 5. Escopo V1 (MVP)

### ✅ In Scope
- Scan recursivo de pastas
- Manter estrutura de diretórios
- Presets web (6 presets)
- Slider de qualidade
- Relatório HTML/CSV
- Modo não-destrutivo
- Cálculo de economia

### ❌ Out of Scope (V2+)
- CLI (`brjoy-img optimize`)
- Gerador de snippets `<picture>`
- Responsive variants (srcset)
- Deduplicação por hash
- Integração CDN
- Preview antes/depois visual
- Batch processing com múltiplos tamanhos

---

## 6. User Stories

### US01 - Desenvolvedor Frontend
**Como** desenvolvedor frontend  
**Quero** converter todas as imagens do meu projeto Next.js para WebP  
**Para** melhorar o Lighthouse score e reduzir tempo de carregamento

**Cenário:**
1. Abro BrJoy Web Optimizer
2. Clico "Escanear Pasta" e seleciono `/meu-projeto/public`
3. Sistema encontra 347 imagens
4. Seleciono preset "Mobile Optimized"
5. Clico "Converter"
6. Aguardo 3min
7. Vejo relatório: economizei 89MB (71%)
8. Copio pasta `brjoy-output/` para `/public/`

---

### US02 - Agência Web
**Como** agência web  
**Quero** otimizar imagens de 10 sites de clientes  
**Para** entregar projetos com melhor performance

**Cenário:**
1. Para cada cliente, escaneia pasta `/uploads`
2. Aplica preset "Blog Post" (1200x630, 85%)
3. Gera relatório CSV para cada cliente
4. Envia relatório mostrando economia de banda/CDN

---

### US03 - Freelancer
**Como** freelancer  
**Quero** converter imagens de um e-commerce  
**Para** reduzir custos de hospedagem do cliente

**Cenário:**
1. Cliente tem 2.000 fotos de produtos (500MB)
2. Escaneia pasta `/produtos`
3. Aplica preset "Thumbnail" para listagens
4. Converte e economiza 380MB (76%)
5. Mostra relatório ao cliente justificando upgrade de plano

---

## 7. Fluxo de Usuário (Happy Path)

```
┌─────────────────┐
│  Abrir App      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Escanear Pasta  │ ← Seleciona diretório raiz
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Lista Populada  │ ← Mostra 247 imagens encontradas
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Aplicar Preset  │ ← Seleciona "Mobile Optimized"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Ajustar Config  │ ← (Opcional) Ajusta qualidade para 80%
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Converter       │ ← Clica "Converter (247)"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Progresso       │ ← Barra: "Convertendo 123/247..."
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Relatório       │ ← Abre HTML: "Economizou 114MB (73%)"
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Abrir Pasta     │ ← Botão "Abrir pasta de saída"
└─────────────────┘
```

---

## 8. Wireframes (Texto)

### Tela Principal - Após Scan
```
┌─────────────────────────────────────────────────────────────┐
│ 🖼️ BrJoy Web Optimizer                                      │
│ Pipeline de otimização de imagens para web                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌─────────────────────────────┐  ┌────────────────────────┐│
│ │ 📁 Arquivos (247)           │  │ ⚙️ Configurações       ││
│ │                             │  │                        ││
│ │ [Escanear Pasta] [Limpar]  │  │ Presets Web:           ││
│ │                             │  │ [Mobile Optimized ▼]   ││
│ │ ┌─────────────────────────┐ │  │                        ││
│ │ │ Nome          | Tamanho │ │  │ Formato:               ││
│ │ ├─────────────────────────┤ │  │ ○ WebP  ○ PNG          ││
│ │ │ hero.jpg      | 2.3 MB  │ │  │                        ││
│ │ │ blog/post1.png| 1.8 MB  │ │  │ Qualidade: [====] 85%  ││
│ │ │ ...           | ...     │ │  │                        ││
│ │ └─────────────────────────┘ │  │ ☑ Strip EXIF           ││
│ │                             │  │ ☑ Manter estrutura     ││
│ │ Total: 156.8 MB             │  │                        ││
│ └─────────────────────────────┘  └────────────────────────┘│
│                                                              │
│ ┌────────────────────────────────────────────────────────┐  │
│ │ Pasta de saída: /home/user/brjoy-output [Escolher]    │  │
│ │ [████████████████░░░░░░░░░░] 65%                       │  │
│ │ Status: Convertendo 160/247... • Ctrl+Enter converter │  │
│ │                                    [✨ Converter (247)]│  │
│ └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 9. Critérios de Lançamento

### Pré-Lançamento
- [ ] Todos os RF P0 implementados e testados
- [ ] Teste com 1.000+ imagens sem crash
- [ ] Relatório HTML funcional
- [ ] README.md atualizado com instruções
- [ ] Vídeo demo de 2min no YouTube

### Lançamento Soft (Beta)
- [ ] Compartilhar em comunidades: r/webdev, r/nextjs, Dev.to
- [ ] Coletar feedback de 10 usuários beta
- [ ] Corrigir bugs críticos

### Lançamento Público
- [ ] Landing page simples (GitHub Pages)
- [ ] Post no Product Hunt
- [ ] Tweet thread explicando problema/solução

---

## 10. Riscos e Mitigações

| Risco | Impacto | Probabilidade | Mitigação |
|-------|---------|---------------|-----------|
| ImageMagick não instalado | Alto | Média | Detectar e mostrar instruções de instalação |
| Conversão muito lenta (>10min) | Alto | Baixa | Implementar processamento paralelo (threads) |
| Usuário perde arquivos originais | Crítico | Baixa | Modo não-destrutivo obrigatório |
| Relatório não abre (falta browser) | Médio | Baixa | Salvar também como TXT |
| Pasta com 100k+ imagens trava UI | Médio | Média | Limite de 10k arquivos + aviso |

---

## 11. Roadmap Futuro

### V2 - CLI (Q2 2026)
- `brjoy-img optimize ./public --format webp --quality 85`
- Integração CI/CD (GitHub Actions)
- Modo watch (converte automaticamente ao adicionar imagens)

### V3 - Snippets & Responsive (Q3 2026)
- Gerador de `<picture>` com fallback
- Responsive variants (320w, 640w, 960w, 1280w)
- Deduplicação por hash

### V4 - Integrações (Q4 2026)
- Integração Cloudflare Images
- Integração AWS S3
- API REST para automação

---

## 12. Definição de Sucesso

**V1 é considerado sucesso se:**
- ✅ 100+ downloads nos primeiros 30 dias
- ✅ 70%+ dos usuários convertem >50 imagens
- ✅ NPS >40 (feedback positivo)
- ✅ 0 bugs críticos reportados
- ✅ 5+ menções orgânicas em redes sociais

---

## 13. Aprovações

| Stakeholder | Papel | Status | Data |
|-------------|-------|--------|------|
| BrJoy Team | Product Owner | ✅ Aprovado | 03/03/2026 |
| Dev Team | Engineering | 🔄 Em Revisão | - |
| Design Team | UX/UI | 🔄 Em Revisão | - |

---

**Próximos Passos:**
1. Revisar PRD com time técnico
2. Estimar esforço (story points)
3. Criar issues no GitHub
4. Iniciar Sprint 1 (Scan + Estrutura + Presets)

---

*Documento vivo - atualizar conforme feedback e descobertas durante desenvolvimento.*
