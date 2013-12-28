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

define("port", default=8888, help="Run Socket Server on the given port", type=int)
define("status_file", default='status.eot', help="Location of the Chadburn status file")
BASEDIR = os.path.abspath(os.path.dirname(__file__))
STATUSFILE = options.status_file
MAX_WAIT = 5 #Seconds, before shutdown in signal


#Store clients in a dictionary..
clients = dict()

def get_status():

    with open(STATUSFILE, 'r') as status_file:
        status = status_file.read()
    return status

@gen.engine
def status_watcher():
    print "Sleeping"
    yield gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 15)
    print "Awake!"

def sig_handler(sig, frame):
    tornado.ioloop.IOLoop.instance().add_callback_from_signal(shutdown)

def shutdown():
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

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        self.render("panel.html")

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.id = uuid.uuid4()
        self.stream.set_nodelay(True)
        clients[self.id] = {"id": self.id, "object": self}
        print "New Client : %s" % (self.id)
        self.write_message("Connected to EOT Server")
        tornado.ioloop.PeriodicCallback(self.ext_task, 10000, io_loop=None).start() #Testing Polling incase it's needed

    def on_message(self, message):        
        print "Received a message from Client %s : %s" % (self.id, message)
        if (message == 'base'):
            self.write_message(u"Base Directory: " + BASEDIR)
        elif (message == 'file'):
            self.write_message(u"EOT Status file: " + STATUSFILE)
        elif (message == 'shutdown'):
            #this probably wont happen in the production version, but it's useful for debugging...
            self.write_message(u"Shuttingdown EOT Server")
            tornado.ioloop.IOLoop.instance().add_callback(shutdown)
        elif (message == 'status'):
            status = get_status()
            self.write_message(u"Current Status: " + status)
        else:
            self.write_message(u"Server echoed: " + message)
        
    def on_close(self):
        print "Client %s disconnected." % self.id
        if self.id in clients:
            del clients[self.id]
    
    def ext_task(self):
        self.write_message("Scheduled")

app = tornado.web.Application([
    (r'/', IndexHandler),
    (r'/websocket', WebSocketHandler),
])

if __name__ == '__main__':
    parse_command_line()
    app.listen(options.port)

    #Signal Register
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    tornado.ioloop.IOLoop.instance().add_callback(status_watcher)
    tornado.ioloop.IOLoop.instance().start()
