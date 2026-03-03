#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
from pathlib import Path
from datetime import datetime

class ConversorHEIC:
    def __init__(self, root):
        self.root = root
        self.root.title("BrJoy Image Converter")
        self.root.geometry("700x700")
        self.root.configure(bg='#f5f5f7')
        self.root.resizable(False, False)
        
        # Definir ícone da janela
        try:
            icon_path = Path.home() / ".local/share/brjoy-image-converter/icon.webp"
            if icon_path.exists():
                # Converter webp para formato que Tkinter aceita
                subprocess.run(['convert', str(icon_path), '/tmp/brjoy_icon.png'], 
                             capture_output=True)
                icon = tk.PhotoImage(file='/tmp/brjoy_icon.png')
                self.root.iconphoto(True, icon)
        except:
            pass
        
        self.formato = tk.StringVar(value="webp")
        self.arquivos = []
        self.pasta_saida = None
        self.redimensionar = tk.BooleanVar(value=False)
        self.largura_max = tk.StringVar(value="1920")
        
        self.criar_interface()
        self.verificar_dependencias()
    
    def toggle_resize(self):
        """Ativa/desativa campo de largura"""
        if self.redimensionar.get():
            self.largura_entry.config(state=tk.NORMAL, bg='#ffffff')
        else:
            self.largura_entry.config(state=tk.DISABLED, bg='#f0f0f0')
    
    def verificar_dependencias(self):
        """Verifica se ImageMagick está instalado"""
        try:
            subprocess.run(['convert', '-version'], capture_output=True, check=True)
        except:
            resposta = messagebox.askyesno(
                "ImageMagick não encontrado",
                "O ImageMagick é necessário para converter imagens.\n\nDeseja instalar agora?"
            )
            if resposta:
                subprocess.run(['x-terminal-emulator', '-e', 'sudo apt install imagemagick'])
    
    def criar_pasta_sessao(self):
        """Cria pasta para a sessão atual"""
        if not self.pasta_saida:
            # Pega a pasta do primeiro arquivo selecionado
            pasta_origem = Path(self.arquivos[0]).parent
            
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            # Perguntar se quer renomear
            try:
                result = subprocess.run([
                    'zenity', '--entry',
                    '--title=Nome da pasta',
                    '--text=Nome para a pasta de saída:',
                    '--entry-text=BrJoy_' + timestamp
                ], capture_output=True, text=True)
                
                if result.returncode == 0 and result.stdout.strip():
                    nome_pasta = result.stdout.strip()
                else:
                    nome_pasta = 'BrJoy_' + timestamp
            except:
                nome_pasta = 'BrJoy_' + timestamp
            
            self.pasta_saida = pasta_origem / nome_pasta
            self.pasta_saida.mkdir(parents=True, exist_ok=True)
    
    def criar_interface(self):
        # Header
        header = tk.Frame(self.root, bg='#ffffff', height=100)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        titulo = tk.Label(header, text="BrJoy Image Converter", 
                         font=("Arial", 28, "bold"), bg='#ffffff', fg='#000000')
        titulo.pack(pady=(30, 5))
        
        # Container principal
        main_container = tk.Frame(self.root, bg='#f5f5f7')
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=25)
        
        # Card de configurações
        config_card = tk.Frame(main_container, bg='#ffffff', relief=tk.SOLID, bd=1)
        config_card.pack(fill=tk.X, pady=(0, 15))
        
        config_inner = tk.Frame(config_card, bg='#ffffff')
        config_inner.pack(padx=25, pady=20)
        
        # Formato
        tk.Label(config_inner, text="Formato de saída", 
                font=("Arial", 12, "bold"), bg='#ffffff', fg='#000000').pack(anchor=tk.W, pady=(0, 12))
        
        radio_frame = tk.Frame(config_inner, bg='#ffffff')
        radio_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Radiobutton(radio_frame, text="WebP (menor tamanho)", 
                      variable=self.formato, value="webp",
                      font=("Arial", 11), bg='#ffffff', fg='#000000',
                      selectcolor='#ffffff', activebackground='#ffffff',
                      highlightthickness=0).pack(anchor=tk.W, pady=3)
        
        tk.Radiobutton(radio_frame, text="PNG (máxima qualidade)", 
                      variable=self.formato, value="png",
                      font=("Arial", 11), bg='#ffffff', fg='#000000',
                      selectcolor='#ffffff', activebackground='#ffffff',
                      highlightthickness=0).pack(anchor=tk.W, pady=3)
        
        # Separador
        tk.Frame(config_inner, bg='#cccccc', height=1).pack(fill=tk.X, pady=15)
        
        # Redimensionamento
        tk.Checkbutton(config_inner, text="Redimensionar imagens", 
                      variable=self.redimensionar, command=self.toggle_resize,
                      font=("Arial", 11, "bold"), bg='#ffffff', fg='#000000',
                      selectcolor='#ffffff', activebackground='#ffffff',
                      highlightthickness=0).pack(anchor=tk.W, pady=(0, 12))
        
        resize_input = tk.Frame(config_inner, bg='#ffffff')
        resize_input.pack(fill=tk.X, padx=(20, 0))
        
        tk.Label(resize_input, text="Largura máxima:", 
                font=("Arial", 10), bg='#ffffff', fg='#333333').pack(side=tk.LEFT, padx=(0, 10))
        
        self.largura_entry = tk.Entry(resize_input, textvariable=self.largura_max,
                                      font=("Arial", 11), bg='#f0f0f0', fg='#000000',
                                      relief=tk.SOLID, bd=1, width=10, state=tk.DISABLED)
        self.largura_entry.pack(side=tk.LEFT)
        
        tk.Label(resize_input, text="px (altura proporcional)", 
                font=("Arial", 10), bg='#ffffff', fg='#333333').pack(side=tk.LEFT, padx=(10, 0))
        
        # Lista de arquivos
        files_card = tk.Frame(main_container, bg='#ffffff', relief=tk.SOLID, bd=1, height=200)
        files_card.pack(fill=tk.X, pady=(0, 15))
        files_card.pack_propagate(False)
        
        files_inner = tk.Frame(files_card, bg='#ffffff')
        files_inner.pack(fill=tk.BOTH, expand=True, padx=25, pady=(20, 15))
        
        tk.Label(files_inner, text="Arquivos selecionados", 
                font=("Arial", 12, "bold"), bg='#ffffff', fg='#000000').pack(anchor=tk.W, pady=(0, 10))
        
        list_frame = tk.Frame(files_inner, bg='#fafafa', relief=tk.SOLID, bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame, bg='#e0e0e0')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.files_listbox = tk.Listbox(list_frame, font=("Arial", 10), 
                                        bg='#fafafa', fg='#000000', 
                                        relief=tk.FLAT, bd=0, highlightthickness=0,
                                        yscrollcommand=scrollbar.set, selectmode=tk.NONE)
        self.files_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.config(command=self.files_listbox.yview)
        
        self.placeholder_label = tk.Label(list_frame, text="Nenhum arquivo selecionado", 
                                         font=("Arial", 11), bg='#fafafa', fg='#888888')
        self.placeholder_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Botões
        btn_container = tk.Frame(main_container, bg='#f5f5f7')
        btn_container.pack(fill=tk.X)
        
        self.btn_selecionar = tk.Button(btn_container, text="Selecionar Arquivos", 
                                        command=self.selecionar_arquivos,
                                        font=("Arial", 12, "bold"), bg='#0066CC', fg='#ffffff',
                                        padx=35, pady=14, cursor='hand2', relief=tk.FLAT,
                                        activebackground='#0052A3', activeforeground='#ffffff',
                                        borderwidth=0)
        self.btn_selecionar.pack(side=tk.LEFT, padx=(0, 12))
        
        self.btn_converter = tk.Button(btn_container, text="Converter", 
                                       command=self.converter,
                                       font=("Arial", 12, "bold"), bg='#cccccc', fg='#666666',
                                       padx=50, pady=14, cursor='hand2', relief=tk.FLAT,
                                       state=tk.DISABLED, borderwidth=0)
        self.btn_converter.pack(side=tk.LEFT)
    
    def selecionar_arquivos(self):
        try:
            result = subprocess.run([
                'zenity', '--file-selection',
                '--multiple',
                '--title=Selecione imagens para converter',
                '--file-filter=Imagens | *.heic *.HEIC *.jpg *.jpeg *.JPG *.JPEG *.png *.PNG *.bmp *.BMP *.tiff *.TIFF *.gif *.GIF *.webp *.WEBP',
                '--file-filter=Todos os arquivos | *'
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                arquivos = result.stdout.strip().split('|')
                self.arquivos = [arq for arq in arquivos if arq]
                
                self.files_listbox.delete(0, tk.END)
                self.placeholder_label.place_forget()
                
                for arq in self.arquivos:
                    self.files_listbox.insert(tk.END, f"  {Path(arq).name}")
                
                self.btn_converter.config(state=tk.NORMAL, bg='#28a745', fg='#ffffff',
                                         activebackground='#218838')
        except FileNotFoundError:
            arquivos = filedialog.askopenfilenames(
                title="Selecione imagens para converter",
                filetypes=[
                    ("Imagens", "*.heic *.HEIC *.jpg *.jpeg *.JPG *.JPEG *.png *.PNG *.bmp *.BMP *.tiff *.TIFF *.gif *.GIF *.webp *.WEBP"),
                    ("Todos os arquivos", "*.*")
                ]
            )
            
            if arquivos:
                self.arquivos = list(arquivos)
                
                self.files_listbox.delete(0, tk.END)
                self.placeholder_label.place_forget()
                
                for arq in self.arquivos:
                    self.files_listbox.insert(tk.END, f"  {Path(arq).name}")
                
                self.btn_converter.config(state=tk.NORMAL, bg='#28a745', fg='#ffffff',
                                         activebackground='#218838')
    
    def converter(self):
        if not self.arquivos:
            return
        
        self.criar_pasta_sessao()
        
        self.btn_converter.config(state=tk.DISABLED, bg='#cccccc', fg='#666666')
        self.btn_selecionar.config(state=tk.DISABLED, bg='#999999')
        
        # Conversão no thread principal para evitar acesso Tk fora da thread da UI.
        self.root.after(10, self._converter_thread)
    
    def _converter_thread(self):
        formato = self.formato.get()
        sucesso = 0
        erro = 0
        
        total = len(self.arquivos)
        
        for idx, arquivo in enumerate(self.arquivos, 1):
            arquivo_path = Path(arquivo)
            nome_saida = arquivo_path.stem + f'.{formato}'
            saida = self.pasta_saida / nome_saida
            
            try:
                # Atualizar lista
                self.files_listbox.delete(idx-1)
                self.files_listbox.insert(idx-1, f"  ⏳ {arquivo_path.name}")
                self.files_listbox.see(idx-1)
                
                # Comando de conversão
                cmd = ['convert', str(arquivo_path)]
                
                if self.redimensionar.get():
                    try:
                        largura = int(self.largura_max.get())
                        cmd.extend(['-resize', f'{largura}x>', '-quality', '90'])
                    except ValueError:
                        pass
                
                cmd.append(str(saida))
                
                subprocess.run(cmd, check=True, capture_output=True)
                
                self.files_listbox.delete(idx-1)
                self.files_listbox.insert(idx-1, f"  ✓ {arquivo_path.name}")
                sucesso += 1
            except Exception as e:
                self.files_listbox.delete(idx-1)
                self.files_listbox.insert(idx-1, f"  ✗ {arquivo_path.name}")
                erro += 1
        
        # Finalizar
        messagebox.showinfo("Concluído", 
                           f"Conversão finalizada!\n\n✓ {sucesso} convertidos\n✗ {erro} falhas\n\nPasta: {self.pasta_saida}")
        
        self.btn_converter.config(state=tk.NORMAL, bg='#28a745', fg='#ffffff')
        self.btn_selecionar.config(state=tk.NORMAL, bg='#0066CC')
        
        # Abrir pasta
        subprocess.run(['xdg-open', str(self.pasta_saida)])

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversorHEIC(root)
    root.mainloop()
