#!/usr/bin/env python3
"""
Test AI Report Generation
"""
from pathlib import Path
from datetime import datetime

# Simular conversões
details = [
    {"file": "hero.png", "before": 2500000, "after": 850000, "saved": 1650000, "percent": 66.0},
    {"file": "blog-post.jpg", "before": 1800000, "after": 720000, "saved": 1080000, "percent": 60.0},
    {"file": "thumbnail.png", "before": 450000, "after": 180000, "saved": 270000, "percent": 60.0},
    {"file": "avatar.png", "before": 320000, "after": 95000, "saved": 225000, "percent": 70.3},
    {"file": "banner.jpg", "before": 3200000, "after": 1100000, "saved": 2100000, "percent": 65.6},
]

output_folder = Path("/tmp/test-ai-report")
output_folder.mkdir(exist_ok=True)
formato = "webp"

# Criar relatório TXT para IA
ai_report = f"""# BrJoy WebP Optimizer - AI Code Update Report
# Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# 
# INSTRUÇÕES PARA IA:
# Use este relatório para substituir URLs de imagens no código.
# Formato: ANTES → DEPOIS
# 
# Exemplo de prompt:
# "Substitua todas as URLs deste relatório no meu código fonte"
#
# ============================================================

"""

# Listar todas as conversões
ai_report += "# LISTA DE SUBSTITUIÇÕES\n"
ai_report += "# ----------------------\n\n"

for item in details:
    original_name = item["file"]
    name_without_ext = Path(original_name).stem
    new_name = f"{name_without_ext}.{formato}"
    
    ai_report += f"{original_name} → {new_name}\n"

# Adicionar seção CSV
ai_report += f"\n\n# FORMATO CSV (para importar em planilhas)\n"
ai_report += "# ----------------------------------------\n\n"
ai_report += "ANTES,DEPOIS,ECONOMIA_KB,ECONOMIA_PERCENT\n"

for item in details:
    original_name = item["file"]
    name_without_ext = Path(original_name).stem
    new_name = f"{name_without_ext}.{formato}"
    saved_kb = item["saved"] / 1024
    percent = item["percent"]
    
    ai_report += f"{original_name},{new_name},{saved_kb:.1f},{percent:.1f}\n"

# Adicionar exemplos de uso
ai_report += f"""

# EXEMPLOS DE SUBSTITUIÇÃO NO CÓDIGO
# -----------------------------------

# HTML:
# <img src="images/{details[0]['file']}" /> 
# ↓
# <img src="images/{Path(details[0]['file']).stem}.{formato}" />

# CSS:
# background-image: url('images/{details[0]['file']}');
# ↓
# background-image: url('images/{Path(details[0]['file']).stem}.{formato}');

# JavaScript/React:
# import hero from './images/{details[0]['file']}'
# ↓
# import hero from './images/{Path(details[0]['file']).stem}.{formato}'

# Markdown:
# ![Alt text](images/{details[0]['file']})
# ↓
# ![Alt text](images/{Path(details[0]['file']).stem}.{formato})

# ============================================================
# PROMPT SUGERIDO PARA IA:
# ============================================================
# 
# "Analise meu código e substitua todas as referências de imagens
# listadas neste relatório. Mantenha os caminhos relativos e absolutos.
# Procure em arquivos: HTML, CSS, JS, JSX, TSX, MD, JSON, etc."
#
# ============================================================
"""

# Salvar relatório para IA
ai_report_path = output_folder / "AI-CODE-UPDATE.txt"
with open(ai_report_path, "w", encoding="utf-8") as f:
    f.write(ai_report)

# Também salvar CSV puro
csv_path = output_folder / "conversions.csv"
with open(csv_path, "w", encoding="utf-8") as f:
    f.write("ANTES,DEPOIS,TAMANHO_ANTES_KB,TAMANHO_DEPOIS_KB,ECONOMIA_KB,ECONOMIA_PERCENT\n")
    for item in details:
        original_name = item["file"]
        name_without_ext = Path(original_name).stem
        new_name = f"{name_without_ext}.{formato}"
        before_kb = item["before"] / 1024
        after_kb = item["after"] / 1024
        saved_kb = item["saved"] / 1024
        percent = item["percent"]
        
        f.write(f"{original_name},{new_name},{before_kb:.1f},{after_kb:.1f},{saved_kb:.1f},{percent:.1f}\n")

print("✅ Relatórios gerados:")
print(f"   📄 {ai_report_path}")
print(f"   📊 {csv_path}")
print("\n📋 Conteúdo do AI-CODE-UPDATE.txt:")
print("=" * 60)
print(ai_report)
