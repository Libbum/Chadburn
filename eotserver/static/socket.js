var ws = new WebSocket("ws://localhost:1873/websocket");

ws.onmessage = function(evt){
    x = document.createElement("p");
    x.innerHTML = evt.data;
    document.getElementById("console").appendChild(x);
    switch (evt.data) {
        case "1":
            /* Full */
            spin(-104.20,0);
            break;
        case "2":
            /* Half */
            spin(-83.36,0);
            break;
        case "3":
            /* Slow */
            spin(-62.52,0);
            break;
        case "4":
            /* Reverse */
            spin(-41.68,0);
            break;
        case "5":
            /* Next */
            spin(-20.84,0);
            break;
        case "6":
            /* Stop */
            spin(0,0);
            break;
        case "7":
            /* Coffee */
            spin(20.84,0);
            break;
        case "8":
            /* Lunch */
            spin(41.68,0);
            break;
        case "9":
            /* Engine Working Wrong */
            spin(62.52,0);
            break;
        case "10":
            /* SIWOTI */
            spin(83.36,0);
            break;
        case "11":
            /* Battle Stations */
            spin(104.20,0);
            break;
        default:
            break;
    }
}
   
function DispatchResponse(){
    var userInput = document.getElementById("message").value;
    document.getElementById("message").value = "";
    x = document.createElement("p");
    x.innerHTML = "You sent: " + userInput;
    document.getElementById("console").appendChild(x);
    ws.send(userInput);
}

