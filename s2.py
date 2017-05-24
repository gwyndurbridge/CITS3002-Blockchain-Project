#!/usr/bin/env python
 
# Copyright (C) 2012  Biggie
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
 
 
import socket
import socketserver
import threading
 
from OpenSSL import SSL
 
 
 
class MyRequestHandler(socketserver.StreamRequestHandler):
    """The MyRequestHandler-class is used to handle a client in
   its own thread"""
 
    def setup(self):
        """setup is called to set up the new client connection."""
        # ----
        # Instead of using socketserver.StreamRequestHandler.setup(self):
        #   self.connection = self.request
        #   self.rfile = self.connection.makefile('rb', self.rbufsize)
        #   self.wfile = self.connection.makefile('wb', self.wbufsize)
        # Use the following (because of ssl-usage):
        # ----
        if self.server.use_ssl:
            self.connection = self.request
            self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
            self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)
        else:
            socketserver.StreamRequestHandler.setup(self)
 
        # The connection-lock is used to prevent closing the connection
        # while data is written
        self.connection_lock = threading.Lock()
        self.write_lock = threading.Lock()
        self.connected = True
 
    def finish(self):
        """finish is called if the connection to the client is closed."""
        with self.connection_lock:
            socketserver.StreamRequestHandler.finish(self)
            self.connected = False
 
    def readline(self):
        """Read a new line from the client.socket.
 
       Returns an empty string if an error occurred or the socket was
       closed.
       """
        line = ""
        if self.connected and not self.rfile.closed:
            try:
                line = self.rfile.readline()
            except socket.error:
                print('error occurred while reading:')
            except SSL.SysCallError:
                pass
            except SSL.Error:
                pass  # maybe client does not use ssl
        return line
 
    def write(self, data):
        """Write data to the client-socket.
 
       data -- the data to send
       """
        with self.connection_lock:
            if self.connected:
                # only 1 write at a time
                with self.write_lock:
                    if not self.wfile.closed:
                        try:
                            self.wfile.write(data)
                        except socket.error:
                            print('error occurred while writing:')
 
    def handle(self):
        """handle is called to handle the new client."""
        while True:
            # self.rfile is a file-like object created by the handler
            request = self.readline().strip()
 
            if request == '':
                return
 
            # act like an echo server
            self.write(request + '\n')
 
 
 
class MyThreadedTCPServer(socketserver.ThreadingMixIn,
                                socketserver.TCPServer):
    """The MyThreadedTCPServer is the TCP-server and handles each client in its
   own thread."""
 
    def __init__(self, certfile, server_address, RequestHandlerClass,
                    bind_and_activate=True):
        """Initialize the MyThreadedTCPServer.
       
       certfile        -- The cert-file which should be used for SSL
                          sockets. If None, no SSL-sockets will be used.
       server_address, RequestHandlerClass, bind_and_activate
                       -- see socketserver.TCPServer.__init__
       """
        self.daemon_threads = True  # kill threads when server stops
        self.client_lock = threading.Lock()
 
        # if cert-file is present then use ssl
        if certfile is None:
            self.use_ssl = False
            socketserver.TCPServer.__init__(self, server_address,
                                        RequestHandlerClass, bind_and_activate)
        else:
            self.use_ssl = True
            # Code taken from socketserver.TCPServer.__init__
            # and added ssl-support:
            socketserver.BaseServer.__init__(self, server_address,
                                                RequestHandlerClass)
            ctx = SSL.Context(SSL.SSLv23_METHOD)
            # cert.pem-file containing the server private key and certificate
            cert = certfile
            ctx.use_privatekey_file(cert)
            ctx.use_certificate_file(cert)
            self.socket = SSL.Connection(ctx, socket.socket(self.address_family,
                                                            self.socket_type))
            if bind_and_activate:
                self.server_bind()
                self.server_activate()
 
    def shutdown_request(self,request):
        request.shutdown()
 
 
 
class MyTCPServer:
    """The MyTCPServer ecapsulates the TCP-server and can be used to start and
   stop the server."""
 
    def __init__(self, host, port, certfile=None):
        """Initialize the MyTCPServer.
 
       host        -- The host-address of the server.
       port        -- The port to bind the server to.
       certfile -- The cert-file to use when using SSL-sockets.
       """
        self.host = host
        self.port = port
 
        self.server = MyThreadedTCPServer(certfile, (self.host, self.port),
                                                MyRequestHandler)
 
    def start(self):
        """Start the server."""
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=self.server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = False
        server_thread.start()
 
    def stop(self):
        """Stop the server."""
        self.server.shutdown()
 
 
 
if __name__ == "__main__":
    # EXAMPLE-Code
 
    server = MyTCPServer('localhost', 9999, '/home/biggie/foruse.cer')
    server.start()
 
    import time
    time.sleep(30)
 
    server.stop()