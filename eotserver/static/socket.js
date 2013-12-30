var ws = new WebSocket("ws://localhost:1873/websocket");

ws.onmessage = function(evt){
    x = document.createElement("p");
    x.innerHTML = evt.data;
    document.getElementById("console").appendChild(x);
}
   
function DispatchResponse(){
    var userInput = document.getElementById("message").value;
    document.getElementById("message").value = "";
    x = document.createElement("p");
    x.innerHTML = "You sent: " + userInput;
    document.getElementById("console").appendChild(x);
    ws.send(userInput);
}

