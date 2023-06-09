
const axios = require('axios');

const hostname = '127.0.0.1';
const port = 3000;

var bodyParser = require('body-parser');

var jsonParser = bodyParser.json();
var urlencodedParser = bodyParser.urlencoded({ extended: false });

const cors = require('cors');

const express = require('express');
const app = express();

app.use(cors({
    methods: ['GET','POST','DELETE','UPDATE','PUT','PATCH'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    origin: 'http://127.0.0.1:5000'
}));

//global variables
var idGlobale = "";
var posLaneSave = [];


const http = require('http');
const https = require('https');

const pl = require('tau-prolog');
require("tau-prolog/modules/lists.js")(pl);
var session = pl.create();


//axios.post('http://127.0.0.1:5000/', {
//    testData: 'hello world'
//  })




/*
const server = http.createServer((req, res) => {
    
    
    res.statusCode = 200;

    res.setHeader('Content-Type', 'text/plain');

    session.consult("../prolog/test.pl", {
            success: function() {console.log("ok") },
            error: function(err) { console.log(err) }
        });

    session.query("likes(sam, X).", {  
        success: function(goal) {console.log(goal)},
        error: function(err) {  }
    });
    res.end('Hello World');

    session.answer({
        success: function(answer) {
            console.log(session.format_answer(answer)); // X = salad ;
            ;
        },
        fail: function() { },
        error: function(err) {  },
        limit: function() { }
    });
    
});
*/

app.post('/API/test',jsonParser, cors(),  function(req, res) {
    //console.log(res);
    //console.log(res);
    var body = req.body;
    
    console.log(body);

    pos = getPosition(getLast(body.team));

    //"nextMove(1,1,4, NewPos, NewLane, NewCurveId).";
    var call = "nextMove(" + pos[0] + "," + pos[1] + "," + body.card + ", NewPos, NewLane, NewCurveId).";
    var positionCheck = "getPositionWidth(68, X).";
    var checkNot = "doesNotWork(false)."
    var testMember = "doesMemWork(a, [a,b,c]).";
    var testEqAndMem = "isLegalInsideCurve(2, c, 2).";
    var testEq = "doesEqWork(1, 1).";
    var testOr = "testOr(true, 2).";
    // /isLegalLane(Position, Lane, Width)
    var testLegalLane = "isLegalLane(1, 1, 3).";
    //positionLegal(Position, Lane, CurveId)
    var testLegalPos = "positionLegal(1, 1, n).";
    //isFreeWidthSplitCurve(NewPos, LaneIn, CurveId, Lane):- gotta test the subfunction first
    var testFreeWidthSplitCurve = "isFreeWidthSplitCurve(24, 1, A, B).";
    //isFreeWidthSplitCurve2(NewPos, LaneIn, CurveId, LaneOut)
    var testFreeWidthSplitCurve2 = "isFreeWidthSplitCurve2(24, 1, A, B).";
    //test empty _
    var testEmpty = "testEmpty(1, a).";
    //test cyclist cyclist(89, 1, a, n1).
    var testCyclist = "cyclist(89, 1, a, n1, _).";

    session.consult("../prolog/game.pl", {
        success: function() {
            
            session.query(call, {  
                success: function(goal) {
                    
                    session.answer({
                        success: function(answer) {
                            console.log(session.format_answer(answer)); // X = salad ;
                            ;
                        },
                        fail: function() {console.log("fail Answer") },
                        error: function(err) {console.log(err)},
                        limit: function() { }
                    });
                

                },
                error: function(err) { console.log("error query") }
            });


         },
        error: function(err) { console.log(err) }
    });

  
    //nextMove(Position, _ , Movement, NewPos, Lane, CurveId)

    axios.post('http://127.0.0.1:5000/', {
      testData: 'hello world from node code'
    })
})
app.post('/API/chatbot',jsonParser,cors(),function(req,res) {
    var body=req.body;
    console.log(body);
    const goal= ` 
    produire_reponse([${body.query}],L_reponse),
    convert_sentence(L_reponse, Message).
    
`;console.log(goal)
    session.consult("../prolog/chat_bot.pl",{
        success: function() {
            
            session.query(goal, {  
                success: function() {
                    
                    session.answer({
                        success: function(answer) {
                            //console.log(answer);
                            console.log(session.format_answer(answer));
                            const response = answer.lookup('Message');
                            //console.log(response);
                            axios.post('http://127.0.0.1:5000/', {
                            testData: response
                                })
                            ;
                        },
                        fail: function() {console.log("fail Answer") },
                        error: function(err) {console.log(err); console.log("fail")},
                        limit: function() { }
                    });

                    
                

                },
                error: function(err) { console.log("ko") }
            });


         },
        error: function(err) { console.log(err) }
    }
    );






})

app.post('/API/play',jsonParser, cors(),  function(req, res) {

    
    //console.log(res);
    var body = req.body;
    
    console.log(body);

    getLast(body.team, body.card);


    
})


app.post('/API/testAdd',jsonParser, cors(),  function(req, res) {
    //console.log(res);
  
    var testAddCyclist = "asserta(cyclist(1, 0, n, n1, _)).";

    session.consult("../prolog/game.pl", {
        success: function() {
            
            session.query(testAddCyclist, {  
                success: function(goal) {
                    
                    session.answer({
                        success: function(answer) {
                            console.log(session.format_answer(answer)); 
                            ;
                        },
                        fail: function() {console.log("fail Answer") },
                        error: function(err) {console.log("this is the error");console.log(err)},
                        limit: function() { }
                    });
                

                },
                error: function(err) { console.log("error query") }
            });


         },
        error: function(err) { console.log(err) }
    });

  
    axios.post('http://127.0.0.1:5000/', {
      testData: 'This is the add function response'
    })
})

app.post('/API/testNewAdd',jsonParser, cors(),  function(req, res) {
    //console.log(res);
  
    var testAddCyclist = "cyclist(0, 0, n, n1, _).";

    session.consult("../prolog/game.pl", {
        success: function() {
            
            session.query(testAddCyclist, {  
                success: function(goal) {
                    
                    session.answer({
                        success: function(answer) {
                            console.log(session.format_answer(answer)); // X = salad ;
                            ;
                        },
                        fail: function() {console.log("fail Answer") },
                        error: function(err) {console.log(err)},
                        limit: function() { }
                    });
                

                },
                error: function(err) { console.log("error query") }
            });


         },
        error: function(err) { console.log(err) }
    });

  
    axios.post('http://127.0.0.1:5000/', {
      testData: 'This is the check new term function response'
    })
})

app.listen(port, hostname, () => {
console.log(`Server running at http://${hostname}:${port}/`);
});



function updateCyclist() {
    
    var testCyclist = "cyclist(89, 1, a, n1, _).";

    session.consult("../prolog/game.pl", {
        success: function() {
            
            session.query(call, {  
                success: function(goal) {
                    
                    session.answer({
                        success: function(answer) {
                            console.log(session.format_answer(answer)); // X = salad ;
                            ;
                        },
                        fail: function() {console.log("fail Answer") },
                        error: function(err) {console.log(err)},
                        limit: function() { }
                    });
                

                },
                error: function(err) { console.log("error query") }
            });


         },
        error: function(err) { console.log(err) }
    });
    //nextMove(Position, _ , Movement, NewPos, Lane, CurveId)
}


async function getLast(team, card) {
    //getLast(1, Id), getPosition(Id, Pos, Lane). this works in the sandbox but not here whyyyyyyyyyyyyyyyy
    var testLast = "getLast("+team+", Id), getPosition(n1, Position, Lane).";

    session.consult("../prolog/game.pl", {
        success: function() {
            
            session.query(testLast, {  
                success: function(goal) {
                    
                    session.answer({
                        success: function(answer) {
                            console.log(answer.lookup("Id").id);
                            console.log(answer.lookup("Position").value);
                            play([answer.lookup("Position").value, answer.lookup("Lane").value, answer.lookup("Id").id], card); // X = salad ;
                            
                            //this is the second request
                           
                            //return idResponse;
                        },
                        fail: function() {return false;},
                        error: function(err) {return "error"},
                        limit: function() {}
                    });

                   
                },
                error: function(err) { console.log("error query") }
            });

            
         },
        error: function(err) { console.log(err) }
    });


    //nextMove(Position, _ , Movement, NewPos, Lane, CurveId)
}

function play(pos, card){
    

    //"nextMove(1,1,4, NewPos, NewLane, NewCurveId).";
    var call = "nextMove(" + pos[0] + "," + pos[1] + "," + card + ", NewPos, NewLane, NewCurveId).";
    

    session.consult("../prolog/game.pl", {
        success: function() {
            
            session.query(call, {  
                success: function(goal) {
                    
                    session.answer({
                        success: function(answer) {
                            changeCyclistValues([pos[0], pos[1], answer.lookup("NewPos").value, answer.lookup("NewLane").value, answer.lookup("NewCurveId").id, pos[2]]); // X = salad ;
                            ;
                        },
                        fail: function() {
                            axios.post('http://127.0.0.1:5000/', {
                                testData: 'Play returned false'
                                })
                        },
                        error: function(err) {console.log(err)},
                        limit: function() { }
                    });
                

                },
                error: function(err) { console.log("error query") }
            });


         },
        error: function(err) { console.log(err) }
    });

  
    //nextMove(Position, _ , Movement, NewPos, Lane, CurveId)

    //axios.post('http://127.0.0.1:5000/', {
    //  testData: 'The next move was calculated'
    //})
    

}


function changeCyclistValues(answ){


    if (answ[5][0] == "b"){
        team = 0;
    }
    else if (answ[5][0] == "n"){
        team = 1;
    }
    else if (answ[5][0] == "g"){
        team = 2;
    }
    else {
        team = 3;
    }
    
    //answer.lookup("NewPos").value, answer.lookup("NewLane").value, answer.lookup("NewCurveId").id
    var changeValues = "retract(cyclist(_, _, _,"+answ[5]+",_)), asserta(cyclist("+answ[2]+","+answ[3]+","+answ[4]+","+answ[5]+","+team+")).";

    session.consult("../prolog/game.pl", {
        success: function() {
            
            session.query(changeValues, {  
                success: function(goal) {
                    
                    session.answer({
                        success: function(answer) {
                            console.log(session.format_answer(answer)); // X = salad ;
                            getCyclists();
                            //testAdd(answer);
                            ;
                        },
                        fail: function() {
                            axios.post('http://127.0.0.1:5000/', {
                                testData: 'Play returned false'
                                })
                        },
                        error: function(err) {console.log(err)},
                        limit: function() { }
                    });
                

                },
                error: function(err) { console.log("error query") }
            });


         },
        error: function(err) { console.log(err) }
    });

}

function getCyclists(){

    var changeValues = "bagof(cyclist(A,B,C,D,E), clause(cyclist(A,B,C,D,E), _), Bag).";

    session.consult("../prolog/game.pl", {
        success: function() {
            
            session.query(changeValues, {  
                success: function(goal) {
                    
                    session.answer({
                        success: function(answer) {
                            allData0 = answer.lookup("Bag").args[0];
                            allData1 = answer.lookup("Bag").args[1];
                            allData11 = answer.lookup("Bag").args[1].args[0];
                            allData12 = answer.lookup("Bag").args[1].args[1];
                            allData121 = answer.lookup("Bag").args[1].args[1].args[0];
                            allData122 = answer.lookup("Bag").args[1].args[1].args[1];
                            
                            var listAllCyclist = [];
                            var lastCylist;
                            for (let i = 0; i < 12; i++){
                                if (i == 0){
                                    lastCylist = answer.lookup("Bag");
                                    listAllCyclist.push(lastCylist);
                                }
                                lastCylist = lastCylist.args[1];
                                listAllCyclist.push(lastCylist);
                            } 

                            var listObjectCyclist = [];

                            for (let i = 0; i < 12; i++){
                                listObjectCyclist.push(listAllCyclist[i].args[0]);
                            }

                            var cylistData;
                            var listToSend = [];
                            for (let i = 0; i < 12; i++){
                                var cylistData = [listObjectCyclist[i].args[0].value, listObjectCyclist[i].args[1].value, listObjectCyclist[i].args[2].id, listObjectCyclist[i].args[3].id, listObjectCyclist[i].args[4].value];
                                listToSend.push(cylistData);
                            }

                            axios.post('http://127.0.0.1:5000/', {
                                "allCyclists": JSON.stringify(listToSend)
                                });
                            ;
                        },
                        fail: function() {
                            axios.post('http://127.0.0.1:5000/', {
                                testData: 'Play returned false'
                                })
                        },
                        error: function(err) {console.log(err)},
                        limit: function() { }
                    });
                

                },
                error: function(err) { console.log("error query") }
            });


         },
        error: function(err) { console.log(err) }
    });

}
