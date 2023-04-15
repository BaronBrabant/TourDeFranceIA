
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

    /*
    axios.post('http://127.0.0.1:3000/API/test', {
        body: JSON.stringify({
            data : "hello world from html"
        })
    })
    */
    var data = {};
                data.title = "title";
                data.message = "message";

    jQuery.ajax({
        type : 'POST',
        url : "http://127.0.0.1:3000/API/test",
        data : JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
      });
    

}

function playCard(Position, LaneIn){

    /*
    axios.post('http://127.0.0.1:3000/API/test', {
        body: JSON.stringify({
            data : "hello world from html"
        })
    })

    Position, LaneIn, Movement
    */

    var Card = document.getElementById("cardChosen").value;
    Card = parseInt(Card);

    console.log(Card);

    if (isNaN(Card)){
        alert("Please enter a valid card number!");
        return;
    }

    var data = {};
                data.card = Card;
                data.position = Position;
                data.laneIn = LaneIn;

    jQuery.ajax({
        type : 'POST',
        url : "http://127.0.0.1:3000/API/play",
        data : JSON.stringify(data),
        contentType: "application/json; charset=utf-8",
      });
    

}


function addNewRider(){

    jQuery.ajax({
        type : 'POST',
        url : "http://127.0.0.1:3000/API/testAdd",
        contentType: "application/json; charset=utf-8",
      });
    

}

function checkNewRider(){

    jQuery.ajax({
        type : 'POST',
        url : "http://127.0.0.1:3000/API/testNewAdd",
        contentType: "application/json; charset=utf-8",
      });
    

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