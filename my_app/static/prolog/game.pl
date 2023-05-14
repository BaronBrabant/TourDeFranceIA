:- use_module(library(lists)).
:- dynamic(cyclist/5).

% position, lane, curveId, cyclistId, teamId

cyclist(4, 0, n, b1, 0).
cyclist(0, 0, n, b2, 0).
cyclist(3, 0, n, b3, 0).

cyclist(4, 0, n, n1, 1).
cyclist(0, 0, n, n2, 1).
cyclist(4, 0, n, n3, 1).

cyclist(0, 0, n, g1, 2).
cyclist(0, 0, n, g2, 2).
cyclist(3, 0, n, g3, 2).

cyclist(0, 0, n, i1, 3).
cyclist(0, 0, n, i2, 3).
cyclist(0, 0, n, i3, 3).




%positionCyclist(Position, Lane, CurveId, Cyclist) :- 
%    					positionCyclist(X, _, _, Cyc), 
%    					Position \= Position,
%    					Lane .


%movement().

incremented_list(Start, End, List) :-
    Start =< End,
    incremented_list_helper(Start, End, List).

incremented_list_helper(Start, End, [Start|Rest]) :-
    Start =< End,
    Next is Start + 1,
    incremented_list_helper(Next, End, Rest).

incremented_list_helper(Start, End, []) :-
    Start > End.

%works for iteratePosInbetween([1,2,3,4,5], Pos).
%iteratePosInbetween([]).
iteratePosInbetween([Head|Tail], Return):- checkCollision(Head), 
								   iteratePosInbetween(Tail, Return).
iteratePosInbetween([Head|_], Return) :- Return = Head.

checkCyclistInWay(InitialPosition, NewPosition, CollisionPos) :- 
    			FirstStep is InitialPosition + 1,
    			incremented_list(FirstStep, NewPosition, PosInBetween),
    			append(PosInBetween, [-1], ListToCheckPos),
                iteratePosInbetween(ListToCheckPos, CollisionPos).

checkCollision(OtherCyc) :- getPositionWidth(OtherCyc, Width),
                            Width == 3, 
                            !, \+((cyclist(OtherCyc, _, _,ID, _),
                            cyclist(OtherCyc,_ ,_ ,ID2, _), ID \= ID2, 
                            cyclist(OtherCyc, _,_,ID3, _), ID \= ID3, ID2\=ID3)).

checkCollision(OtherCyc) :- getPositionWidth(OtherCyc, Width),
                            Width == 2, 
                            !, \+((cyclist(OtherCyc, _, _,ID,_ ),
                            cyclist(OtherCyc,_ ,_,ID2,_), 
                            ID \= ID2)).

checkCollision(OtherCyc) :- getPositionWidth(OtherCyc, Width),
                            Width == 1,
                            !, \+(cyclist(OtherCyc, _ , _,_, _)).


nextMove(Position, _ , Movement, NewPos, Lane, CurveId) :-
	CheckWay is Position + Movement,
    checkCyclistInWay(Position, CheckWay, Return),
    Return == -1,
    NewPos is Position + Movement,
    \+(getPositionSplit(NewPos)), 
    \+(getPositionCurve(NewPos)),
    isFreeNormalLane(NewPos, Lane), CurveId = n.

nextMove(Position, LaneIn, Movement, NewPos, Lane, CurveId) :- 
    CheckWay is Position + Movement,
    checkCyclistInWay(Position, CheckWay, Return),
    Return == -1,
    NewPos is Position + Movement,
    getPositionSplit(NewPos), 
    getPositionCurve(NewPos),
    (getPositionSplit(Position), isFreeWidthSplitCurve(NewPos, LaneIn, CurveId, Lane) ; 
    \+(getPositionSplit(Position)), (LaneIn2 = 1 ; LaneIn2 = 2; LaneIn2 = 3), 
    isFreeWidthSplitCurve(NewPos, LaneIn2, CurveId, Lane)).


