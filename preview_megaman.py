import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import codecs
from tkinter import Scrollbar
from PIL import Image, ImageTk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import webbrowser
from tkinter import ttk
import json
from tkinter import Button
from pytube import YouTube
import os








def search_text():
    # Limpar marcações anteriores
    translated_text_box.tag_remove("search", "1.0", tk.END)

    search_query = search_entry.get()

    # Obter todo o texto da caixa de texto traduzido
    translated_text = translated_text_box.get("1.0", tk.END).lower()

    # Remover todas as marcações existentes
    translated_text_box.tag_remove("search", "1.0", tk.END)

    # Iniciar a busca a partir do início da caixa de texto
    start_index = "1.0"

    occurrences = 0

    while True:
        # Procurar o texto na caixa de texto traduzido a partir da posição atual
        start_index = translated_text_box.search(search_query, start_index, tk.END)

        if not start_index:
            break

        end_index = f"{start_index}+{len(search_query)}c"

        # Adicionar uma nova marcação
        translated_text_box.tag_add("search", start_index, end_index)

        # Atualizar a posição de início para evitar encontrar a mesma ocorrência repetidamente
        start_index = end_index

        occurrences += 1

    # Configurar a aparência da marcação
    translated_text_box.tag_configure("search", background="red")

    if occurrences > 0:
        # Rolar para a primeira ocorrência (se houver alguma)
        first_index = translated_text_box.tag_nextrange("search", "1.0")
        if first_index:
            translated_text_box.see(first_index[0])
        
        messagebox.showinfo("Ocorrências Encontradas!", f"Foram encontradas {occurrences} ocorrências.")
    else:
        messagebox.showinfo("Nenhuma Ocorrência Encontrada", "Nenhuma ocorrência foi encontrada.")

translated_text_history = []

  # Adicione essa linha no início do seu código para armazenar o estado original

def undo_translated_text(event=None):
    global translated_text_history
    if len(translated_text_history) > 1:
        current_text = translated_text_box.get("1.0", "end-1c")
        translated_text_history.pop()  # Remove the current state
        previous_text = translated_text_history[-1]  # Get the previous state
        translated_text_box.delete("1.0", "end")
        translated_text_box.insert("1.0", previous_text)

def update_translated_text_history(event=None):
    global translated_text_history
    current_text = translated_text_box.get("1.0", "end-1c")
    if not translated_text_history or translated_text_history[-1] != current_text:
        translated_text_history.append(current_text)

def on_text_change(event):
    update_translated_text_history()



current_language = "Português do Brasil" 

scroll_speed_factor = 0.001


# Função para sincronizar a rolagem do mouse


# Configurar o scrollbar para usar a função de sincronização


dark_theme = {
    'bg': 'black',
    'fg': 'white',
    'highlightbackground': 'black',
    'highlightcolor': 'white',
    'selectbackground': 'white',
    'selectforeground': 'black',
    'insertbackground': 'white',
    'insertwidth': 2,
    'font': ('Arial', 12),
}




def load_translations(language):
    global current_language
    current_language = language
    
    with open("translations.json", "r", encoding="utf-8") as file:
        translations = json.load(file)
        return translations.get(language, translations["English"])
    
def update_interface_text():
    translations = load_translations(current_language)
    
    
   
    translated_text_label.config(text=translations["TranslatedText"])
    load_table_button.config(text=translations["OpenTable"])
    load_translated_button.config(text=translations["OpenTextExtract"])
    

   
  
    all_replace_button.config(text=translations["Allreplace"])
    clear_button.config(text=translations["ClearText"])
    save_button.config(text=translations["SaveText"])
    exibir_creditos_button.config(text=translations["About"])
    language_label.config(text=translations["SelectLanguage"])
   # english_button.config(text=translations["LanguageEnglish"])
   # portuguese_button.config(text=translations["LanguagePortuguese"])
    exibir_creditos_button.config(text=translations["Credits"])
    text_label.config(text=translations["Label"])
   
    window.title(f"Preview MegaMan Legends - Developed By Sora Leon")
    
    
    


def set_english_language():
    change_language("English")

def set_portuguese_language():
    change_language("Português do Brasil")

def set_spanish_language():
    change_language("Español")

