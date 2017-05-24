import socketserver
import ssl


# class MyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
#     def server_bind(self):
#         """
#         Handle the server bind
#         We want to 'wrap' the socket but not accept the handshake until the connection is accepted
#         """
#         socketserver.TCPServer.server_bind(self)
#         # self.socket = ssl.wrap_socket(
#         #     self.socket, server_side=True, certfile="cert.pem",
#         #     do_handshake_on_connect=False)
#         self.socket = ssl.wrap_socket(
#             self.socket,
#             server_side=True, certfile="cert.pem",
#             do_handshake_on_connect=False,
#             ssl_version=ssl.PROTOCOL_TLSv1)
#     def get_request(self):
#         """
#         Handle the request
#         We want to handshake on request
#         """
#         (socket, addr) = socketserver.TCPServer.get_request(self)
#         socket.do_handshake()
#         return (socket, addr)


class MyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def get_request(self):
        (socket, addr) = socketserver.TCPServer.get_request(self)
        return (ssl.wrap_socket(socket, server_side=True, certfile="cert.pem", ssl_version=ssl.PROTOCOL_TLSv1_2), addr)

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        print(str(self.request.recv(1024),'utf-8'))
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9997

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()




# class MySSL_TCPServer(TCPServer):
#     def __init__(self,
#                  server_address,
#                  RequestHandlerClass,
#                  certfile,
#                  keyfile,
#                  ssl_version=ssl.PROTOCOL_TLSv1,
#                  bind_and_activate=True):
#         TCPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
#         self.certfile = certfile
#         self.keyfile = keyfile
#         self.ssl_version = ssl_version

#     def get_request(self):
#         newsocket, fromaddr = self.socket.accept()
#         connstream = ssl.wrap_socket(newsocket, server_side=True, certfile="cert.pem")
#         return connstream, fromaddr

# class MySSL_ThreadingTCPServer(ThreadingMixIn, MySSL_TCPServer): pass

# class testHandler(StreamRequestHandler):
#     def handle(self):
#         data = self.connection.recv(4096)
#         self.wfile.write(data)
# #test code
# MySSL_ThreadingTCPServer(('127.0.0.1',9999),testHandler,"cert.pem","key.pem").serve_forever()
