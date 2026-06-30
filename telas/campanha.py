import tkinter as tk

janela = tk.Tk()
janela.title("Cadastro de Campanha")
janela.geometry("600x400")

# Título
titulo = tk.Label(janela, text="Cadastro de Campanha", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# Campo nome
tk.Label(janela, text="Nome da campanha").pack()
entrada_nome = tk.Entry(janela, width=40)
entrada_nome.pack(pady=5)

# Campo objetivo
tk.Label(janela, text="Objetivo").pack()
entrada_objetivo = tk.Entry(janela, width=40)
entrada_objetivo.pack(pady=5)

# Campo data de início
tk.Label(janela, text="Data de início").pack()
entrada_data_inicio = tk.Entry(janela, width=40)
entrada_data_inicio.pack(pady=5)

# Campo data de fim
tk.Label(janela, text="Data de fim").pack()
entrada_data_fim = tk.Entry(janela, width=40)
entrada_data_fim.pack(pady=5)

# Campo gestor
tk.Label(janela, text="Gestor responsável").pack()
entrada_gestor = tk.Entry(janela, width=40)
entrada_gestor.pack(pady=5)

# Botão
botao_salvar = tk.Button(janela, text="Salvar")
botao_salvar.pack(pady=10)

janela.mainloop()
