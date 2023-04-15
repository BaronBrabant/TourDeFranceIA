
/*
var session = pl.create();


function testCall() {
    session.consult("../prolog/test.pl", {
        success: function() {console.log("ok") },
        error: function(err) {  }
    });
    session.query("likes(sam, X).", {
        success: function(goal) {  },
        error: function(err) {  }
    });
    session.answer({
        success: function(answer) {
            console.log(session.format_answer(answer)); // X = salad ;
            ;
        },
        fail: function() {  },
        error: function(err) {  },
        limit: function() { / }
    });
}
*/

function testCallNode(){

    axios.post('http://127.0.0.1:3000/', {
        testData: 'hello world'
    })

}

/*
session.consult("../prolog/test.pl", {
    success: function() {console.log("ok") },
    error: function(err) {  }
});


session.query("likes(sam, X).", {
    success: function(goal) {  },
    error: function(err) {  }
});
*/