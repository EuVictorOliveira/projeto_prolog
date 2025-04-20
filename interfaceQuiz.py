import tkinter as tk
from tkinter import PhotoImage
from pyswip import Prolog
import random

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz com Prolog")
        self.root.geometry("800x600")
        self.root.configure(bg="red")

        # Conectar com Prolog
        self.perguntas = self.carregar_perguntas_prolog()
        random.shuffle(self.perguntas)

        # Fundo
        self.canvas = tk.Canvas(root, width=800, height=600, bg="red", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        try:
            self.bg = PhotoImage(file="imagemFundo.png")
            self.canvas.create_image(0, 0, anchor="nw", image=self.bg)
        except:
            print("Imagem não encontrada, fundo vermelho aplicado.")

        # Topo vermelho fixo
        self.canvas.create_rectangle(0, 0, 800, 80, fill="red", outline="red")

        self.pergunta_idx = 0
        self.pontuacao = 0

        self.frame_slide = tk.Frame(self.canvas, bg="red")
        self.frame_slide.place(x=800, y=100)  # Começa fora da tela para animar entrada

        self.label_pergunta = tk.Label(self.frame_slide, text="", font=("Arial", 20, "bold"),
                                       bg="red", fg="white", wraplength=700, justify="center")
        self.label_pergunta.pack(pady=10)

        self.botoes = []
        for i in range(4):
            btn = tk.Button(self.frame_slide, text="", font=("Arial", 14), width=30, height=2,
                            bg="white", fg="black", command=lambda i=i: self.verificar(i))
            btn.pack(pady=5)
            self.botoes.append(btn)

        self.animar_entrada()

    def carregar_perguntas_prolog(self):
        prolog = Prolog()
        prolog.consult("base_dados.pl")
        perguntas = []
        for p in prolog.query("pergunta(ID, P, L, R)"):
            perguntas.append({
                "pergunta": str(p["P"]),
                "opcoes": list(map(str, p["L"])),
                "resposta": str(p["R"])
            })
        return perguntas

    def animar_entrada(self):
        self.atualizar_pergunta()
        x = 800

        def slide():
            nonlocal x
            if x > 0:
                x -= 40
                self.frame_slide.place(x=x, y=100)
                self.root.after(10, slide)
            else:
                self.frame_slide.place(x=0, y=100)
        slide()

    def atualizar_pergunta(self):
        if self.pergunta_idx < len(self.perguntas):
            p = self.perguntas[self.pergunta_idx]
            self.label_pergunta.config(text=p["pergunta"])
            opcoes = p["opcoes"]
            random.shuffle(opcoes)
            for i in range(4):
                self.botoes[i].config(text=opcoes[i], bg="white", state="normal")
        else:
            self.label_pergunta.config(text=f"Fim do Quiz! Pontuação: {self.pontuacao}/{len(self.perguntas)}")
            for btn in self.botoes:
                btn.pack_forget()

    def verificar(self, i):
        resposta = self.botoes[i]["text"]
        correta = self.perguntas[self.pergunta_idx]["resposta"]

        for btn in self.botoes:
            btn.config(state="disabled")

        if resposta == correta:
            self.botoes[i].config(bg="green")
            self.pontuacao += 1
        else:
            self.botoes[i].config(bg="red")
            for btn in self.botoes:
                if btn["text"] == correta:
                    btn.config(bg="green")

        self.root.after(1500, self.proxima)

    def proxima(self):
        self.pergunta_idx += 1
        self.frame_slide.place(x=800, y=100)
        self.animar_entrada()

# Execução principal
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
