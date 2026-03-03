# BrJoy Web Optimizer V1 - Guia de Uso

## 🚀 Instalação

```bash
# 1. Instalar dependências
pip3 install tkinterdnd2

# 2. Instalar ImageMagick
sudo apt install imagemagick

# 3. Executar
python3 brjoy-converter
```

## 📖 Como Usar

### 1. Escanear Pasta
1. Clique em "📂 Escanear Pasta"
2. Selecione a pasta raiz do seu projeto (ex: `/projeto/public`)
3. Aguarde o scan (ignora `node_modules`, `.git`, etc)
4. Veja lista de arquivos encontrados com tamanhos

### 2. Aplicar Preset
Escolha um preset otimizado para web:
- **Hero Image**: 1920x1080, 85% (banners, headers)
- **Blog Post**: 1200x630, 85% (Open Graph, artigos)
- **Thumbnail**: 400x300, 80% (listagens, grids)
- **Mobile Optimized**: 800px largura, 80% (mobile-first)
- **Avatar/Icon**: 256x256, 90% (perfis, ícones)
- **Original Quality**: Sem resize, 95% (conversão sem perda)

### 3. Ajustar Configurações
- **Formato**: WebP (recomendado) ou PNG
- **Qualidade**: Slider 60-100% (padrão: 85%)
- **Recorte 1:1**: Crop quadrado centralizado
- **Redimensionar**: Largura customizada em px

### 4. Converter
1. Clique "✨ Converter (N)"
2. Aguarde processamento (barra de progresso)
3. Relatório HTML abre automaticamente
4. Pasta de saída abre no gerenciador de arquivos

## 🎯 Casos de Uso

### Otimizar site Next.js
```
1. Escanear: /meu-projeto/public
2. Preset: "Mobile Optimized"
3. Converter
4. Copiar brjoy-output/ para /public/
```

### Preparar imagens para blog
```
1. Escanear: /blog/uploads
2. Preset: "Blog Post" (1200x630 Open Graph)
3. Qualidade: 85%
4. Converter
```

### Criar thumbnails em lote
```
1. Escanear: /produtos/fotos
2. Preset: "Thumbnail" (400x300)
3. Qualidade: 80%
4. Converter
```

## 📊 Relatório

Após conversão, você verá:
- Total de arquivos processados
- Tamanho original vs final
- Economia em MB e %
- Tempo de processamento
- Status por arquivo (✓ sucesso, ✗ erro)

## ⌨️ Atalhos

- `Ctrl+O`: Escanear pasta
- `Delete`: Remover selecionados
- `Ctrl+Enter`: Converter

## 🔧 Configurações Avançadas

### Manter Estrutura de Diretórios
Por padrão, a estrutura de pastas é preservada:
```
Origem:              Destino:
/public/             /brjoy-output/
  hero.jpg    →        hero.webp
  blog/                blog/
    post1.png  →         post1.webp
```

### Qualidade Recomendada
- **60-70%**: Economia máxima (perda visual perceptível)
- **80-85%**: Sweet spot ⭐ (melhor custo-benefício)
- **90-95%**: Alta fidelidade (quase sem perda)
- **100%**: Lossless (apenas para PNG com transparência)

## 🐛 Troubleshooting

### "ImageMagick não encontrado"
```bash
sudo apt install imagemagick
```

### "Conversão muito lenta"
- Reduza qualidade para 80%
- Processe em lotes menores (<500 imagens)
- Feche outros programas

### "Erro ao converter arquivo X"
- Arquivo pode estar corrompido
- Formato não suportado
- Permissões de leitura

## 📈 Performance

- **1000 imagens**: ~3-5min
- **Economia média**: 60-80%
- **Formatos suportados**: JPG, PNG, HEIC, BMP, TIFF, GIF, WebP

## 🎓 Dicas Pro

1. **Sempre teste com 10 imagens primeiro** antes de processar milhares
2. **Mantenha originais** (modo não-destrutivo ativo por padrão)
3. **Use preset "Mobile Optimized"** para 90% dos casos web
4. **Qualidade 85%** é o sweet spot para web
5. **Verifique relatório** para identificar imagens problemáticas

## 🚀 Próximas Versões

- **V2**: CLI para CI/CD (`brjoy-img optimize ./public`)
- **V3**: Gerador de snippets `<picture>` com fallback
- **V4**: Cloud integrations (Cloudflare, S3) and CDN

---

**Feedback?** Abra uma issue no GitHub ou envie email para brjoy@example.com
