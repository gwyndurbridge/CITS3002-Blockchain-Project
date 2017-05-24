 #!/bin/python
# -*- coding: utf-8 -*-
import os
import ssl
import socket
import socketserver

socket_file_path = "/tmp/myservice.sock"

LISTEN_FDS = int(os.environ.get("LISTEN_FDS", 0))
LISTEN_PID = os.environ.get("LISTEN_PID", None) or os.getpid()

SSL_CERT_PERM = "/ssl/server.crt"
SSL_KEY_PERM = "/ssl/server.key"

class MyRequestHandler(socketserver.BaseRequestHandler):
    """Handle request from client"""
    def handle(self):
        data = self.request.recv(1024).strip()
        print(str(data))

class UnixServer(socketserver.UnixStreamServer):

    def server_bind(self):
        print("LISTEN_FDS: "+str(LISTEN_FDS))
        print("LISTEN_PID: "+str(LISTEN_PID))
        if LISTEN_FDS == 0:
            print("create new socket")
            socketserver.UnixStreamServer.server_bind(self)
        else:
            print("rebind socket")
            print("address_family: "+str(self.address_family))
            print("socket_type: "+str(self.socket_type))
            sock = socket.fromfd(3, self.address_family, self.socket_type)
            # //stackoverflow.com/a/16740536
            self.socket = socket.socket(_sock=sock)

    def get_request(self):
        newsocket, fromaddr = self.socket.accept()
        connstream = ssl.wrap_socket(newsocket,
                                        server_side=True,
                                        certfile = SSL_CERT_PERM,
                                        keyfile = SSL_KEY_PERM,
                                        ssl_version = ssl.PROTOCOL_TLSv1,
                                        do_handshake_on_connect=False)
        return connstream, fromaddr

server = UnixServer(socket_file_path, MyRequestHandler)

try:
    print("start server!")
    server.serve_forever()
except KeyboardInterrupt:
    print("googbye!")
    server.shutdown()
    os.remove(socket_file_path)