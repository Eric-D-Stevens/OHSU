/**********************************
* Eric Stevens
* CS 560: Homework 5(b)
* PL: Conversion to CNF
**********************************/

step1(impliedby(impliedby(A,B),impliedby(C,D)),TopOutput) :-
	!,
	%write("made double implied\n"),
	step1(impliedby(A,B),OutputAB),
	step1(impliedby(C,D),OutputCD),
	TopOutput = or(OutputAB,not(OutputCD)).

step1(impliedby(X,impliedby(Y,Z)),Output) :- 
	!,
	%write("made iRight\n"),
	step1(impliedby(Y,Z), Output2),
	Output = or(X,not(Output2)).

step1(impliedby(impliedby(X,Y),Z),Output) :-
	!,
	%write("made iLeft\n"),
	step1(impliedby(X,Y),Output2),
	Output = or(Output2,not(Z)).

step1(impliedby(X,Y),Output) :-
	!,
	%write("made iSingel\n"),
	Output = or(X,not(Y)).

step1(and(X,Y),TopOutput) :-
	!,
	%write("made AND\n"),
	step1(X,OutputX),
	step1(Y,OutputY),
	TopOutput = and(OutputX,OutputY).

step1(or(X,Y),TopOutput) :-
	!,
	%write("made OR\n"),
	step1(X,OutputX),
	step1(Y,OutputY),
	TopOutput = or(OutputX,OutputY).

step1(not(X),TopOutput) :-
	!,
	%write("made NOT\n"),
	step1(X,OutputX),
	TopOutput = not(OutputX).

step1(X,Output) :-
	%write("made Generalized\n"),
	Output = X.

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
