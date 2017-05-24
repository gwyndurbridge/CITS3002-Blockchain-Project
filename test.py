#install openssl
#sudo aptitude install python-openssl

from OpenSSL import SSL
import socket, socketserver

class SSlSocketServer(socketserver.ThreadingMixIn, socketserver.TCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        socketserver.BaseServer.__init__(self, server_address,
            RequestHandlerClass)
        ctx = SSL.Context(SSL.SSLv3_METHOD)
        cert = 'cert.pem'
        key = 'private_key.pem'
        ctx.use_privatekey_file(key)
        ctx.use_certificate_file(cert)
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family,
            self.socket_type))
        if bind_and_activate:
            self.server_bind()
            self.server_activate()
    def shutdown_request(self,request):
        request.shutdown()

class Decoder(socketserver.StreamRequestHandler):
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)

    def handle(self):
        try:
            socket1 = self.connection
            str1 = socket1.recv(4096)
            print(str1)
        except socket.error:
            print('socket error')
def main():
    server = SSlSocketServer(('127.0.0.1', 9999), Decoder)
    server.serve_forever()
if __name__ == '__main__':
    main()



#now test server

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 9999))
sslSocket = socket.ssl(s)
print(repr(sslSocket.server()))
print(repr(sslSocket.issuer()))
sslSocket.write('Hello secure socket\n')
s.close()