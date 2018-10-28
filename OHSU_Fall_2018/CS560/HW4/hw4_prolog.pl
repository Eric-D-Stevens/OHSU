
% Question 2
succ(X,Y) :- Y is X+1.
pred(X,Y) :- Y is X-1.

% Question 3
plus(X,0,X).
plus(X,Y,Z) :-
	succ(X,NewX),
	pred(Y,NewY),
	plus(NewX,NewY,Z).


% Knowledge Base for questions 4, 5, and 6
%declare blocks
block(red1).
block(red2).
block(red3).
block(red4).
block(red5).
block(red6).
block(red7).
block(gre1).
block(gre2).
block(gre3).
block(blu1).
block(blu2).
block(yel1).
block(bla1).
% set block colors
color(red1,red).
color(red2,red).
color(red3,red).
color(red4,red).
color(red5,red).
color(red6,red).
color(red7,red).
color(gre1,green).
color(gre2,green).
color(gre3,green).
color(blu1,blue).
color(blu2,blue).
color(yel1,yellow).
color(bla1,black).

% Question 4
multicolortower4(1,[X]) :- block(X).
multicolortower4(Height,[Top|Rest]) :-
	Height > 1,
	block(Top),
	NewHeight is Height-1,
	multicolortower4(NewHeight,Rest).


% Question 5
differentFromList(Block,[]) :- block(Block).
differentFromList(Block,[Top|Rest]) :-
	block(Block),
	not(Block = Top),
	differentFromList(Block,Rest).

mct5(0,List,Out) :- 
	Out = List.
mct5(Height,List,Out) :-
	Height > 0,
	Height < 14,
	block(Top),
	differentFromList(Top,List),
	NewHeight is Height-1,
	mct5(NewHeight,[Top|List],Out).

multicolortower5(Height,List) :-
	mct5(Height,_,List).




% Question 6
differentcolor(X,Y) :-
	block(X),
	block(Y),
	color(X,CX),
	color(Y,CY),
	not(CX=CY).


mct6(1,List,Out) :- 
	Out = List.
mct6(Height,[Tl|List],Out) :-
	Height > 1,
	Height < 14,
	block(Top),
	differentFromList(Top,List),
	differentcolor(Top,Tl),
	NewHeight is Height-1,
	mct6(NewHeight,[Top|[Tl|List]],Out).

multicolortower6(Height,List) :-
	mct6(Height,_,List).

