def change_language(language):
    global current_language
    current_language = language
   
    update_interface_text()
    update_image()




hex_table={}



def credits():
    message = ("Desenvolvido por Sora Leon\nVersão 1.0\nFerramenta Para Preview: Megaman Legends [PSX]\nTodos os Direitos Reservados Sora Leon™")
    messagebox.showinfo("Créditos", message,)
    webbrowser.open("https://www.youtube.com/@SoraLeon")
    webbrowser.open("https://digi-translations.blogspot.com/")
    

    




def insert_newlines(text, max_line_length=26):
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        if "{0a}" in line:
            parts = line.split("{0a}")
            for part in parts:
                while len(part) > max_line_length:
                    new_lines.append(part[:max_line_length])
                    part = part[max_line_length:]
                if part:
                    new_lines.append(part)
        else:
            while len(line) > max_line_length:
                new_lines.append(line[:max_line_length])
                line = line[max_line_length:]
            if line:
                new_lines.append(line)
    return '\n'.join(new_lines)

from PIL import Image, ImageDraw, ImageFont, ImageTk

def update_image():
    text = text_entry.get('1.0', 'end-1c')
    
    # Limita o número de linhas a 3
    lines = text.split('\n')[:3]

    # Limita cada linha a 29 caracteres e insere {0a} para quebrar linhas
    for i, line in enumerate(lines):
        lines[i] = insert_newlines(line)

    text = "\n".join(lines)
    
    # Substitui {0a} por quebra de linha
    text = text.replace("{0a}", "\n")
    text = text.replace("{0A}", "\n")  # Considera {0A} como quebra de linha também
    
    image = Image.open("previewer.png")
    
    # Configura a posição e tamanho do texto com base nas dimensões da imagem
    text_x = 30  # Convertendo cm para pixels (21 pixels = 1 cm)
    text_y = 30  # Convertendo cm paa pixels (29.7 pixels = 1 cm)

    draw = ImageDraw.Draw(image)
    font_size = 18  # Tamanho da fonte (ajustado para caber 3 linhas de 29 caracteres)
    
    font = ImageFont.truetype("msgothic.ttc", font_size)
    
    lines = text.split('\n')[:3]
    for i, line in enumerate(lines):
        x_position = text_x
        for char in line:
            # Ajusta a posição horizontal apenas para os caracteres específicos
            if char.lower() in ['i', 'í',]:
                x_position += -3  # Ajusta a posição para a direita antes de desenhar o caractere
                draw.text((x_position, text_y + i * (font_size)), char, fill="white", font=font)
                x_position += font.getsize(char)[-0]  # Ajusta o espaçamento entre os caracteres

            elif char.lower() in ['a', 'á', 'ã', 'à']:
                x_position += -0  # Ajusta a posição para a direita antes de desenhar o caractere
                draw.text((x_position, text_y + i * (font_size)), char, fill="white", font=font)
                x_position += font.getsize(char)[-0]  # Ajusta o espaçamento entre os caracteres


            else:
                draw.text((x_position, text_y + i * (font_size)), char, fill="white", font=font)
                x_position += font.getsize(char)[0]

              

            

    photo = ImageTk.PhotoImage(image)

    preview_label.configure(image=photo)
    preview_label.image = photo

# Atualize a função load_stb_text para exibir a contagem de linhas



def load_translated_text():
    file_path = filedialog.askopenfilename(title="Escolha o arquivo de texto editado",
                                           filetypes=[("Arquivos de texto", "*.txt")])
    if file_path:
        try:
            with codecs.open(file_path, 'r', encoding='utf-8') as file:
                translated_text = file.read()

                # Substituir caracteres usando a tabela hex_table, de forma invertida
                translated_text = reverse_replace_characters(translated_text)

                translated_text_box.delete(1.0, tk.END)
                translated_text_box.insert(tk.END, translated_text)
        except FileNotFoundError:
            translated_text_box.delete(1.0, tk.END)

def reverse_replace_characters(text):
    global hex_table

    reversed_hex_table = {v: k for k, v in hex_table.items()}

    for value, char in reversed_hex_table.items():
        text = text.replace(value, char)

    return text







