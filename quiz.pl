% Ajuste para permitir caracteres especiais.
:- encoding(utf8).

% Consulta à base de dados contendo as perguntas.
:- consult('base_dados.pl').

% Função responsável por exibir a pergunta da base de dados
exibe_pergunta(ID) :-
    pergunta(ID, Pergunta, Opcoes, _),
    write(Pergunta), nl,
    write(Opcoes), nl.

% Função responsável por verificar a validade\invalidade das resposta
verifica_resposta(ID, Escolha) :-
    pergunta(ID, _, Opcoes, RespostaCorreta),
    nth1(Escolha, Opcoes, OpcaoSelecionada),
    (OpcaoSelecionada == RespostaCorreta -> write('correto') ; write('errado')).
