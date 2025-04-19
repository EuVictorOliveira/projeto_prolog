:- encoding(utf8).
:- consult('base_dados.pl').

iniciar_quiz :-
    writeln('Bem-vindo ao Quiz!'),
    writeln('Digite 0 a qualquer momento para encerrar o quiz.'),
    jogar(1, 0).

jogar(ID, Pontuacao) :-
    pergunta(ID, Pergunta, Opcoes, RespostaCorreta),
    writeln(''),
    format('Pergunta ~w: ~w~n', [ID, Pergunta]),
    exibir_opcoes(Opcoes, 1),
    write('Digite sua resposta seguida de "."(1 a 4, ou 0 para sair): '),
    read(Escolha),
    (
        Escolha == 0 ->
            writeln('\nQuiz encerrado!!!.'),
            mostrar_pontuacao_final(Pontuacao)
        ;
        integer(Escolha),
        Escolha >= 1,
        Escolha =< 4 ->
            Index is Escolha - 1,  % Ajusta para índice 0 baseado no número digitado
            nth0(Index, Opcoes, RespostaEscolhida),
            verificar_resposta(RespostaEscolhida, RespostaCorreta, GanhaPonto),
            NovoPontos is Pontuacao + GanhaPonto,
            ID1 is ID + 1,
            jogar(ID1, NovoPontos)
        ;
            writeln('Opção inválida. Tente novamente.'),
            jogar(ID, Pontuacao)
    ).

% Fim do quiz (sem mais perguntas)
jogar(_, Pontuacao) :-
    writeln('\nFim das perguntas!'),
    mostrar_pontuacao_final(Pontuacao).

mostrar_pontuacao_final(Pontos) :-
    format('Sua pontuação final foi: ~w~n', [Pontos]).

exibir_opcoes([], _).
exibir_opcoes([H|T], N) :-
    format('~w - ~w~n', [N, H]),
    N1 is N + 1,
    exibir_opcoes(T, N1).

verificar_resposta(Escolhida, Correta, 1) :-
    Escolhida == Correta,
    writeln('Correto!'),
    !.

verificar_resposta(_, _, 0) :-
    writeln('Errado!').

