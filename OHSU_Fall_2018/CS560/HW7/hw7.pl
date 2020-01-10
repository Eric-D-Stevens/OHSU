step1(and(X,Y),and(NewX,NewY)) :-
	!,
	step1(X,NewX),
	step1(Y,NewY).

step1(or(X,Y),or(NewX,NewY)) :-
	!,
	step1(X,NewX),
	step1(Y,NewY).

step1(not(X),not(NewX)) :-
	!,
	step1(X,NewX).

step1(impliedby(X,Y),New) :-
	!,
	step1(X,NewX),
	step1(Y,NewY),
	New = or(NewX,not(NewY)).

step1(X,X).


test1 :-
        findall(X,step1(impliedby(d,e),X),L1),
        write(L1),nl,
        findall(X,step1(impliedby(d,not(e)),X),L2),
        write(L2),nl,
        findall(X,step1(impliedby(d,impliedby(e,f)),X),L3),
        write(L3),nl,
        findall(X,step1(impliedby(impliedby(a,b),impliedby(e,f)),X),L4),
        write(L4),nl,
        findall(X,step1(and(a,(or(b,or(c,(not(impliedby(d,e))))))),X),L5),
        write(L5),nl.


/**
RESULTS:

?- test1.
[or(d,not(e))]
[or(d,not(not(e)))]
[or(d,not(or(e,not(f))))]
[or(or(a,not(b)),not(or(e,not(f))))]
[and(a,or(b,or(c,not(or(d,not(e))))))]
true.
**/


step2(not(not(X)),NewX) :-
	!,
	step2(X,NewX).

step2(not(or(X,Y)),and(NewX,NewY)) :-
	!,
	step2(not(X),NewX),
	step2(not(Y),NewY).

step2(not(and(X,Y)),or(NewX,NewY)) :-
	!,
	step2(not(X),NewX),
	step2(not(Y),NewY).	

step2(not(X),not(NewX)) :-
	!,
	step2(X,NewX).

step2(or(X,Y),or(NewX,NewY)) :-
	!,
	step2(X,NewX),
	step2(Y,NewY).

step2(and(X,Y),and(NewX,NewY)) :-
	!,
	step2(X,NewX),
	step2(Y,NewY).

step2(X,X).



test2 :-
        findall(X,step2(or(d,not(e)),X),L1),
        write(L1),nl,
        findall(X,step2(or(d,not(not(e))),X),L2),
        write(L2),nl,
        findall(X,step2(or(d,not(or(e,not(f)))),X),L3),
        write(L3),nl,
        findall(X,step2(or(or(a,not(b)),not(or(e,not(f)))),X),L4),
        write(L4),nl,
        findall(X,step2(and(a,or(b,or(c,not(or(d,not(e)))))),X),L5),
        write(L5),nl.


/**
RESULTS:

?- test2.
[or(d,not(e))]
[or(d,e)]
[or(d,and(not(e),f))]
[or(or(a,not(b)),and(not(e),f))]
[and(a,or(b,or(c,and(not(d),e))))]
true.
**/


