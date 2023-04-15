:- include('gameData.pl').

%positionCyclist(Position, Lane, CurveId, Cyclist) :- 
%    					positionCyclist(X, _, _, Cyc), 
%    					Position \= Position,
%    					Lane .


%movement().


nextMove(Position, _ , Movement, NewPos, Lane, CurveId) :- 
    NewPos is Position + Movement,
    not(getPositionSplit(NewPos)), 
    not(getPositionCurve(NewPos)),
    isFreeNormalLane(NewPos, Lane), CurveId = n.

nextMove(Position, LaneIn, Movement, NewPos, Lane, CurveId) :- 
    NewPos is Position + Movement,
    getPositionSplit(NewPos), 
    getPositionCurve(NewPos),
    (getPositionSplit(Position), isFreeWidthSplitCurve(NewPos, LaneIn, CurveId, Lane) ; 
    not(getPositionSplit(Position)), (LaneIn2 = 1 ; LaneIn2 = 2; LaneIn2 = 3), 
    isFreeWidthSplitCurve(NewPos, LaneIn2, CurveId, Lane)).


nextMove(Position, LaneIn, Movement, NewPos, Lane, CurveId) :- 
    NewPos is Position + Movement,
    getPositionSplit(NewPos), 
    not(getPositionCurve(NewPos)),
    (getPositionSplit(Position), isFreeWidthSplit(Position, NewPos, LaneIn, Lane), CurveId = n ; 
    not(getPositionSplit(Position)), (LaneIn2 = 1 ; LaneIn2 = 2; LaneIn2 = 3), 
    isFreeWidthSplit(Position, NewPos, LaneIn2, Lane), CurveId = n).

nextMove(Position,_,  Movement, NewPos, Lane, CurveId) :- 
    NewPos is Position + Movement,
    not(getPositionSplit(NewPos)), 
    getPositionCurve(NewPos),
 	isFreeWidthCurve(NewPos, CurveId, Lane).
    							  
    							  
             

%check if position with newPos is valid, check if intial lane is free and if not redo with incremented
%lane

%isFreeWidth3

%(in, out)
isFreeNormalLane(NewPos, Lane) :- (positionLegal(NewPos, 1, n), not(cyclist(NewPos, 1, n, _)), Lane = 1, !);
    						(positionLegal(NewPos, 2, n), not(cyclist(NewPos, 2, n, _)), Lane = 2, !);
    						(positionLegal(NewPos, 3, n), not(cyclist(NewPos, 3, n, _)), Lane = 3).
                        

    
    
getPositionSplit(Position):- 	(Position >= 22,
                               	Position =< 33);
    							(Position >= 83,
                                Position =< 93).

%(in, in, in, out)
isFreeWidthSplit(Position, NewPos, LaneIn, LaneOut):- 
    getPositionSplit(NewPos),
    getPositionWidth(Position, X), 
    ((X == 2, not(cyclist(NewPos, LaneIn, n, _)), LaneOut = LaneIn);
    (X == 3, ((LaneIn == 3, not(cyclist(NewPos, LaneIn, n , _)), LaneOut = LaneIn); 
    	(LaneIn \= 3, ((not(cyclist(NewPos, 1, n,_)), LaneOut = 1) ; (not(cyclist(NewPos, 2, n,_)), LaneOut = 2)))))).

%(in, out, out)
isFreeWidthCurve(NewPos, CurveId, Lane):- 
    (not(cyclist(NewPos, 1, a, _)), CurveId = a, Lane = 1); 
    (not(cyclist(NewPos, 2, c, _)), (not(cyclist(NewPos, 2, b, _)), CurveId = b, Lane = 2); 
    	(not(cyclist(NewPos, 2, c, _)), CurveId = c, Lane = 2)). 

%(in, in, out, out)
isFreeWidthSplitCurve2(NewPos, LaneIn, CurveId, LaneOut):-
    (LaneIn == 1, (not(cyclist(NewPos, LaneIn, a, _)), LaneOut = LaneIn, CurveId = a)); 
    (LaneIn == 2, not(cyclist(NewPos, LaneIn, c, _)), ((not(cyclist(NewPos, LaneIn, b, _)), LaneOut = LaneIn, CurveId = b); 
    	(not(cyclist(NewPos, LaneIn, c, _)), LaneOut = LaneIn, CurveId = c))).

%(in, in, out, out)
isFreeWidthSplitCurve3(NewPos, LaneIn, CurveId, LaneOut):-
    ((LaneIn == 1 ; LaneIn == 2), ((not(cyclist(NewPos, 1, a, _)), LaneOut = 1, CurveId = a); 
    	(not(cyclist(NewPos, 2, b, _)), LaneOut = 2, CurveId = b)));
    (LaneIn == 3, not(cyclist(NewPos, 3, d, _)), ((not(cyclist(NewPos, 3, c, _)), LaneOut = 3, CurveId = c); 
    	(not(cyclist(NewPos, 3, d, _)), LaneOut = 3, CurveId = d))).
    									
%(in, in, out, out)
isFreeWidthSplitCurve(NewPos, LaneIn, CurveId, Lane):- 
    getPositionWidth(NewPos, Width),
    ((Width == 2, isFreeWidthSplitCurve2(NewPos, LaneIn, CurveId, Lane)); 
    (Width == 3, isFreeWidthSplitCurve3(NewPos, LaneIn, CurveId, Lane))).
                                

positionLegal(Position, Lane, CurveId) :- 
    					Position >= 0,
    					Position =< 104,
   			 			isLegalLane(Position, Lane, Width), 
    					((getPositionCurve(Position),
    					isLegalInsideCurve(Width, CurveId, Lane));
                        CurveId == n).
    			
isLegalLane(Position, Lane, Width):- getPositionWidth(Position, Width), 
    						Lane =< Width.

isLegalInsideCurve(Width, CurveID, Lane):- 
                         (Width == 2,((
                         Lane == 1, 
                         CurveID == a);
                         (Lane == 2,
                         member(CurveID, [b, c]))
                         ));
    					 (Width == 3, ((
                          Lane == 1,
                          CurveID == a);
                          (Lane == 2,
                          CurveID == b);
    					  (Lane == 3,
                           member(CurveID, [c, d]))
                          )).

getPositionWidth(Position, Width):- (((Position >= 0, Position =< 7);
                                  (Position >= 18, Position =< 35);
                                  (Position >= 94, Position =< 104)),
                                  Width = 3);
                                  ((Position >= 72, Position =< 74),
                                  Width = 1);
                                  (((Position >= 8, Position =< 17);
                                  (Position >= 35, Position =< 71);
                                  (Position >= 75, Position =< 93)),
                                  Width = 2).

getPositionCurve(Position) :-     (Position >= 8,
                                  Position =< 9);
    							  (Position >= 25,
                                  Position =< 26);
    							  (Position >= 62,
                                  Position =< 63);
    							  (Position >= 88,
                                  Position =< 89).
