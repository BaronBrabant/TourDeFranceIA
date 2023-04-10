


%positionCyclist(Position, Lane, CurveId, Cyclist) :- 
%    					positionCyclist(X, _, _, Cyc), 
%    					Position \= Position,
%    					Lane .

positionLegal(Position, Lane, CurveId) :- 
    					Position >= 0,
    					Position =< 104,
   			 			legalLane(Position, Lane, Width), 
    					((positionCurve(Position),
    					positionInsideCurve(Position, Width, CurveId, Lane));
                        CurveId == "n").
    			


legalLane(Position, Lane, Width):- positionWidth(Position, Width), 
    						Lane =< Width.


positionWidth(Position, Width):- (((Position >= 0,
                                  Position =< 7);
                                  (Position >= 18,
                                  Position =< 35);
                                  (Position >= 94,
                                  Position =< 104)),
                                  Width = 3);
                                  ((Position >= 72,
                                   Position =< 74),
                                  Width = 1);
                                  Width = 2.

positionCurve(Position) :- 		  (Position >= 8,
                                  Position =< 9);
    							  (Position >= 25,
                                  Position =< 26);
    							  (Position >= 62,
                                  Position =< 63);
    							  (Position >= 88,
                                  Position =< 89).
    							  
positionInsideCurve(Width, CurveID, Lane):- 
                         (Width == 2,((
                         Lane == 1, 
                         CurveID == "a");
                         (Lane == 2,
                         member(CurveID, ["b", "c"]))
                         ));
    					 (Width == 3, ((
                          Lane == 1,
                          CurveID == "a");
                          (Lane == 2,
                          CurveID == "b");
    					  (Lane == 3,
                           member(CurveID, ["c", "d"]))
                          )).
    				