def load_hex_table():
    global hex_table
    file_path = filedialog.askopenfilename(title="Escolha o arquivo de tabela",
                                           filetypes=[("Arquivos de texto", "*.txt")])
    if file_path:
        try:
            with codecs.open(file_path, 'r', encoding='utf-8') as file:
                hex_table = {}
                for line in file:
                    line = line.strip()  # Remove espaços em branco no início e no final da linha
                    if '=' in line:
                        char, value = line.split('=', 1)  # Divida a linha na primeira ocorrência do "="
                        hex_table[char] = value
                messagebox.showinfo("Alerta Berserk!", "Tabela carregada com sucesso!")
        except FileNotFoundError:
            pass

def save_translated_text():
    translated_text = translated_text_box.get('1.0', 'end-1c')  # Obtém o texto traduzido

    for char, value in hex_table.items():
        translated_text = translated_text.replace(char, value)

    file_path = filedialog.asksaveasfilename(title="Salvar Texto Traduzido", defaultextension=".txt",
                                             filetypes=[("Arquivos de texto", "*.txt")])

    if file_path:
        with codecs.open(file_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)


def all_replace():
    file_paths = filedialog.askopenfilenames(title="Escolha os arquivos .txt para substituição de caracteres",
                                            filetypes=[("Arquivos de texto", "*.txt")])

    for file_path in file_paths:
        with codecs.open(file_path, 'r', encoding='utf-8') as file:
            original_text = file.read()
        
        # Aplica a substituição usando a tabela hex_table
        translated_text = original_text
        for char, value in hex_table.items():
            translated_text = translated_text.replace(char, value)
        
        with codecs.open(file_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)
            message = ("Substituição de todos caracteres concluída!")
            messagebox.showinfo("Substituição Completa!", message)



def clear_text():
    translated_text_box.config(state=tk.NORMAL)
    translated_text_box.delete(1.0, tk.END)
    translated_text_box.config(state=tk.DISABLED)
   # line_numbers_box.config(state=tk.NORMAL)
   # line_numbers_box.delete(1.0, tk.END)
   # line_numbers_box.config(state=tk.DISABLED)
    
    translated_text_box.delete(1.0, tk.END)

            

def ask_autosave():
    result = messagebox.askquestion("Seleção de Idiomas", "Deseja salvar automaticamente o arquivo .txt?")
    if result == "yes":
        # Código para salvar automaticamente
        save_translated_text()
    else:
       
        pass


window = tk.Tk()
window.title("Preview Megaman Legends - Desenvolvido Por Sora Leon")

window.geometry("780x630")

load_table_button = tk.Button(window, text="Abrir Tabela")
load_table_button.grid(row=0, column=0)
load_table_button.config(command=load_hex_table)


load_translated_button = tk.Button(window, text="Abrir .TXT")
load_translated_button.grid(row=0, column=1)
load_translated_button.config(command=load_translated_text)

clear_button = tk.Button(window, text="Apagar Texto")
clear_button.grid(row=0, column=2)
clear_button.config(command=clear_text)

save_button = tk.Button(window, text="Salvar")
save_button.grid(row=0, column=3)
save_button.config(command=save_translated_text)



all_replace_button = tk.Button(window, text="Acentuar vários .TXT", command=all_replace)
all_replace_button.grid(row=0, column=4)

exibir_creditos_button = tk.Button(window, text="Sobre")
exibir_creditos_button.config(command=credits)
exibir_creditos_button.grid(row=0, column=10, columnspan=3, sticky="n")
exibir_creditos_button.place(x=350, y=0) 

cabecalho = bytes.fromhex("53 54 42 20 00 00 00 00")



translated_text_label = tk.Label(window, text="Texto")
translated_text_label.grid(row=1, column=1, columnspan=3, sticky="n")
translated_text_label.config(anchor="center")










text_frame = tk.Frame(window)
text_frame.grid(row=2, column=0, columnspan=6, sticky="n")






translated_text_box = tk.Text(text_frame, wrap=tk.WORD, width=36, height=20)
translated_text_box.grid(row=0, column=1, columnspan=4)
translated_text_box.config(selectbackground='blue')













window.iconbitmap(r'MEGA.img')
image_frame = tk.Frame(window)
image_frame.grid(row=2, column=10, rowspan=10, padx=20, pady=20, sticky="n")

image = Image.open("previewer.png")