nextMove(Position, LaneIn, Movement, NewPos, Lane, CurveId) :- 
    CheckWay is Position + Movement,
    checkCyclistInWay(Position, CheckWay, Return),
    Return == -1,
    NewPos is Position + Movement,
    getPositionSplit(NewPos), 
    \+(getPositionCurve(NewPos)),
    (getPositionSplit(Position), isFreeWidthSplit(Position, NewPos, LaneIn, Lane), CurveId = n ; 
    \+(getPositionSplit(Position)), (LaneIn2 = 1 ; LaneIn2 = 2; LaneIn2 = 3), 
    isFreeWidthSplit(Position, NewPos, LaneIn2, Lane), CurveId = n).

nextMove(Position,_,  Movement, NewPos, Lane, CurveId) :- 
    CheckWay is Position + Movement,
    checkCyclistInWay(Position, CheckWay, Return),
    Return == -1,
    NewPos is Position + Movement,
    \+(getPositionSplit(NewPos)), 
    getPositionCurve(NewPos),
 	isFreeWidthCurve(NewPos, CurveId, Lane).
    							  
    							  
             

%check if position with newPos is valid, check if intial lane is free and if \+ redo with incremented
%lane

%isFreeWidth3

%(in, out)
isFreeNormalLane(NewPos, Lane) :- (positionLegal(NewPos, 1, n), \+(cyclist(NewPos, 1, n, _, _)), Lane = 1, !);
    						(positionLegal(NewPos, 2, n), \+(cyclist(NewPos, 2, n, _, _)), Lane = 2, !);
    						(positionLegal(NewPos, 3, n), \+(cyclist(NewPos, 3, n, _, _)), Lane = 3).
                        

    
    
getPositionSplit(Position):- 	(Position >= 23,
                               	Position =< 34);
    							(Position >= 84,
                                Position =< 94).

%(in, in, in, out)
isFreeWidthSplit(Position, NewPos, LaneIn, LaneOut):- 
    getPositionSplit(NewPos),
    getPositionWidth(Position, X), 
    ((X == 2, \+(cyclist(NewPos, LaneIn, n, _, _)), LaneOut = LaneIn);
    (X == 3, ((LaneIn == 3, \+(cyclist(NewPos, LaneIn, n , _, _)), LaneOut = LaneIn); 
    	(LaneIn \= 3, ((\+(cyclist(NewPos, 1, n,_)), LaneOut = 1) ; (\+(cyclist(NewPos, 2, n,_)), LaneOut = 2)))))).

%(in, out, out)
isFreeWidthCurve(NewPos, CurveId, Lane):- 
    (\+(cyclist(NewPos, 1, a, _, _)), CurveId = a, Lane = 1); 
    (\+(cyclist(NewPos, 2, c, _, _)), (\+(cyclist(NewPos, 2, b, _, _)), CurveId = b, Lane = 2); 
    	(\+(cyclist(NewPos, 2, c, _, _)), CurveId = c, Lane = 2)). 

%(in, in, out, out)
isFreeWidthSplitCurve2(NewPos, LaneIn, CurveId, LaneOut):-
    (LaneIn =:= 1, (\+(cyclist(NewPos, LaneIn, a, _, _)), LaneOut = LaneIn, CurveId = a)); 
    (LaneIn =:= 2, \+(cyclist(NewPos, LaneIn, c, _, _)), ((\+(cyclist(NewPos, LaneIn, b, _, _)), LaneOut = LaneIn, CurveId = b); 
    	(\+(cyclist(NewPos, LaneIn, c, _, _)), LaneOut = LaneIn, CurveId = c))).

%(in, in, out, out)
isFreeWidthSplitCurve3(NewPos, LaneIn, CurveId, LaneOut):-
    ((LaneIn == 1 ; LaneIn == 2), ((\+(cyclist(NewPos, 1, a, _, _)), LaneOut = 1, CurveId = a); 
    	(\+(cyclist(NewPos, 2, b, _, _)), LaneOut = 2, CurveId = b)));
    (LaneIn == 3, \+(cyclist(NewPos, 3, d, _, _)), ((\+(cyclist(NewPos, 3, c, _, _)), LaneOut = 3, CurveId = c); 
    	(\+(cyclist(NewPos, 3, d, _, _)), LaneOut = 3, CurveId = d))).
    									
