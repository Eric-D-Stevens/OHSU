

kb([has_tree(T,T)]).
kb([has_tree(T,n(N,LT,RT)), has_tree(T,LT)]).
kb([has_tree(T,n(N,LT,RT)), has_tree(T,RT)]).


 depthFirstProve([yes(X,Y),has_tree(n(X,l(l4),Y),n(n1,n(n2,l(l1),l(l2)),n(n3,l(l3),n(n4,l(l4),l(l5)))))]).


 neighbor(AnswerClause,NewAnswerClause) :-
 	[Yes,Head|Body] = AnswerClause,
	kb([Head|NewBody]),
	NewAnswerClause = [Yes,Head,NewBody].
