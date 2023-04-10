

var session = pl.create();


session.consult("../prolog/test.pl", {
    success: function() {console.log("ok") },
    error: function(err) { /* Error parsing program */ }
});


session.query("likes(sam, X).", {
    success: function(goal) { /* Goal loaded correctly */ },
    error: function(err) { /* Error parsing goal */ }
});