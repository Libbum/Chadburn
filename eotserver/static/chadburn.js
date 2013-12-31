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

    function spin() {
        clearTimeout(timer);

        indicator.animate({ 
            transform: "r" + [105, pivot]
        }, 1000, mina.backout);
                
        handle.animate({ 
            transform: "r" + [-105, pivot]
        }, 1000, mina.backout);
                
    }

    timer = setTimeout(stop, 50);
            
    eot.hover(spin,
        function () {
            timer = setTimeout(stop, 300);
        }
    );
};

