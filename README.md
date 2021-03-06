Chadburn
========

All files required for the CQPLabs Engine Order Telegraph project. 

Updates and further description will be soon found on the [CPQLabs](http://cqplabs.neophilus.net) site.

Web Server
----------

Written in Python, mainly because I'm not a fan of Ruby and the machine this project will ultimately be deployed on already has Python installed for the most part, and I'd be pushing it to insist Haskell was installed on it...

Also, because this is all a learning experience anyway; I thought it may be time to see what this Python doohickey is all about.

![Moi](http://oi39.tinypic.com/15moaqb.jpg)

__Dependencies:__ 

* [Tornado](http://www.tornadoweb.org) (for websockets)
* [Watchdog](http://pythonhosted.org/watchdog/) (for the file watcher)

__Status:__
Currently the filewatcher will check for modifications on the status file, then push the updated status through the websocket to the status panel. Rudimentry debug control is also available but will probably be removed in the future. The socket server has graceful failures implimented as well.

The panel is also complete. SVG animations have been built, javascript control is working fine, push notifications update the panel and send a chime notification. An accept command is sent once the user clicks to a control area.

__TODO:__

* [X] Comment the server file
* [X] Rework `panel.html` to be actual panel-like rather than a debug box
* [X] Build acknowledgements into the panel
* [X] Remove debugging options or hide them so they don't complicate the panel

Control Board
-------------

Will be using a [Teensy](http://www.pjrc.com/teensy/), it has just arrived in the mail so prototyping will begin soon.

__Status:__
Had to build the teensyduino from AUR, the dependencies took a bit; but now that's working fine and I can program the board no problems.

Good news actually - looks like I'll be able to spit the status values directly to python through a serial connection; meaning no file watcher requirements! I've currently set up a minimal arduino program that will push a random status (between 1 and 11) every ten seconds - so I can recode the server to accept a serial connection and push that result through the web socket.

Need to go switch shopping as well - may look in to a rotary switch or a set of momentary micro swithes; not sure what'll be the best just yet.
