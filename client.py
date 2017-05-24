"""
Client
"""

import socket
import ssl
import PrintStyle as ps

import pprint

def connect_to_port(host, port):
    """
    Create socket with port number
    """
    print("Connecting to: " + host + ":" + str(port))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(sock, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1_2)
    ssl_sock.connect((host, port))

    print(repr(ssl_sock.getpeername()))
    print(ssl_sock.cipher())
    print(pprint.pformat(ssl_sock.getpeercert()))

    ssl_sock.write("Hello world!".encode())

    ssl_sock.write("Test".encode())

    # while True:
        # ssl_sock.write("test".encode())
        # data = ssl_sock.read()
        # ssl_sock.close()

    # if False: # from the Python 2.7.3 docs
    #     # Set a simple HTTP request -- use httplib in actual code.
    #     ssl_sock.write("""GET / HTTP/1.0\r
    #     Host: www.verisign.com\n\n""")

    #     # Read a chunk of data.  Will not necessarily
    #     # read all the data returned by the server.
    #     data = ssl_sock.read()

    #     # note that closing the SSLSocket will also close the underlying socket
    #     ssl_sock.close()


def main():
    """
    Main function for client
    """
    print(ps.title("CITS3002 Client"))
    port = input("Please enter the PORT number you wish to use: ")
    if len(port) == 0:
        port = 9001 # default port
    connect_to_port("localhost", int(port))

if __name__ == '__main__':
    main()
