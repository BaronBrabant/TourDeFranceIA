let jokesID = Object.keys(sessionStorage);


function nbBasket() {
    //document.getElementById('nbBasket').innerHTML = basket.length;
}

function basketTable() {
    let table = document.getElementById('basketTable');
    if(table == null) {
        return
    }
    let tbody = table.querySelector('tbody');
    tbody.innerHTML = '';

    let total = 0;

    for(let jokeID of jokesID) {
        let jsonFile = sessionStorage.getItem(jokeID);
        let joke = JSON.parse(jsonFile)

        // Insert a row at the end of the table
        let newRow = tbody.insertRow(-1);
        newRow.id = jokeID;

        // Insert a cell in the row at index 0,1,2,3,4
        let tierCell = newRow.insertCell(0);
        let typeCell = newRow.insertCell(1);
        let keywordsCell = newRow.insertCell(2);
        let priceCell = newRow.insertCell(3);
        let removeCell = newRow.insertCell(4);

        if (joke.tier == 0){
            let textTierCell = document.createTextNode("Dirt");
            tierCell.appendChild(textTierCell);
        }else if (joke.tier == 1){
            let textTierCell = document.createTextNode("Vip");
            tierCell.appendChild(textTierCell);
        }else if (joke.tier == 2){
            let textTierCell = document.createTextNode("Platinum");
            tierCell.appendChild(textTierCell);
        }

        let textTypeCell = document.createTextNode(joke.type);
        typeCell.appendChild(textTypeCell);

        let textKeywordsCell = document.createTextNode(joke.keywords);
        keywordsCell.appendChild(textKeywordsCell);

        let textPriceCell = document.createTextNode(joke.price + "€");
        priceCell.appendChild(textPriceCell);

        // delete button
        let deleteButton = document.createElement('button');
        deleteButton.classList.add("deleteButton");
        deleteButton.classList.add("fa");
        deleteButton.classList.add("fa-trash");
        deleteButton.addEventListener('click', function() {
            //let rowIndex = newRow.rowIndex-1;
            //tbody.deleteRow(rowIndex);

            let key = newRow.id;
            //let joke = sessionStorage.getItem(key);
            //total = total - joke.price;
            //let textPriceCell = document.createTextNode("Tot : " + parseFloat(total).toFixed(2) + "€");
            //priceCell.appendChild(textPriceCell);

            //console.log(key);
            sessionStorage.removeItem(key);
            location.href = '/basket';
        });
        document.body.appendChild(deleteButton);
        removeCell.appendChild(deleteButton);

        total = total + joke.price;
    }

    let lastRow = tbody.insertRow(-1);
    lastRow.id = "total";
    let tierCell = lastRow.insertCell(0);
    let typeCell = lastRow.insertCell(1);
    let keywordsCell = lastRow.insertCell(2);
    let priceCell = lastRow.insertCell(3);
    let removeCell = lastRow.insertCell(4);

    let textPriceCell = document.createTextNode("Tot : " + parseFloat(total).toFixed(2) + "€");
    priceCell.appendChild(textPriceCell);
}



function pay() {
    

    jQuery.ajax({
        type : 'POST',
        data : {'data':JSON.stringify(jokesID)},
        url : "basket",
        success: function () {
            sessionStorage.clear();
            location.href = '/myJokes';
        }
      });


}

function login(){

    location.href = "/login";
}

$("#target").click(function() {
    sessionStorage.clear();
});



nbBasket();
basketTable();
console.log(jokesID)