preview_image = ImageTk.PhotoImage(image)

preview_label = tk.Label(image_frame, image=preview_image)
preview_label.grid(row=0, column=0)

# Crie a caixa de diálogo para inserir texto na imagem
text_frame = tk.Frame(window)
text_frame.grid(row=3, column=10, padx=20, pady=20, sticky="n")

text_label = tk.Label(text_frame, text="Preview - Digite para Visualizar")
text_label.grid(row=0, column=0, sticky="n")


text_entry = tk.Text(text_frame, width=40, height=3)
text_entry.grid(row=1, column=0, sticky="n")
text_entry.bind("<KeyRelease>", lambda event: update_image())
text_entry.config(selectbackground='blue')



background_image = tk.PhotoImage(file="MEG.img")

canvas = tk.Canvas(window, width=329, height=199)  
canvas.grid(row=3, column=0, columnspan=7)
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Elementos da interface para seleção de idioma
language_label = tk.Label(text_frame, text="Seleção de Idioma:")
language_label.grid(row=15, column=0, columnspan=1, pady=(1, 0))

# Substitua os botões de seleção de idioma por uma barra seletiva
s = ttk.Style()  # Crie um objeto de estilo

# Após a criação do Combobox, configure a cor do texto para a cor desejada, por exemplo, preta (black).
language_slider = ttk.Combobox(text_frame, values=["Português do Brasil", "English", "Español", "日本語", "Italiano", "Português de Portugal","Russian"])
language_slider.set(current_language)
language_slider.grid(row=16, column=0, columnspan=2, sticky="n")

# Configure a cor do texto (foreground) para preto.
language_slider.config(foreground="black")
language_slider.config(background="black")

language_slider.bind("<<ComboboxSelected>>", lambda event: change_language(language_slider.get()))





window.tk_setPalette(background=dark_theme['bg'], foreground=dark_theme['fg'])
#original_text_box.config(bg=dark_theme['bg'], fg=dark_theme['fg'], insertbackground=dark_theme['insertbackground'], font=dark_theme['font'])
translated_text_box.config(bg=dark_theme['bg'], fg=dark_theme['fg'], insertbackground=dark_theme['insertbackground'], font=dark_theme['font'])
#line_numbers_box.config(bg=dark_theme['bg'], fg=dark_theme['fg'], insertbackground=dark_theme['insertbackground'], font=dark_theme['font'])
preview_label.config(bg=dark_theme['bg'], fg=dark_theme['fg'])
text_label.config(bg=dark_theme['bg'], fg=dark_theme['fg'])
text_entry.config(bg=dark_theme['bg'], fg=dark_theme['fg'], insertbackground=dark_theme['insertbackground'], font=dark_theme['font'])
canvas.config(bg=dark_theme['bg'])

#text_scrollbar.config(bg=dark_theme['bg'], troughcolor=dark_theme['bg'], activebackground=dark_theme['bg'])

# Configurar o seletor de idioma com cores personalizadas
language_slider.config(style="Dark.TCombobox")
s = ttk.Style()
s.theme_create("dark", parent="alt", settings={
    "TCombobox": {
        "configure": {
            "selectbackground": dark_theme['selectbackground'],
            "fieldbackground": dark_theme['bg'],
            "background": dark_theme['bg'],
            "foreground": dark_theme['fg'],
            "font": dark_theme['font'],
        },
    }
})

#translated_text_box.bind("<MouseWheel>", sync_scroll)
#line_numbers_box.bind("<MouseWheel>", sync_scroll)

window.bind("<Control-z>", undo_translated_text)
translated_text_box.bind("<KeyRelease>", update_translated_text_history)

search_label = tk.Label(window, text="Pesquisar Texto:")
search_label.grid(row=0, column=10, sticky="n")
search_label.place(x=420, y=23) 

# Entry
search_entry = tk.Entry(window)
search_entry.grid(row=1, column=10, sticky="n", padx=(0, 2)) 
search_entry.config(selectbackground='blue')
  # Adiciona espaço à direita do Entry

search_button = tk.Button(window, text="Pesquisar", command=search_text)
search_button.grid(row=1, column=10, sticky="n",)
search_button.place(x=645, y=23) 

window.grid_columnconfigure(10, minsize=5)



window.mainloop()
