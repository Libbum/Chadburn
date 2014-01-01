#!/usr/bin/python2

import os
import signal
import time
import uuid

from tornado import gen, ioloop, web, websocket
from tornado.options import define, options, parse_command_line
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

define("port", default=1873, help="Run Socket Server on the given port", type=int)
define("status_file", default='status.eot', help="Location of the Chadburn status file")
define("accept_file", default='accept.eot', help="Location of the Chadburn acceptance file")
BASEDIR = os.path.abspath(os.path.dirname(__file__))
MAX_WAIT = 5 #Seconds, before shutdown in signal

observer = Observer() #Filewatcher
clients = dict() #List of all connections

def get_status():
    """
    Reads the contents of the status file when requested
    """
    with open(options.status_file, 'r') as status_file:
        status = status_file.read()
    return status.rstrip()

def write_accept(cmd):
    """
    Writes to the acceptance file the current accepted state.
    This value should ultimately change the mechanical EOT's
    status to an acknowledgement position.
    """
    with open(options.accept_file, 'w') as accept_file:
        accept_file.write(cmd)

def broadcast(message):
    """
    Pushes a message to all currently connected clients.
    Tests connection before hand just in case a disconnect
    has just occurred.
    """
    for ids, ws in clients.items():
        if not ws.ws_connection.stream.socket:
            del clients[ids]
        else:
            ws.write_message(message)

@gen.engine
def status_watcher():
    """
    File watchdog. Using the PatternMatching event handler to minimize overhead. By default the watchdog
    observes all files and folders recursively from the base directory. This setup only watches the 
    supplied status_file.
    """
    event_handler = ChangeHandler(patterns=[BASEDIR + '/' + options.status_file],
                                      ignore_directories=True,
                                      case_sensitive=True)
    observer.schedule(event_handler, BASEDIR, recursive=False)
    observer.start()
    try:
        while True:
            yield gen.Task(ioloop.IOLoop.instance().add_timeout, time.time() + 1) #Non-blocking thread wait
    except:
        pass #no default keyboard interrupt handler because of the shutdown function below
    observer.join()

def sig_handler(sig, frame):
    """
    Calls shutdown on the next I/O Loop iteration. Should only be used from a signal handler, unsafe otherwise.
    """
    ioloop.IOLoop.instance().add_callback_from_signal(shutdown)

def shutdown():
    """
    Graceful shutdown of all services. Can be called with kill -2 for example, a CTRL+C keyboard interrupt, 
    or 'shutdown' from the debug console on the panel.
    """
    broadcast("EOT Server is shutting down.")
    print "Stopping Status Watcher..."
    observer.stop()
    print "Shutting down EOT server (will wait up to %s seconds to complete running threads ...)" % MAX_WAIT
    
    instance = ioloop.IOLoop.instance()
    deadline = time.time() + MAX_WAIT
 
    def terminate():
        """
        Recursive method to wait for incomplete async callbacks and timeouts
        """
        now = time.time()
        if now < deadline and (instance._callbacks or instance._timeouts):
            instance.add_timeout(now + 1, terminate)
        else:
            instance.stop()
            print "Shutdown."
    terminate()

class ChangeHandler(PatternMatchingEventHandler):
    """
    Broadcasts a status change to all clients when the status_file is modified (i.e. updated)
    """
    def on_modified(self, event):
        status = get_status()
        print "Status changed to: " + status
        broadcast(status)

class IndexHandler(web.RequestHandler):
    """
    Serve up the panel
    """
    @web.asynchronous
    def get(self):
        self.render("panel.html")

class WebSocketHandler(websocket.WebSocketHandler):
    """
    Descriptions of websocket interactions. What to do when connecting/disconnecting a client and how to handle a client message
    """
    def open(self):
        self.id = uuid.uuid4() #Give client a unique identifier. This may be changed to something more personal in the future if required.
        self.stream.set_nodelay(True)
        clients[self.id] = self
        print "New Client: %s" % (self.id)
        self.write_message("Connected to EOT Server")
        self.write_message(get_status() + "&1") #Push initial status and assume acknowledgement

    def on_message(self, message):        
        print "Message from Client %s: %s" % (self.id, message)
        
        commands = message.split("&") #complex commands will be of the form command&command&command
       
        #Most of these are now superfluous. Ultimately only Accept case is needed, but will keep them here until the production version.
        if (message == 'base'):
            self.write_message(u"Base Directory: " + BASEDIR)
        elif (message == 'file'):
            self.write_message(u"EOT Status file: " + options.status_file)
        elif (message == 'shutdown'):
            self.write_message(u"Shutting down EOT Server...")
            ioloop.IOLoop.instance().add_callback(shutdown)
        elif (message == 'status'):
            status = get_status()
            self.write_message(u"Current Status: " + status)
        elif (len(commands) > 1):
            #Incoming command (for now this is just ACK)
            if (commands[0] == 'Accept'):
                self.write_message(u"Accepted state: " + commands[1])
                write_accept(commands[1] + '\n')
        else:
            self.write_message(u"Server echoed: " + message)
        
    def on_close(self):
        print "Client %s disconnected." % self.id
        if self.id in clients:
            del clients[self.id]
    
app = web.Application([
    (r'/', IndexHandler),
    (r'/websocket', WebSocketHandler),
    (r'/(favicon.ico)', web.StaticFileHandler, {'path': ''},),
    (r'/static/(.*)', web.StaticFileHandler, {'path': './static'},),
])

if __name__ == '__main__':
    #Set up server
    parse_command_line()
    app.listen(options.port)

    #Signal Register
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    
    #Start the file watcher
    ioloop.IOLoop.instance().add_callback(status_watcher)
    #Start the server main loop
    ioloop.IOLoop.instance().start()
