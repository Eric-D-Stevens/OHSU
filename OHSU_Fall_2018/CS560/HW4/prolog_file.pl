

/*****    QUESTION 0   *****/

% positive numbers
%s(X) :- is X+1.
/*how do you define s() in prolog*/



/*****    QUESTION 1  *****/

% HOW DO YOU DO THIS? I DONT KNWO HOW TO DO S()


/*****    QUESTION 2  *****/
%successor
succ(X,Y) :- 
   	Y is(X+1).
/*guessing that this is not the proper way to do 
* this because it would make the entire homework 
* much easier. Need s() to be able to do it 
* properly.*/

%predecessor
pred(X,Y) :-
	Y is (X-1).
/*same situation as above.*/



/*****    QUESTION 3  *****/
%plus
plus(X,0,X).
plus(X,Y,Z) :-
	succ(X,newX),
	pred(Y,newY),
	plus(newX,newY,Z).
/*
* am i allowed to use pred in here. If so make 
* sure that I am doing pred properly, otherwise 
* how do you make this without pred.
*/


myPlus(X,Y,Z) :- Z is X+Y.



% BLOCKS
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



/*****    QUESTION 4  *****/
mct(1,[X]) :- block(X).
mct(Height,[Head|Tail]) :- 
	Height > 1,
	block(Head),
	pred(Height,NewHeight),
	write(NewHeight),
	write('  '),
	write(Tail),
	write('\n'),
	mct(NewHeight, Tail).
/* dont understand need for upsidown ? or how 
* to make it. This seems to stop execution fine 
* as long as inital height is greater than 1. */


/*****    QUESTION 5   *****/
differentFromList(_, []).
differentFromList(Block, [Top|Rest]) :-
	block(Top),
	not(member(Top,Rest)),
	differentFromList(Block,Rest).

multicolortower2(1,[X]) :- block(X).
multicolortower2(Height,[Head|Tail]) :- 
	write(' 1 in '),
	not(Height is 1),
	write(' 2 '),
	block(Head),
	write(' 3 '),
	bl(Head,Tail),
	write(' 4 '),
	pred(Height,NewHeight),
	write(NewHeight),
	write('  '),
	write(Tail),
	write('\n'),
	multicolortower2(NewHeight, Tail).
/* is it ok to use the = sign in the check
*  between for repeats */



/*****    QUESTION 6   *****/
%bl(B,[]) :- block(B).
%bl(B,[T|L]) :- 
%	block(B),
%	block(T),
%	not(member(B,[T|L])).


bl(_,[]).
bl(B,[Top|Rest]) :-
	not(Top = B),
	bl(B,Rest).

mt(0,List,Out) :- 
	Out = List.
mt(Height,List,Out) :-
	Height > 0,
	Height < 14,
	block(Top),
	bl(Top,List),
	NewHeight is Height-1,
	mt(NewHeight, [Top|List],Out).

