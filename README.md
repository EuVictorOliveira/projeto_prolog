# Quiz Interativo em Prolog com Interface Gráfica em Python

Este projeto é um sistema de quiz de perguntas e respostas de múltipla escolha, onde a **lógica de controle** é desenvolvida em **Prolog** e a **interface gráfica** é feita com **Python** usando `Tkinter`. A interação entre os python e prolog acontece via `subprocess`, permitindo que a interface chame predicados do Prolog em tempo real.

---

## Arquivos do Projeto

| Arquivo              | Descrição |
|----------------------|-----------|
| `interfaceQuiz.py`   | Interface gráfica em Python. Gerencia a exibição, respostas, pontuação e reinício. |
| `quiz.pl`            | Lógica principal em Prolog. Define predicados para exibir perguntas e verificar respostas. |
| `base_dados.pl`      | Base de dados contendo 100 perguntas no formato Prolog. Cada pergunta tem 4 alternativas e uma resposta correta. |

---

## Tecnologias e Ferramentas Utilizadas

- **Python 3+**
- **SWI-Prolog** (9+ recomendado)

---

## Funcionamento do quiz

1. A interface chama o predicado `exibe_pergunta(ID)` para mostrar uma pergunta aleatória com suas opções.
2. O usuário seleciona uma opção (1 a 4), que é mapeada internamente para o índice da lista de opções.
3. O predicado `verifica_resposta(ID, Escolha)` é chamado para verificar se a resposta está correta.
4. A interface exibe o resultado (`Correto!` ou `Errado!`) e avança para a próxima pergunta.
5. Ao fim das 100 perguntas, ou ao clicar em "Finalizar Quiz", o resultado final é exibido.
6. Um botão de "Reiniciar Quiz" permite jogar novamente.

---

## Pré-requisitos

###  Python
- Instale o Python 3+ a partir do [site oficial](https://www.python.org/downloads/)
- Verifique no terminal:
  ```bash
  python --version
  ```

### SWI-Prolog
- Instale a versão mais recente a partir de [swi-prolog.org](https://www.swi-prolog.org/Download.html)
- Após a instalação, certifique-se de que o comando `swipl` funciona no terminal:
  ```bash
  swipl --version
  ```

> **Importante:** Os arquivos `.pl` devem estar na mesma pasta do script Python para que o `subprocess` funcione corretamente.

---

## Executando o Quiz

1. **Clone ou baixe o projeto:**

   ```bash
   git clone https://github.com/EuVictorOliveira/projeto_prolog
   cd quiz-prolog-python
   ```

2. **Execute o script Python:**

   ```bash
   python interfaceQuiz.py
   ```

3. A interface do quiz será aberta. Responda cada pergunta clicando em uma das quatro alternativas.

---

## Exemplo de Questão da Base

```prolog
% Estrutura: pergunta(ID, Texto, [OpçãoA, OpçãoB, OpçãoC, OpçãoD], RespostaCorreta).
pergunta(1, 'Qual é a capital da França?', ['Paris', 'Londres', 'Roma', 'Berlim'], 'Paris').
```

Ao chamar:

```prolog
exibe_pergunta(1).
```

A saída será:

```
Qual é a capital da França?
['Paris','Londres','Roma','Berlim']
```

---

## Contribuidores

- [João Victor Oliveira](https://github.com/joaosilva)
- [Kevin Gabriel Morais Mangueira](https://github.com/Melvin2781)
- [Victor Gabriel da Silva Menezes](https://github.com/Vitin0N)

