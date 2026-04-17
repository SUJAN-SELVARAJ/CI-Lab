:- use_module(library(apply)).
:- initialization(main).
main :-
    write('Enter operation (+, -, *, /, mod, **, square): '),
    read(Op),
    (
        Op == square ->
            write('Enter a number: '),
            read(X),
            R is X * X,
            write('Result: '), write(R), nl
    ;
        write('How many numbers? '),
        read(N),
        read_numbers(N, List),
        calculate(Op, List, R),
        write('Result: '), write(R), nl
    ).
read_numbers(0, []).
read_numbers(N, [X|T]) :-
    N > 0,
    write('Enter number: '),
    read(X),
    N1 is N - 1,
    read_numbers(N1, T).
calculate(+,   [H|T], R) :- foldl(add, T, H, R).
calculate(-,   [H|T], R) :- foldl(sub, T, H, R).
calculate(*,   [H|T], R) :- foldl(mul, T, H, R).
calculate(/,   [H|T], R) :- foldl(div, T, H, R).
calculate(mod, [H|T], R) :- foldl(mod_op, T, H, R).
calculate(**,  [H|T], R) :- foldl(pow, T, H, R).
add(X,A,B) :- B is A + X.
sub(X,A,B) :- B is A - X.
mul(X,A,B) :- B is A * X.
div(X,A,B) :- B is A / X.
mod_op(X,A,B) :- B is A mod X.
pow(X,A,B) :- B is A ** X.

