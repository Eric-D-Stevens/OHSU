shorter([],_).
shorter([_|B],[_|J]) :-
    shorter(B,J).

remove(E,[E|Y], Y).
remove(E,[A|B],[A|C]) :-
    remove(E,B,C).
       
s(X) = X+1.
