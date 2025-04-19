import subprocess
import tkinter as tk

# Define o caminho para conexão com o quiz
PROLOG_PATH = ["swipl", "-q", "-s", "quiz.pl", "-g"]

id_pergunta = 1
pontuacao = 0
ultima_resposta = None
botao_reiniciar = None

# Função definida para tentar executar o prolog
def executar_prolog(comando):
    # Tratamento de erro caso não seja possível executar
    try:
        resultado = subprocess.run(PROLOG_PATH + [comando], capture_output=True, text=True)
        return resultado.stdout.strip()
    except Exception as e:
        print(f"Não foi possível executar o prolog: {e}")
        return ""

# Função para mostrar perguntas
def carregar_pergunta():
    global id_pergunta, pergunta_label, botoes_opcao, ultima_resposta

    # chama a função exibe pergunta de quiz.pl
    resultado = executar_prolog(f"exibe_pergunta({id_pergunta}), halt.")
    if not resultado or '[' not in resultado:
        finalizar_quiz()
        return

    linhas = resultado.split('\n')
    pergunta = linhas[0]
    opcoes = linhas[1].strip('[]').split(',')

    pergunta_label.config(text=f"{pergunta.strip()}")
    for i, btn in enumerate(botoes_opcao):
        if i < len(opcoes):
            texto = opcoes[i].strip().strip("'").strip('"')
            btn.config(text=f"{i+1} - {texto}", state=tk.NORMAL, command=lambda idx=i+1: responder(idx))
        else:
            btn.config(text=" ", state=tk.DISABLED)

# Função responsável por implementar e tratar resposta do usuário
def responder(opcao):
    global id_pergunta, pontuacao, resultado_label

    # Chama função de verificação de resposta do prolog
    resultado = executar_prolog(f"verifica_resposta({id_pergunta}, {opcao}), halt.")
    if resultado == "correto":
        pontuacao += 1
        resultado_label.config(text="Correto!")
    else:
        resultado_label.config(text="Errado!")

    id_pergunta += 1
    root.after(1000, carregar_pergunta)

# Função de finalização do quiz.
def finalizar_quiz(manual=False):
    if manual:
        pergunta_label.config(text="Quiz encerrado!!!")
    else:
        pergunta_label.config(text="Fim do quiz!!!")

    for btn in botoes_opcao:
        btn.config(state=tk.DISABLED)

    botao_finalizar.config(state=tk.DISABLED)
    resultado_label.config(text=f"Sua pontuação foi: {pontuacao}")
    botao_reiniciar.pack(pady=10)

# Função que permite que o usuário reinicie o quiz
def reiniciar_quiz():
    global id_pergunta, pontuacao
    id_pergunta = 1
    pontuacao = 0
    resultado_label.config(text="")
    for btn in botoes_opcao:
        btn.config(state=tk.NORMAL)
    botao_finalizar.config(state=tk.NORMAL)
    botao_reiniciar.pack_forget()
    carregar_pergunta()

# Início da interface
root = tk.Tk()
root.title("Quiz em Prolog")

# Configuração do padrão das perguntas, qualquer alteração nesse sentido deve ser realizad aqui
pergunta_label = tk.Label(root, text="", font=("Comic Sans MS", 14), wraplength=400, justify="center")
pergunta_label.pack(pady=10)

# Implementa botões de opção no mesmo padrão
botoes_opcao = []
for _ in range(4):
    btn = tk.Button(root, text="", width=40, font=("Comic Sans MS", 12))
    btn.pack(pady=2)
    botoes_opcao.append(btn)

# Botão para finalizar o quiz manualmente
botao_finalizar = tk.Button(
    root,
    text="Finalizar Quiz",
    font=("Comic Sans MS", 12),
    bg="red",
    fg="white",
    command=lambda: finalizar_quiz(manual=True)
)
botao_finalizar.pack(pady=10)

resultado_label = tk.Label(root, text="", font=("Comic Sans MS", 12))
resultado_label.pack(pady=10)

# Botão de reiniciar
botao_reiniciar = tk.Button(
    root,
    text="Reiniciar Quiz",
    font=("Comic Sans MS", 12),
    bg="blue",
    fg="white",
    command=reiniciar_quiz
)

carregar_pergunta()
root.mainloop()