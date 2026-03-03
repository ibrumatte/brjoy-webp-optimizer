#!/bin/bash
# Script de instalação do drag & drop para BrJoy Image Converter

echo "🔧 Instalando dependência para Drag & Drop..."

# Tentar com pip3
if command -v pip3 &> /dev/null; then
    pip3 install --user tkinterdnd2
    
    if [ $? -eq 0 ]; then
        echo "✅ tkinterdnd2 instalado com sucesso!"
        echo ""
        echo "Teste o drag & drop:"
        echo "  python3 -c 'import tkinterdnd2; print(\"OK\")'"
    else
        echo "❌ Erro ao instalar. Tente manualmente:"
        echo "  pip3 install --user tkinterdnd2"
    fi
else
    echo "❌ pip3 não encontrado. Instale primeiro:"
    echo "  sudo apt install python3-pip"
    echo ""
    echo "Depois execute:"
    echo "  pip3 install --user tkinterdnd2"
fi

echo ""
echo "📝 Nota: O app funciona sem tkinterdnd2, mas sem drag & drop."
