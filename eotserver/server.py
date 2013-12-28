#!/usr/bin/python2

import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import uuid

from tornado.options import define, options, parse_command_line

define("port", default=8888, help="run on the given port", type=int)
BASEDIR = os.path.abspath(os.path.dirname(__file__))

#Store clients in a dictionary..
clients = dict()

def get_status():

    with open('status.eot', 'r') as status_file:
        status = status_file.read()
    return status

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
        tornado.ioloop.PeriodicCallback(self.ext_task, 10000, io_loop=None).start()

    def on_message(self, message):        
        print "Received a message from Client %s : %s" % (self.id, message)
        if (message == 'base'):
            self.write_message(u"Base Directory: " + BASEDIR)
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
    tornado.ioloop.IOLoop.instance().start()
