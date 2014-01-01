#!/usr/bin/python2

import os
import signal
import time
import tornado.ioloop
import tornado.web
import tornado.websocket
import uuid

from tornado import gen
from tornado.options import define, options, parse_command_line
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

define("port", default=1873, help="Run Socket Server on the given port", type=int)
define("status_file", default='status.eot', help="Location of the Chadburn status file")
define("accept_file", default='accept.eot', help="Location of the Chadburn acceptance file")
BASEDIR = os.path.abspath(os.path.dirname(__file__))
STATUSFILE = options.status_file
MAX_WAIT = 5 #Seconds, before shutdown in signal
observer = Observer()

#Store clients in a dictionary..
clients = dict()

def get_status():

    with open(STATUSFILE, 'r') as status_file:
        status = status_file.read()
    return status.rstrip()

def write_accept(cmd):

    with open(options.accept_file, 'w') as accept_file:
        accept_file.write(cmd)

def broadcast(message):
    for ids, ws in clients.items():
        if not ws.ws_connection.stream.socket:
            del clients[ids]
        else:
            ws.write_message(message)

@gen.engine
def status_watcher():
    event_handler = ChangeHandler(patterns=[BASEDIR + '/' + STATUSFILE],
                                      ignore_directories=True,
                                      case_sensitive=True)
    observer.schedule(event_handler, BASEDIR, recursive=False)
    observer.start()
    try:
        while True:
            yield gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 1)
    except:
        pass
    observer.join()

def sig_handler(sig, frame):
    tornado.ioloop.IOLoop.instance().add_callback_from_signal(shutdown)

def shutdown():
    print "Stopping Status Watcher..."
    observer.stop()
    print "Shutting down EOT server (will wait up to %s seconds to complete running threads ...)" % MAX_WAIT
    
    instance = tornado.ioloop.IOLoop.instance()
    deadline = time.time() + MAX_WAIT
 
    def terminate():
        now = time.time()
        if now < deadline and (instance._callbacks or instance._timeouts):
            instance.add_timeout(now + 1, terminate)
        else:
            instance.stop()
            print "Shutdown."
    terminate()

class ChangeHandler(PatternMatchingEventHandler):

    def on_modified(self, event):
        status = get_status()
        print "File modified! Current status: " + status
        broadcast(status)

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("panel.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.id = uuid.uuid4()
        self.stream.set_nodelay(True)
        clients[self.id] = self
        print "New Client : %s" % (self.id)
        self.write_message("Connected to EOT Server")
        self.write_message(get_status() + "&1") #Push initial status and assume acknowledgement

    def on_message(self, message):        
        print "Received a message from Client %s : %s" % (self.id, message)
        
        commands = message.split("&")
        
        if (message == 'base'):
            self.write_message(u"Base Directory: " + BASEDIR)
        elif (message == 'file'):
            self.write_message(u"EOT Status file: " + STATUSFILE)
        elif (message == 'shutdown'):
            #this probably wont happen in the production version, but it's useful for debugging...
            self.write_message(u"Shutting down EOT Server")
            tornado.ioloop.IOLoop.instance().add_callback(shutdown)
        elif (message == 'status'):
            status = get_status()
            self.write_message(u"Current Status: " + status)
        elif (len(commands) > 1):
            #Incomming command (for now this is just ACK)
            if (commands[0] == 'Accept'):
                self.write_message(u"Recieved Acceptance for state: " + commands[1])
                write_accept(commands[1] + '\n')
        else:
            self.write_message(u"Server echoed: " + message)
        
    def on_close(self):
        print "Client %s disconnected." % self.id
        if self.id in clients:
            del clients[self.id]
    
app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/websocket', WebSocketHandler),
    (r'/static/(.*)',tornado.web.StaticFileHandler, {'path': './static'},),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)

    #Signal Register
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    tornado.ioloop.IOLoop.instance().add_callback(status_watcher)
    tornado.ioloop.IOLoop.instance().start()
