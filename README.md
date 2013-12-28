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
Currently the filewatcher will check for modifications on the status file, then push the updated status through the websocket to the status panel. Rudimentry debug control is also available but will probably be removed in the future. The socket server has graceful failures implimented as well; so most of the backend is completed. 

__TODO:__

* [] Comment the server file
* [] Rework `panel.html` to be actual panel-like rather than a debug box

Control Board
-------------

Will be using a [Teensy](http://www.pjrc.com/teensy/) once it arrives in the mail.
