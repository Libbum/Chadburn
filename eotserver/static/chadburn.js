window.onload = function () {
    var eot = Snap.select("#EOT");

    eot.select("#stop-area").click(function () {
        spin(0,1);
    });
    eot.select("#coffee-area").click(function () {
        spin(20.84,1);
    });
    eot.select("#lunch-area").click(function () {
        spin(41.68,1);
    });
    eot.select("#eww-area").click(function () {
        spin(62.52,1);
    });
    eot.select("#siwoti-area").click(function () {
        spin(83.36,1);
    });
    eot.select("#battle-area").click(function () {
        spin(104.20,1);
    });
    eot.select("#next-area").click(function () {
        spin(-20.84,1);
    });
    eot.select("#reverse-area").click(function () {
        spin(-41.68,1);
    });
    eot.select("#slow-area").click(function () {
        spin(-62.52,1);
    });
    eot.select("#half-area").click(function () {
        spin(-83.36,1);
    });
    eot.select("#full-area").click(function () {
        spin(-104.20,1);
    });
};

function spin(angle, type) {
    if (type === 1) {        
        Snap.select("#EOT").select("#handle").animate({ 
            transform: "r" + [angle, 1400, 1400]
        }, 1000, mina.backout);
    } else {
        Snap.select("#EOT").select("#indicator").animate({ 
            transform: "r" + [angle, 1400, 1400]
        }, 1500, mina.bounce);

        document.getElementById("bell").play();
    }
}
            
