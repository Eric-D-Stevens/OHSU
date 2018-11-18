disjunction([p(true)|_]).
disjunction([n(false)|_]).
disjunction([_|Rest]) :-
	disjunction(Rest).

conjunction([]).
conjunction([X|Rest]) :-
	conjunction(Rest),
	disjunction(X).
