
const axios = require('axios');

const hostname = '127.0.0.1';
const port = 3000;

const http = require('http');
const https = require('https');

const pl = require('tau-prolog');
//const plTest = require('./prologTest.js');
var session = pl.create();


axios.post('http://127.0.0.1:5000/', {
    testData: 'hello world'
  })



const server = http.createServer((req, res) => {
    res.statusCode = 200;

    res.setHeader('Content-Type', 'text/plain');
    

    session.consult("../prolog/test.pl", {
            success: function() {console.log("ok") },
            error: function(err) { console.log(err) }
        });

    session.query("likes(sam, X).", {
        success: function(goal) {console.log(goal)},
        error: function(err) { /* Error parsing goal */ }
    });
    res.end('Hello World');

    session.answer({
        success: function(answer) {
            console.log(session.format_answer(answer)); // X = salad ;
            ;
        },
        fail: function() { /* No more answers */ },
        error: function(err) { /* Uncaught exception */ },
        limit: function() { /* Limit exceeded */ }
    });
});

server.listen(port, hostname, () => {
console.log(`Server running at http://${hostname}:${port}/`);
});