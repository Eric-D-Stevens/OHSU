
/*Knowedge Base*/
node(1). node(2). node(3). node(4). node(5). node(6).
node(7). node(8). node(9). node(10). node(11). node(12).
node(13). node(14). node(15).
c(1,2). c(1,3). c(1,5). c(1,7). c(1,8). c(1,11).
c(2,4). c(2,8). c(2,12). c(3,5). c(3,7). c(3,11).
c(4,6). c(5,7). c(5,11). c(6,8). c(7,11). c(8,11).
c(9,12). c(10,12). c(13,14). c(13,15). c(14,15).


/*Makes sure c(Node,Element) exists for every element in list*/
connected(Node, [X]) :-
	c(Node,X).
connected(Node,[First|Rest]) :-
	c(Node,First),
	connected(Node,Rest).

/*Ensures that Node does not exist in list*/
not_member(Node,[X]) :-
	not(Node=X).
not_member(Node,[Top|Rest]) :-
	not(Node=Top),
	not_member(Node,Rest).

/*Builds clique of size N from knowledge base as list*/
clique(1,[X]) :-
	getnode(X).
clique(N, [Top|List]) :-
	N >1,
	Nminus is N-1,
	clique(Nminus,List),
	getnode(Top),
	not_member(Top,List),
	connected(Top,List).


/*Provided functions for counting node calls*/
countclique(N,Result) :-
	retractall(cnt(_)),
	assert(cnt(0)),
	clique(N,Result).

countclique(_,_) :-
	cnt(N),
	print(N).

getnode(Node) :-
	node(Node),
	retract(cnt(Cnt)),
	Cnt1 is Cnt + 1,
	assert(cnt(Cnt1)).
	

