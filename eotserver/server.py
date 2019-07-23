"""
The EOT Server
"""
#!/usr/bin/python

import signal
import time
import uuid

from tornado import ioloop, web, websocket
from tornado.options import define, options, parse_command_line

define("port", default=1873, help="Run Socket Server on the given port", type=int)

MAX_WAIT = 1 #Seconds, before shutdown in signal

CLIENTS = dict() #List of all connections

def broadcast(message):
    """
    Pushes a message to all currently connected clients.
    Tests connection before hand just in case a disconnect
    has just occurred.
    """
    for ids, web_socket in list(CLIENTS.items()):
        if not web_socket.ws_connection.stream.socket:
            del CLIENTS[ids]
        else:
            web_socket.write_message(message)

def sig_handler(_sig, _frame):
    """
    Calls shutdown on the next I/O Loop iteration.
    Should only be used from a signal handler, unsafe otherwise.
    """
    ioloop.IOLoop.instance().add_callback_from_signal(shutdown)

def shutdown():
    """
    Graceful shutdown of all services.
    Can be called with kill -2 for example, a CTRL+C keyboard interrupt,
    or 'shutdown' from the debug console on the panel.
    """
    broadcast("EOT Server is shutting down.")
    print("Shutting down EOT server")
    print("(will wait up to %s seconds to complete running threads ...)" % MAX_WAIT)

    instance = ioloop.IOLoop.current()
    deadline = time.time() + MAX_WAIT

    def terminate():
        """
        Recursive method to wait for incomplete async callbacks and timeouts
        """
        now = time.time()
        if now < deadline:
            instance.add_timeout(now + 1, terminate)
        else:
            instance.stop()
            print("Shutdown.")
    terminate()


class IndexHandler(web.RequestHandler):
    """
    Serve up the panel
    """
    async def get(self):
        self.render("panel.html")

class WebSocketHandler(websocket.WebSocketHandler):
    """
    Descriptions of websocket interactions. What to do when connecting/disconnecting a client and how to handle a client message
    """
    def initialize(self):
        self.id = uuid.uuid4() #Give client a unique identifier.

    def open(self):
        self.stream.set_nodelay(True)
        CLIENTS[self.id] = self
        print("New Client: %s" % (self.id))
        self.write_message("Connected to EOT Server")
        self.write_message("6" + "&1") #Push initial status and assume acknowledgement.

    def on_message(self, message):
        print("Message from Client %s: %s" % (self.id, message))

        commands = message.split("&") #complex commands will be of the form command&command&command

        if message == 'shutdown':
            self.write_message("Shutting down EOT Server...")
            ioloop.IOLoop.instance().add_callback(shutdown)
        elif len(commands) > 1:
            if commands[0] == 'Accept':
                self.write_message("Accepted state: " + commands[1])
                broadcast(commands[1] + '&3')
            elif commands[0] == 'Broadcast':
                self.write_message("Send state: " + commands[1])
                broadcast(commands[1])

        else:
            self.write_message("Server echoed: " + message)

    def on_close(self):
        print("Client %s disconnected." % self.id)
        if self.id in CLIENTS:
            del CLIENTS[self.id]

def make_app():
    """
    Builds initial application service
    """
    return web.Application([
        (r'/', IndexHandler),
        (r'/websocket', WebSocketHandler),
        (r'/(favicon.ico)', web.StaticFileHandler, {'path': ''},),
        (r'/static/(.*)', web.StaticFileHandler, {'path': './static'},),
    ])

if __name__ == '__main__':
    #Set up server
    parse_command_line()
    APP = make_app()
    APP.listen(options.port)

    #Signal Register
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    #Start the server main loop
    ioloop.IOLoop.instance().start()
