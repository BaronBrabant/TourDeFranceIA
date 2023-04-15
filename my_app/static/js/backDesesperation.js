
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

//const plTest = require('./prologCalls.js');



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

    var call = "nextMove(1,1,4, NewPos, NewLane, NewCurveId).";
    var positionCheck = "getPositionWidth(68, X).";
    var positionCheck2 = "getPositionCurve(8).";
    var checkNot = "doesNotWork(false).";
    var testLegalCurve = "isLegalInsideCurve(2, c, 2).";
    var testMember = "doesMemWork(1, [1,2,3]).";

    session.consult("../prolog/game.pl ", {
        success: function() {
            
            session.query(positionCheck2, {  
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
                error: function(err) { console.log("ko") }
            });


         },
        error: function(err) { console.log(err) }
    });

  

    //nextMove(Position, _ , Movement, NewPos, Lane, CurveId)
 

    

    

    axios.post('http://127.0.0.1:5000/', {
      testData: 'hello world from node code'
    })
})

app.listen(port, hostname, () => {
console.log(`Server running at http://${hostname}:${port}/`);
});