%(in, in, out, out)
isFreeWidthSplitCurve(NewPos, LaneIn, CurveId, Lane):- 
    getPositionWidth(NewPos, Width),
    ((Width == 2, isFreeWidthSplitCurve2(NewPos, LaneIn, CurveId, Lane)); 
    (Width == 3, isFreeWidthSplitCurve3(NewPos, LaneIn, CurveId, Lane))).
                                

positionLegal(Position, Lane, CurveId) :- 
    					Position >= 1,
    					Position =< 105,
   			 			isLegalLane(Position, Lane, Width), 
    					((getPositionCurve(Position),
    					isLegalInsideCurve(Width, CurveId, Lane));
                        CurveId == n).
    			
isLegalLane(Position, Lane, Width):- getPositionWidth(Position, Width), 
    						Lane =< Width.

isLegalInsideCurve(Width, CurveID, Lane):- 
                         (Width =:= 2,((Lane =:= 1, CurveID =:= a);
                         (Lane =:= 2, member(CurveID, [b, c]))));
    					 (Width =:= 3, ((Lane =:= 1,CurveID =:= a);
                          (Lane =:= 2,CurveID =:= b);
    					  (Lane =:= 3,member(CurveID, [c, d])))).

getPositionWidth(Position, Width):- (((Position >= 1, Position =< 8);
                                  (Position >= 19, Position =< 36);
                                  (Position >= 95, Position =< 105)),
                                  Width = 3);
                                  ((Position >= 73, Position =< 75),
                                  Width = 1);
                                  (((Position >= 9, Position =< 18);
                                  (Position >= 36, Position =< 72);
                                  (Position >= 76, Position =< 94)),
                                  Width = 2).

getPositionCurve(Position) :-     (Position >= 9,
                                  Position =< 10);
    							  (Position >= 26,
                                  Position =< 27);
    							  (Position >= 63,
                                  Position =< 64);
    							  (Position >= 89,
                                  Position =< 890).


getLast(Team, Id) :-
    findall(Number-Id, cyclist(Number,_ ,_ , Id, Team), List),
    sort(List, SortedList),
    nth0(0, SortedList, _-Id).

getPosition(Id, Position, Lane) :- cyclist(Position, Lane, _, Id, _).


doesNotWork(A) :- \+(A).

doesMemWork(A, B) :- member(A, B).

doesEqWork(A, B) :- A == B.

testOr(A, B) :- (A ; write(B)).

testEmpty(A, _) :- write(A).


feedCard([DeckS|Deck], Return) :- 
				
%AllDecksFirst is a list of list containing all the decks which contain all their cards
shallow(AllDecksFirst, Depth, Bound, Best) :-
	

shallow_child(Card, Decks, BuiltSet, Depth, Bound, Best) :-
	length(Decks, Length),
    Length \= 0,
    %take first deck
    nth0(0, Decks, PlayerDeck),
    %Remove first deck from list 
    drop(0, Decks, NewDecks),
    %take first card from the selected deck
    nth0(0, PlayerDeck, NewCard),
    %remove card from selected deck
    drop(0, PlayerDeck, DeckRemoveFirst),
    %add the card to the list built as you go down the tree
    append(BuiltSet, [DeckRemoveFirst], NewBuiltSet),
    %call recursive function with the new card, new decks, new built set, depth, bound and best
    Depth2 is Depth + 1,
    shallow_child(NewCard, NewDecks, NewBuiltSet , Depth2, Bound, Best),
    %need to finish the logic here but ill do the end condition first
    shallow_child



shallow_child(Card, Decks, BuiltSet, Depth, Bound, Best) :-
	length(Decks, Length),
    %this means youre at the last terminal level and need to check the values
    Length == 0,
    buildSetTestBetter

    
buildSetTestBetter([Card|Leftover], BuiltSet, PassedValues, Return) :-
    append(BuiltSet, [Card], NewBuiltSet),
    %apply eval function to all values in 


    Return = BuiltSet.

