window.onload = function () {
    /* Snap.svg controllers, each click updates the handle position and sends an acceptance response through the socket */
    var eot = Snap.select("#EOT");

    eot.select("#stop-area").click(function () {
        spin(0,1);
        ws.send("Accept&6");
    });
    eot.select("#coffee-area").click(function () {
        spin(20.84,1);
        ws.send("Accept&7");
    });
    eot.select("#lunch-area").click(function () {
        spin(41.68,1);
        ws.send("Accept&8");
    });
    eot.select("#eww-area").click(function () {
        spin(62.52,1);
        ws.send("Accept&9");
    });
    eot.select("#siwoti-area").click(function () {
        spin(83.36,1);
        ws.send("Accept&10");
    });
    eot.select("#battle-area").click(function () {
        spin(104.20,1);
        ws.send("Accept&11");
    });
    eot.select("#next-area").click(function () {
        spin(-20.84,1);
        ws.send("Accept&5");
    });
    eot.select("#reverse-area").click(function () {
        spin(-41.68,1);
        ws.send("Accept&4");
    });
    eot.select("#slow-area").click(function () {
        spin(-62.52,1);
        ws.send("Accept&3");
    });
    eot.select("#half-area").click(function () {
        spin(-83.36,1);
        ws.send("Accept&2");
    });
    eot.select("#full-area").click(function () {
        spin(-104.20,1);
        ws.send("Accept&1");
    });
};

function spin(angle, type) {
    /* Takes arguments of rotation angle (self explanatory)
     * and type: 0 = command (coming from the web socket)
     *           1 = click (sends an ACK through the websocket)
     *           2 = startup (a command, but assumes this command
     *                        is already accepted - only used on
     *                        new client connections) */
    
    if (type > 0) {        
        Snap.select("#EOT").select("#handle").animate({ 
            transform: "r" + [angle, 1400, 1400]
        }, 1000, mina.backout);
    }
    if (type !== 1) {
        Snap.select("#EOT").select("#indicator").animate({ 
            transform: "r" + [angle, 1400, 1400]
        }, 1500, mina.bounce);
        
        document.getElementById("bell").play();
    }
}
            
