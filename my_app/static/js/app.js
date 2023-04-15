
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
//const plTest = require('./prologTest.js');
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

app.listen(port, hostname, () => {
console.log(`Server running at http://${hostname}:${port}/`);
});