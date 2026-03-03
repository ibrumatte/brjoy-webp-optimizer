#!/usr/bin/env python3
"""
Teste automatizado de conversão
"""
import subprocess
from pathlib import Path
import time
import tempfile
import sys

print("🧪 Teste Automatizado - BrJoy WebP Optimizer")
print("=" * 50)
print()

# Verificar dependências
print("1️⃣ Verificando dependências...")
try:
    result = subprocess.run(["convert", "-version"], capture_output=True, check=True)
    print("   ✅ ImageMagick OK")
except:
    print("   ❌ ImageMagick não encontrado")
    exit(1)

try:
    import PIL
    print("   ✅ Pillow OK")
except:
    print("   ⚠️  Pillow não encontrado (preview desabilitado)")

print()

# Verificar imagens de teste
print("2️⃣ Verificando imagens de teste...")
test_dir = Path("/tmp/test-images")
if not test_dir.exists():
    print("   ⚠️  Pasta de teste não existe, criando fixture...")
    test_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(["convert", "-size", "800x600", "xc:blue", str(test_dir / "blue.jpg")], check=True, capture_output=True)

images = list(test_dir.glob("*.jpg"))
print(f"   ✅ {len(images)} imagens encontradas")
if not images:
    print("   ❌ Nenhuma imagem de teste encontrada")
    sys.exit(1)

for img in images:
    size_kb = img.stat().st_size / 1024
    print(f"      - {img.name}: {size_kb:.1f} KB")

print()

# Criar pasta de saída
print("3️⃣ Criando pasta de saída...")
output_dir = Path(tempfile.mkdtemp(prefix="brjoy-test-output-"))
print(f"   ✅ {output_dir}")

print()

# Converter imagens
print("4️⃣ Convertendo imagens...")
start_time = time.time()
falhas = 0

for i, img in enumerate(images, 1):
    output = output_dir / f"{img.stem}.webp"
    cmd = ["convert", str(img), "-quality", "85", str(output)]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        size_before = img.stat().st_size / 1024
        size_after = output.stat().st_size / 1024
        saved = size_before - size_after
        percent = (saved / size_before) * 100
        print(f"   ✅ {img.name} → {output.name}")
        print(f"      Antes: {size_before:.1f} KB | Depois: {size_after:.1f} KB | Economia: {saved:.1f} KB ({percent:.1f}%)")
    except Exception as e:
        falhas += 1
        print(f"   ❌ Erro: {e}")

duration = time.time() - start_time
print()
print(f"   ⏱️  Tempo total: {duration:.2f}s")

print()

# Verificar saída
print("5️⃣ Verificando arquivos gerados...")
webp_files = list(output_dir.glob("*.webp"))
print(f"   ✅ {len(webp_files)} arquivos WebP criados")

if len(webp_files) != len(images):
    print("   ❌ Quantidade de arquivos gerados não confere com entradas")
    falhas += 1

total_before = sum(img.stat().st_size for img in images)
total_after = sum(f.stat().st_size for f in webp_files)
total_saved = total_before - total_after
percent_saved = (total_saved / total_before) * 100

print()
print("📊 RESUMO:")
print(f"   Total antes: {total_before/1024:.1f} KB")
print(f"   Total depois: {total_after/1024:.1f} KB")
print(f"   Economia: {total_saved/1024:.1f} KB ({percent_saved:.1f}%)")

print()
if falhas > 0:
    print(f"❌ TESTE FALHOU ({falhas} problema(s))")
    print(f"📁 Arquivos em: {output_dir}")
    sys.exit(1)

print("✅ TESTE COMPLETO!")
print()
print(f"📁 Arquivos em: {output_dir}")
