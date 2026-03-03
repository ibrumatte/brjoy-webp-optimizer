#!/usr/bin/env python3
"""
Test script for HTML report generation
"""
import sys
from pathlib import Path
from datetime import datetime

# Simular dados de conversão
conversion_details = [
    {"file": "hero.jpg", "before": 2500000, "after": 850000, "saved": 1650000, "percent": 66.0},
    {"file": "blog-post.jpg", "before": 1800000, "after": 720000, "saved": 1080000, "percent": 60.0},
    {"file": "thumbnail.jpg", "before": 450000, "after": 180000, "saved": 270000, "percent": 60.0},
    {"file": "avatar.png", "before": 320000, "after": 95000, "saved": 225000, "percent": 70.3},
    {"file": "banner.jpg", "before": 3200000, "after": 1100000, "saved": 2100000, "percent": 65.6},
]

output_folder = Path("/tmp/test-report")
output_folder.mkdir(exist_ok=True)

# Calcular estatísticas
total_before = sum(d["before"] for d in conversion_details)
total_after = sum(d["after"] for d in conversion_details)
total_saved = total_before - total_after
percent_saved = (total_saved / total_before * 100) if total_before > 0 else 0

success = 5
errors = 0
total = 5
duration = 12.5

# Top 10 que mais economizaram
top_10 = sorted(conversion_details, key=lambda x: x["saved"], reverse=True)[:10]

# Gerar HTML
html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BrJoy WebP Optimizer - Relatório de Conversão</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; 
               background: #f5f5f7; padding: 20px; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; 
                     border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .header {{ background: linear-gradient(135deg, #0a84ff 0%, #0070e0 100%); 
                  color: white; padding: 40px; border-radius: 12px 12px 0 0; }}
        .header h1 {{ font-size: 32px; margin-bottom: 8px; }}
        .header p {{ opacity: 0.9; font-size: 14px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                 gap: 20px; padding: 30px; }}
        .stat-card {{ background: #f8f8f8; padding: 20px; border-radius: 8px; }}
        .stat-card h3 {{ font-size: 14px; color: #666; margin-bottom: 8px; }}
        .stat-card .value {{ font-size: 28px; font-weight: bold; color: #111; }}
        .stat-card .sub {{ font-size: 12px; color: #999; margin-top: 4px; }}
        .stat-card.success .value {{ color: #10b981; }}
        .stat-card.error .value {{ color: #ef4444; }}
        .stat-card.savings .value {{ color: #0a84ff; }}
        .section {{ padding: 30px; border-top: 1px solid #e6e6ea; }}
        .section h2 {{ font-size: 20px; margin-bottom: 20px; color: #111; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ text-align: left; padding: 12px; border-bottom: 1px solid #e6e6ea; }}
        th {{ background: #f8f8f8; font-weight: 600; font-size: 12px; 
             color: #666; text-transform: uppercase; }}
        td {{ font-size: 14px; }}
        .file-name {{ font-family: 'Courier New', monospace; color: #0a84ff; }}
        .size {{ text-align: right; }}
        .savings {{ text-align: right; color: #10b981; font-weight: 600; }}
        .footer {{ padding: 20px 30px; background: #f8f8f8; border-radius: 0 0 12px 12px; 
                  text-align: center; font-size: 12px; color: #666; }}
        .export-btn {{ display: inline-block; margin: 10px 5px; padding: 10px 20px; 
                      background: #0a84ff; color: white; text-decoration: none; 
                      border-radius: 6px; font-size: 14px; }}
        .export-btn:hover {{ background: #0070e0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🖼️ Relatório de Conversão</h1>
            <p>BrJoy WebP Optimizer v1.1 • {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card success">
                <h3>Convertidos</h3>
                <div class="value">{success}</div>
                <div class="sub">de {total} arquivos</div>
            </div>
            <div class="stat-card error">
                <h3>Erros</h3>
                <div class="value">{errors}</div>
                <div class="sub">{(errors/total*100) if total > 0 else 0:.1f}% falhas</div>
            </div>
            <div class="stat-card savings">
                <h3>Economia Total</h3>
                <div class="value">{total_saved/1024/1024:.1f} MB</div>
                <div class="sub">{percent_saved:.1f}% redução</div>
            </div>
            <div class="stat-card">
                <h3>Tempo</h3>
                <div class="value">{int(duration//60)}:{int(duration%60):02d}</div>
                <div class="sub">{duration/success if success > 0 else 0:.2f}s por imagem</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 Resumo</h2>
            <table>
                <tr>
                    <th>Métrica</th>
                    <th class="size">Antes</th>
                    <th class="size">Depois</th>
                    <th class="size">Economia</th>
                </tr>
                <tr>
                    <td><strong>Tamanho Total</strong></td>
                    <td class="size">{total_before/1024/1024:.2f} MB</td>
                    <td class="size">{total_after/1024/1024:.2f} MB</td>
                    <td class="savings">-{total_saved/1024/1024:.2f} MB ({percent_saved:.1f}%)</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>🏆 Top 10 - Maior Economia</h2>
            <table>
                <tr>
                    <th>Arquivo</th>
                    <th class="size">Antes</th>
                    <th class="size">Depois</th>
                    <th class="size">Economia</th>
                </tr>"""

for item in top_10:
    html += f"""
                <tr>
                    <td class="file-name">{item['file']}</td>
                    <td class="size">{item['before']/1024:.1f} KB</td>
                    <td class="size">{item['after']/1024:.1f} KB</td>
                    <td class="savings">-{item['saved']/1024:.1f} KB ({item['percent']:.1f}%)</td>
                </tr>"""

html += f"""
            </table>
        </div>
        
        <div class="footer">
            <p><strong>Pasta de saída:</strong> {output_folder}</p>
            <p style="margin-top: 10px;">Gerado por BrJoy WebP Optimizer v1.1</p>
            <a href="https://github.com/ibrumatte/brjoy-webp-optimizer" class="export-btn">GitHub</a>
        </div>
    </div>
</body>
</html>"""

# Salvar relatório
report_path = output_folder / "conversion-report.html"
with open(report_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Relatório gerado: {report_path}")
print(f"📊 Estatísticas:")
print(f"   - Convertidos: {success}/{total}")
print(f"   - Economia: {total_saved/1024/1024:.1f} MB ({percent_saved:.1f}%)")
print(f"   - Tempo: {duration:.1f}s")
print(f"\n🌐 Abrindo no navegador...")

import subprocess
subprocess.run(["xdg-open", str(report_path)])
