//document.getElementById("demo").innerHTML = "Jokes 0: " + jokes[0].keywords;

function styleBasketButton(btn) {    
    btn.style.backgroundColor = 'rgb(0, 132, 255)';
    btn.style.color = 'white';
}


function colorBasketTable() {
    

    for(let joke in jokes) {


        let data = sessionStorage.getItem(joke);
        if(data != null) {
            styleBasketButton(document.getElementById(joke));
            
        }
    }
}


function addToBasket(elem) {
    let id = elem.id;

    sessionStorage.setItem(id, JSON.stringify(jokes[id-1]));

    styleBasketButton(elem);
}

function removeBasketOwned(){

    for (let jokes in jokesOwned){
        let data = sessionStorage.getItem(jokes);
        if (data != null){
            sessionStorage.removeItem(jokes);
        }
    }
}



function toggleJoke() {
    var x = document.getElementById('joke');
    if (x.style.visibility === 'hidden') {
        console.log("hello");
      x.style.visibility = 'visible';
    } else {
      x.style.visibility = 'hidden';
    }
}

$(document).ready(function() {
    $('#myTable').DataTable({
        columnDefs: [
            { orderable: false, targets: 3 }
        ],
        "bLengthChange": false,
        order: [[2, 'asc']],
        info: false,
    });
} );


jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});

removeBasketOwned();
colorBasketTable();
