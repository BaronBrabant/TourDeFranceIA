
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
    var body = req.body;
    
    console.log(body);


    axios.post('http://127.0.0.1:5000/', {
      testData: 'hello world from node code'
    })
})

app.post('/API/play',jsonParser, cors(),  function(req, res) {
    //console.log(res);
    var body = req.body;
    
    console.log(body);

    //"nextMove(1,1,4, NewPos, NewLane, NewCurveId).";
    var call = "nextMove(" + body.position + "," + body.lane + "," + body.card + ", NewPos, NewLane, NewCurveId).";
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