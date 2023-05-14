
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

function playCard(Team){

    /*
    axios.post('http://127.0.0.1:3000/API/test', {
        body: JSON.stringify({
            data : "hello world from html"
        })
    })

    Position, LaneIn, Movement
    */

    var Card = document.getElementById("cardChosen").value;
    $("#cardChosen").val("");
    //document.getElementById("cardChosen").innerHTML = "";
    Card = parseInt(Card);

    console.log(Card);
    console.log(Team);

    if (isNaN(Card)){
        alert("Please enter a valid card number!");
        return;
    }

    var data = {};
                data.card = Card;
                data.team = Team;

    jQuery.ajax({
        type : 'POST',
        url : "http://127.0.0.1:5000/API/game",
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

function writeResponseBot(botResponse){
    alert(botResponse)
    document.getElementById("tbot").innerHTML +="<p><strong>Tbot : </strong>" + botResponse + "</p>";
}

function bot(){

    var data={}
    
    var userInput = document.getElementById("question").value;
    userInput = userInput.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    
    console.log(userInput)
    document.getElementById("tbot").innerHTML +="<p><strong>Vous : </strong>" + userInput + "</p>";
            data.query=userInput.toLowerCase().split(" ");
            console.log("coucou 1")
            jQuery.ajax({       
                type: 'POST',
                url: "/API/prolog/chatbotAsk",
                data: JSON.stringify(data),
                contentType: "application/json; charset=utf-8",
                success: function(response) {
                    var botResponse = response.testData;
                    console.log("Coucou ")
                    document.getElementById("tbot").innerHTML +="<p><strong>Tbot : </strong>" + botResponse + "</p>";
                },
                error: function(response) {
                    console.log("Erreur :");
                }
            });
            $("#question").val(""); // Vider le champ de saisie
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
var selectedIndex = []
function switchCard(cardIndex, team){
    if (!selectedIndex.includes(cardIndex)){
        document.getElementById(team+String((cardIndex+1))).style.backgroundColor = 'Lightgreen'
        selectedIndex.push(cardIndex)
    }else{
        document.getElementById(team+String((cardIndex+1))).style.backgroundColor = 'white'
        selectedIndex = selectedIndex.filter(function (idx) {
            return idx !== cardIndex;
        });
    }
    console.log(selectedIndex)

}

function renew(){
    if (selectedIndex.length === 3){
        jQuery.ajax({
            type : 'POST',
            url : "http://127.0.0.1:5000/API/renewCards",
            data : JSON.stringify(selectedIndex),
            contentType: "application/json; charset=utf-8",
          });
    }
}