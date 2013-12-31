window.onload = function () {
    var eot = Snap.select("#EOT"),
        indicator = eot.select("#indicator"),
        handle = eot.select("#handle"),

        timer;

    var pivot = [1400, 1400];
            
    function stop() {
        clearTimeout(timer);

        indicator.animate({ 
            transform: "r" + [0, pivot]
        }, 1000, mina.backout);
                
        handle.animate({ 
            transform: "r" + [0, pivot]
        }, 1000, mina.backout);
                
    }

    function spin(a) {
        clearTimeout(timer);

        indicator.animate({ 
            transform: "r" + [a, pivot]
        }, 1000, mina.backout);
                
        handle.animate({ 
            transform: "r" + [a, pivot]
        }, 1000, mina.backout);
                
    }

    timer = setTimeout(stop, 50);
            
    eot.select("#stop-area").click(function () {
        spin(0);
    });
    eot.select("#coffee-area").click(function () {
        spin(20.84);
    });
    eot.select("#lunch-area").click(function () {
        spin(41.68);
    });
    eot.select("#eww-area").click(function () {
        spin(62.52);
    });
    eot.select("#siwoti-area").click(function () {
        spin(83.36);
    });
    eot.select("#battle-area").click(function () {
        spin(104.20);
    });
    eot.select("#next-area").click(function () {
        spin(-20.84);
    });
    eot.select("#reverse-area").click(function () {
        spin(-41.68);
    });
    eot.select("#slow-area").click(function () {
        spin(-62.52);
    });
    eot.select("#half-area").click(function () {
        spin(-83.36);
    });
    eot.select("#full-area").click(function () {
        spin(-104.20);
    });
};

