import tkinter as tk
from controller.controlador import Controlador

def iniciar_interface():
    root = tk.Tk()
    root.title("Progressão TAE")
    root.geometry("300x200")

    # Função de retorno à tela inicial (fechar a tela de resultados)
    def voltar_a_tela_inicial(janela_resultados):
        janela_resultados.destroy()  # Fecha apenas a janela de resultados

    # Passando a função de retorno para o Controlador
    controlador = Controlador(voltar_callback=voltar_a_tela_inicial)

    meses_var = tk.IntVar(value=18)

    label = tk.Label(root, text="Selecione o período de interstício:")
    label.pack(pady=5)

    radio_18 = tk.Radiobutton(root, text="18 meses", variable=meses_var, value=18)
    radio_12 = tk.Radiobutton(root, text="12 meses", variable=meses_var, value=12)
    radio_18.pack()
    radio_12.pack()

    botao = tk.Button(root, text="Selecionar Planilha", command=lambda: controlador.acionar_leitura_planilha(meses_var.get()))
    botao.pack(pady=20)

    # Função para fechar corretamente
    def fechar_interface():
        root.quit()  # Encerra o loop principal do Tkinter
        root.destroy()  # Destrói a janela para liberar os recursos

    # Conectando o botão de fechar da janela ao fechamento correto
    root.protocol("WM_DELETE_WINDOW", fechar_interface)

    root.mainloop()
