/* Socket controlling functions */

/* The sockets adress will be updated to it's correct location after testing */
var ws = new WebSocket("ws://127.0.0.1:1873/websocket");

ws.onmessage = function(evt){
    /* Debug log, may be removed in a future version */
    x = document.createElement("p");
    x.innerHTML = evt.data;
    document.getElementById("console").appendChild(x);

    /* Checx to see if an additional command has been sent */
    var cmd = evt.data.split("&");
    var type = 0;
    if (cmd.length > 1) {
        if (cmd[1] === "1") {
            /* Startup */
            type = 2;
        } else if (cmd[1] === "3") {
            //This is a broadcasted ACK
            type = 3;
        }
    }
    /* If the message is a number from 1 to 11, this is interpreted as a status change */
    // The third command is a lazy hack, but should be fine for the purposes needed here.
    switch (cmd[0]) {
        case "1":
            /* Full */
            spin(-104.20,type,1);
            break;
        case "2":
            /* Half */
            spin(-83.36,type,2);
            break;
        case "3":
            /* Slow */
            spin(-62.52,type,3);
            break;
        case "4":
            /* Reverse */
            spin(-41.68,type,4);
            break;
        case "5":
            /* Next */
            spin(-20.84,type,5);
            break;
        case "6":
            /* Stop */
            spin(0,type,6);
            break;
        case "7":
            /* Coffee */
            spin(20.84,type,7);
            break;
        case "8":
            /* Lunch */
            spin(41.68,type,8);
            break;
        case "9":
            /* Engine Working Wrong */
            spin(62.52,type,9);
            break;
        case "10":
            /* SIWOTI */
            spin(83.36,type,10);
            break;
        case "11":
            /* Battle Stations */
            spin(104.20,type,11);
            break;
        default:
            break;
    }
}

function DispatchResponse(){
    /* A debugging function to take the command written in the console and push it through the web socket */
    var userInput = document.getElementById("message").value;
    document.getElementById("message").value = "";
    x = document.createElement("p");
    x.innerHTML = "You sent: " + userInput;
    document.getElementById("console").appendChild(x);
    ws.send(userInput);
}

