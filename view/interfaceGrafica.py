import tkinter as tk
from tkinter import filedialog, messagebox
from controller.controlador import Controlador

# Função de retorno à tela inicial (fechar a tela de resultados)
def voltar_a_tela_inicial(janela_resultados):
    janela_resultados.destroy()  # Fecha apenas a janela de resultados

def iniciar_interface():
    root = tk.Tk()
    root.title("SISPAMER")
    root.geometry("800x600")
    root.configure(bg="gray")

    controlador = Controlador(voltar_callback=voltar_a_tela_inicial)
    #Titlulo
    titulo = tk.Label(root, text="SISPAMER", font=("Arial", 24), bg="gray", fg="black")
    titulo.pack(pady=10)

    subtitulo = tk.Label(root, text="Sistema para Progressão por Méritos", font=("Arial", 16), bg="gray", fg="black")
    subtitulo.pack(pady=10)

    botoes_frame = tk.Frame(root, bg="gray")
    botoes_frame.pack(pady=20)

    #Seleção de arquivo
    def selecionar_arquivo():
        caminho = filedialog.askopenfilename(
            title="Selecione a Planilha",
            filetypes=[("Arquivos Excel", "*.xlsx;*.xls")]
        )
        if caminho:
            controlador.caminho_arquivo = caminho
            messagebox.showinfo("Arquivo Selecionado", f"Arquivo selecionado: {caminho}")
        else:
            messagebox.showwarning("Aviso", "Nenhum arquivo foi selecionado.")

    botao_selecionar = tk.Button(
    botoes_frame, text="📂", font=("Arial", 14),
    command=selecionar_arquivo, bg="black", fg="gray", width=3, height=1)
    botao_selecionar.pack(side="right", padx=2)

    # Botão para processar planilha
    def processar_planilha():
        if not hasattr(controlador, 'caminho_arquivo') or not controlador.caminho_arquivo:
            messagebox.showerror("Erro", "Nenhum arquivo foi selecionado.")
        else:
            controlador.acionar_leitura_planilha(controlador.caminho_arquivo)

    botao_processar = tk.Button(
    botoes_frame, text="Processar Planilha", font=("Arial", 14),
    command=processar_planilha, bg="black", fg="gray", width=20, height=1)
    botao_processar.pack(side="right", padx=2)

    #Configuração de regras
    janela_configuracoes = None
    def abrir_configuracoes():
        nonlocal janela_configuracoes 
        
        if janela_configuracoes is not None and tk.Toplevel.winfo_exists(janela_configuracoes):
            janela_configuracoes.lift()
            janela_configuracoes.focus_force()
            return
        
        janela_configuracoes = tk.Toplevel()
        janela_configuracoes.title("Configurações de Regras de Negócio")
        janela_configuracoes.geometry("500x400")
        janela_configuracoes.configure(bg="gray")

        def on_close():
            nonlocal janela_configuracoes
            janela_configuracoes.destroy()
            janela_configuracoes = None

        janela_configuracoes.protocol("WM_DELETE_WINDOW", on_close)

        #Título
        titulo_config = tk.Label(janela_configuracoes, text="Configurações", font=("Arial", 20), bg="gray", fg="black")
        titulo_config.pack(pady=20)

        #Campo para meses
        label_meses = tk.Label(janela_configuracoes, text="Meses para Interstício:", font=("Arial", 14), bg="gray", fg="black")
        label_meses.pack(pady=10)
        entry_meses = tk.Entry(janela_configuracoes, font=("Arial", 14))
        entry_meses.insert(0, str(controlador.meses_intersticio))
        entry_meses.pack(pady=5)

        #Campo para nota de corte
        label_nota = tk.Label(janela_configuracoes, text="Nota de Corte:", font=("Arial", 14), bg="gray", fg="black")
        label_nota.pack(pady=10)
        entry_nota = tk.Entry(janela_configuracoes, font=("Arial", 14))
        entry_nota.insert(0, str(controlador.nota_corte))
        entry_nota.pack(pady=5)

        #Botão para salvar configurações
        def salvar_configuracoes():
            try:
                meses = int(entry_meses.get())
                nota = float(entry_nota.get())
                controlador.atualizar_configuracoes(meses, nota)
                messagebox.showinfo("Configurações", f"Configurações salvas:\nMeses: {meses}\nNota de corte: {nota}")
                janela_configuracoes.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores válidos.")

        botao_salvar = tk.Button(janela_configuracoes, text="Salvar Configurações", font=("Arial", 14),
                                 command=salvar_configuracoes, bg="black", fg="gray")
        botao_salvar.pack(pady=20)

    engrenagem = tk.Button(root, text="\u2699", font=("Arial", 20), bg="gray", fg="black",
                       command=abrir_configuracoes, bd=0, highlightthickness=0)
    engrenagem.place(relx=0.95, rely=0.95, anchor="se")

    def fechar_interface():
        root.quit()
        root.destroy()

    # Conectando o botão de fechar da janela ao fechamento correto
    root.protocol("WM_DELETE_WINDOW", fechar_interface)
    root.mainloop()