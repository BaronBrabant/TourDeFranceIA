
let ratios = [];
let nb = 0;
let set = [];
let setNumber = 3;
let switcher = false;

let x = document.getElementById("mapDiv")

window.addEventListener('click',
    function (e) {

        if (switcher){
            if (setNumber == 3){setNumber = 2;}
            else{setNumber = 3}
            ratios.push(set)
            nb = 0;
            switcher = false;
        }
        
        if (setNumber == 3){
            if (nb%3==0){
                sendListBackend(ratios)
                nb = 0;
                ratios.push(set)
                set = [];
                let vals = [e.x/x.clientWidth, e.y/x.clientHeight];
                set.push(vals);
                nb++;
            }
            else {
                let vals = [e.x/x.clientWidth, e.y/x.clientHeight];
                set.push(vals);
                nb++;
            }
        }
        else {
            if (nb%2==0){
                sendListBackend(ratios)
                nb = 0;
                ratios.push(set)
                set = [];
                let vals = [e.x/x.clientWidth, e.y/x.clientHeight];
                set.push(vals);
                nb++;
            }
            else {
                let vals = [e.x/x.clientWidth, e.y/x.clientHeight];
                set.push(vals);
                nb++;
            }
        }
    }
);
 
function sendListBackend(list) {
    
    jQuery.ajax({
        type : 'POST',
        data : {'data':JSON.stringify(list)},
        url : "/",
      
      });

}