initial([block(a),block(b),block(c),table(t),on(a,b),on(b,c),on(c,t),empty,clear(a)]).
goal([on(c,b),on(b,a),on(a,t)]).

action(pickup(A,B),
       [block(A),clear(A),block(B),on(A,B),empty],
       [holding(A),clear(B)],
       [empty,on(A,B),clear(A)]).
action(pickup(A,B),
       [block(A),clear(A),table(B),on(A,B),empty],
       [holding(A)],
       [empty,on(A,B),clear(A)]).
action(putdown(A,B),
       [holding(A),block(B),clear(B)],
       [on(A,B),clear(A),empty],
       [clear(B),holding(A)]).
action(putdown(A,B),
       [holding(A),table(B)],
       [on(A,B),clear(A),empty],
       [holding(A)]).


subset([],_). 
subset([Sub_head|Sub_rest],Set) :-
	member(Sub_head,Set),
	subset(Sub_rest,Set).
	

remove(Sub,Set,Rest) :-
	subset(Sub,Set),	
	subtract(Set, Sub, Rest).

neighbor([Plan,World],[[NewPlan],NewWorld]) :-
	action(NextAction,Pre,Add,Del),
	subset(Pre,World),
	remove(Del,World,NewWorldMinus),
	append(NewWorldMinus,Add,NewWorld),
	append(Plan,NextAction,NewPlan).


plan([[CurrentPlan,CurrentWorld]|_]) :-
	goal(Goal),
	subset(Goal,CurrentWorld),
	write("\n Goal: "),
	write(Goal),
	write("\n CurrentWorld: "),
	write(CurrentWorld),
	write("\n CurrentPlan: "),
	write(CurrentPlan),
	!. % this cut will prevent infinite combos

plan([First|Frontier]) :-
	findall(New,neighbor(First,New),Neighbors),
	append(Frontier,Neighbors, Temp),
	plan(Temp).


test() :-
	initial(Initial),
	plan([[[],Initial]]).
	




