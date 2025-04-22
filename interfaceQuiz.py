import subprocess
import tkinter as tk
from random import choice

# Define o caminho para conexão com o quiz
PROLOG_PATH = ["swipl", "-q", "-s", "quiz.pl", "-g"]

id_pergunta = 1
ids_nao_usados = [x for x in range(1,101)]
pontuacao = 0
ultima_resposta = None
botao_reiniciar = None

def executar_prolog(comando):
    # Tratamento de erro caso não seja possível executar
    try:
        resultado = subprocess.run(PROLOG_PATH + [comando], capture_output=True, text=True)
        return resultado.stdout.strip()
    except Exception as e:
        print(f"Não foi possível executar o prolog: {e}")
        return ""
    
def sortear_id():
    global ids_nao_usados
    if len(ids_nao_usados) == 0:
        return None
    novo_id = choice(ids_nao_usados)
    return novo_id
    
def mostrar_pergunta():
    global id_pergunta

    id_pergunta = sortear_id()
    if id_pergunta is None:
        encerra_quiz()
        return

    comando = f"exibe_pergunta({id_pergunta}), halt."
    resultado = executar_prolog(comando)
    
    canva.delete("pergunta") #apaga pergunta anterior se tiver

    comando = f"exibe_pergunta({id_pergunta}), halt."
    resultado = executar_prolog(comando)

    if not resultado or '[' not in resultado:
        mostrar_pergunta()
        return

    partes = resultado.split("\n")
    opcoes = partes[1].strip('[]').split(',')

    if len(partes) >= 2:
        canva.create_text(250, 150, text=partes[0], font=("Arial", 15), fill="white", width=480, anchor="center", tags="pergunta")
    
    letras = ['A', 'B', 'C', 'D']
    for i, btn in enumerate(botoes):
        if i < len(opcoes):
            texto = opcoes[i].strip().strip("'").strip('"')
            btn.config(
                text=f"{letras[i]} - {texto}",
                state=tk.NORMAL,
                command=lambda idx=i: verificar_resposta(idx)
            )

        else:
            btn.config(text=" ", state=tk.DISABLED)

def verificar_resposta(opcao):
    global pontuacao, id_pergunta

    resultado = executar_prolog(f"verifica_resposta({id_pergunta}, {opcao + 1}), halt.")
    for btn in botoes:
        btn.config(state="disabled")

    if resultado == "correto":
        pontuacao += 1
        piscar(botoes[opcao], "green")
    else:
        for i in range(4):    
            if executar_prolog(f"verifica_resposta({id_pergunta}, {i + 1}), halt.") == "correto":
                correta = i
                break
        piscar(botoes[opcao], "red")
        piscar(botoes[correta], "green")

    ids_nao_usados.remove(id_pergunta)
    root.after(1000, mostrar_pergunta)

def encerra_quiz():
    botao_acaba.config(state="disabled")
    canva.delete("pergunta")
    texto_final = f"Fim do Quiz!\nPontuação final: {pontuacao} pontos"
    canva.create_text(250, 150, text=texto_final, font=("Arial", 18), fill="white", width=480, anchor="center", tags="pergunta")
    for btn in botoes:
        btn.config(state="disabled",text="")
    
     # Mostra o botão de reinício
    canva.itemconfigure(reiniciar_btn_id, state="normal")  # Tornando o botão de reinício visível
    return

def reiniciar_quiz():
    global pontuacao, ids_nao_usados, id_pergunta
    # Resetar as variáveis
    pontuacao = 0
    id_pergunta = 1
    ids_nao_usados = [x for x in range(1,101)]
    canva.delete("pergunta")
    canva.itemconfigure(reiniciar_btn_id, state="hidden")
    botao_acaba.config(state="normal")
    mostrar_pergunta()  # Esconde o botão de reiniciar após o reinício


# Função responsável por implementar e tratar resposta do usuário
def piscar(botao, cor, callback=None, count=0):
    if count >= 4:
        if callback:
            callback()
        return
    nova = cor if (count % 2) == 0 else "lightgray"
    botao.config(bg=nova)
    root.after(150, lambda: piscar(botao, cor, callback, count+1))


#interface nova
root = tk.Tk()
root.title("Quiz Prolog")
root.geometry("500x400")
root.resizable(False, False)

#----------------------------------

frame_botao = tk.Frame(root, bg="gray", 
                       height=150, bd=2, 
                       highlightbackground="black", 
                       highlightthickness=2)
frame_botao.pack_propagate(False)
frame_botao.pack(side="bottom", fill="x")

#----------------------------------

bg_interface = tk.PhotoImage(file="fundo.png")


canva = tk.Canvas(root, width=500, height=400, highlightthickness=0)
canva.pack(fill="both", expand=True)
canva.create_image(0, 0, anchor="nw", image=bg_interface)

#----------------------------------
# Adiciona botão Encerrar no canto superior direito do canvas
botao_acaba = tk.Button(
    root, 
    text="Encerrar", 
    width=12, 
    height=1, 
    font=("Impact", 12), 
    bg="black", 
    fg="red", 
    command=encerra_quiz
)
canva.create_window(480, 20, window=botao_acaba, anchor="ne")

# Adiciona botão Reiniciar no canto superior esquerdo, inicialmente invisível
botao_reiniciar = tk.Button(
    root, 
    text="Reiniciar Quiz", 
    width=12, 
    height=1, 
    font=("Impact", 12), 
    bg="green", 
    fg="white", 
    command=reiniciar_quiz
)

# Inicialmente, o botão de reiniciar está escondido
reiniciar_btn_id = canva.create_window(20, 20, window=botao_reiniciar, anchor="nw")
canva.itemconfigure(reiniciar_btn_id, state="hidden")

# Implementa botões de opção no mesmo padrão
botoes = []
for i in range(4):
    btn = tk.Button(
        frame_botao,
        text="",
        width=20,
        height=2,
        font=("Arial", 12),
        bg="lightgray",
        
    )
    btn.grid(row=i // 2, column=i % 2, padx=20, pady=10)
    botoes.append(btn)

mostrar_pergunta()

root.mainloop()