# BrJoy Web Optimizer

Pipeline de otimização de imagens para websites. Converta JPG/PNG para WebP em lote, mantenha estrutura de diretórios e veja quanto economizou.

## 🎯 Para Quem É

- Desenvolvedores frontend (Next.js, Astro, Hugo, Vite)
- Agências web otimizando sites de clientes
- Freelancers reduzindo custos de hospedagem
- Times melhorando Core Web Vitals

## ✨ Features V1

- ✅ Scan recursivo de pastas (ignora `node_modules`, `.git`, etc)
- ✅ 6 presets web (Hero, Blog, Thumbnail, Mobile, Avatar, Original)
- ✅ Slider de qualidade 60-100% (padrão: 85%)
- ✅ Mantém estrutura de diretórios
- ✅ Relatório HTML com economia de espaço
- ✅ Modo não-destrutivo (nunca sobrescreve originais)
- ✅ Drag & Drop de arquivos/pastas
- ✅ Atalhos de teclado (Ctrl+O, Delete, Ctrl+Enter)

## 🚀 Instalação Rápida

```bash
# 1. Clonar repositório
git clone https://github.com/brjoy/web-optimizer.git
cd web-optimizer

# 2. Instalar dependências
pip3 install tkinterdnd2

# 3. Instalar ImageMagick
sudo apt install imagemagick

# 4. Executar
python3 brjoy-converter
```

## 📖 Uso Básico

1. **Escanear**: Clique "📂 Escanear Pasta" e selecione pasta raiz
2. **Preset**: Escolha "Mobile Optimized" (recomendado)
3. **Converter**: Clique "✨ Converter (N)"
4. **Resultado**: Veja relatório e pasta de saída

**Exemplo:**
```
Entrada: /projeto/public (247 imagens, 156.8 MB)
Saída: /brjoy-output (247 imagens, 42.3 MB)
Economia: 114.5 MB (73%) 🎉
```

## 📊 Presets Web

| Preset | Dimensões | Qualidade | Uso |
|--------|-----------|-----------|-----|
| Hero Image | 1920x1080 | 85% | Banners, headers |
| Blog Post | 1200x630 | 85% | Open Graph, artigos |
| Thumbnail | 400x300 | 80% | Listagens, grids |
| Mobile Optimized | 800px | 80% | Mobile-first ⭐ |
| Avatar/Icon | 256x256 | 90% | Perfis, ícones |
| Original Quality | Mantém | 95% | Sem perda visual |

## 🎓 Guia Completo

Veja [GUIA.md](GUIA.md) para:
- Casos de uso detalhados
- Configurações avançadas
- Troubleshooting
- Dicas pro

## 📋 Roadmap

- **V1** (Atual): Desktop Pro - conversão em massa + relatórios ✅
- **V2** (Q2 2026): CLI para CI/CD
- **V3** (Q3 2026): Gerador de snippets `<picture>`
- **V4** (Q4 2026): Plugin WordPress + integrações CDN

## 🐛 Troubleshooting

**ImageMagick não encontrado?**
```bash
sudo apt install imagemagick
```

**Drag & Drop não funciona?**
```bash
pip3 install tkinterdnd2
```

**Conversão lenta?**
- Reduza qualidade para 80%
- Processe em lotes menores

## 🤝 Contribuindo

1. Fork o projeto
2. Crie branch (`git checkout -b feature/nova-feature`)
3. Commit (`git commit -m 'Add nova feature'`)
4. Push (`git push origin feature/nova-feature`)
5. Abra Pull Request

## 📄 Licença

MIT License - veja [LICENSE](LICENSE)

## 💬 Suporte

- 📧 Email: brjoy@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/brjoy/web-optimizer/issues)
- 💬 Discord: [BrJoy Community](https://discord.gg/brjoy)

---

**⭐ Se este projeto te ajudou, deixe uma estrela no GitHub!**
