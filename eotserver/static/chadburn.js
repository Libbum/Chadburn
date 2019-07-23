window.onload = function () {
    /* Snap.svg controllers, each click updates the handle position and sends an acceptance response through the socket */
    var eot = Snap.select("#EOT");

    eot.select("#stop-area").click(function () {
        spin(0,1,6);
    });
    eot.select("#coffee-area").click(function () {
        spin(20.84,1,7);
    });
    eot.select("#lunch-area").click(function () {
        spin(41.68,1,8);
    });
    eot.select("#eww-area").click(function () {
        spin(62.52,1,9);
    });
    eot.select("#siwoti-area").click(function () {
        spin(83.36,1,10);
    });
    eot.select("#battle-area").click(function () {
        spin(104.20,1,11);
    });
    eot.select("#next-area").click(function () {
        spin(-20.84,1,5);
    });
    eot.select("#reverse-area").click(function () {
        spin(-41.68,1,4);
    });
    eot.select("#slow-area").click(function () {
        spin(-62.52,1,3);
    });
    eot.select("#half-area").click(function () {
        spin(-83.36,1,2);
    });
    eot.select("#full-area").click(function () {
        spin(-104.20,1,1);
    });

};

function spin(angle, type, location) {
    /* Takes arguments of rotation angle (self explanatory)
     * and type: 0 = command (coming from the web socket)
     *           1 = click (sends an ACK or Broadcast through the websocket)
     *           2 = startup (a command, but assumes this command
     *                        is already accepted - only used on
     *                        new client connections)
     *           3 = special case: broadcasted ACK only */
    if (document.getElementById('bridge').checked) {
        switch (type) {
            case 0:
                break;
            case 1:
                Snap.select("#EOT").select("#handle").animate({ 
                    transform: "r" + [angle, 1400, 1400]
                }, 1000, mina.backout);
                ws.send("Broadcast&" + location);
                current_handle = location;
                break;
            case 2:
            case 3:
                Snap.select("#EOT").select("#indicator").animate({ 
                    transform: "r" + [angle, 1400, 1400]
                }, 1500, mina.bounce);

                current_indicator = location;
                var audio = new Audio('/static/bell.mp3');
                audio.play();
                break;
            default:
                break;
        }
    } else {
        switch (type) {
            case 0:
                Snap.select("#EOT").select("#indicator").animate({ 
                    transform: "r" + [angle, 1400, 1400]
                }, 1500, mina.bounce);

                current_indicator = location;
                var audio = new Audio('/static/bell.mp3');
                audio.play();
                break;
            case 1:
                Snap.select("#EOT").select("#handle").animate({ 
                    transform: "r" + [angle, 1400, 1400]
                }, 1000, mina.backout);
                ws.send("Accept&" + location);
                current_handle = location;
                break;
            default:
                break;
        }
    }
    console.log(current_handle);
    console.log(current_indicator);
}

