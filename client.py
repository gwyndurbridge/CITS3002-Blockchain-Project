import socket, ssl, pprint

class printStyle:
    moneyBag = u"\U0001F4B0"
    bold = "\033[1m"
    purple = "\033[95m"
    reset = "\033[0m"

def createSocket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(s,
                            ca_certs="cert.pem",
                            cert_reqs=ssl.CERT_REQUIRED)
    ssl_sock.connect((host, 5009))

    print(repr(ssl_sock.getpeername()))
    print(ssl_sock.cipher())
    print(pprint.pformat(ssl_sock.getpeercert()))

    ssl_sock.write("Test Message!".encode())

    if False: # from the Python 2.7.3 docs
        # Set a simple HTTP request -- use httplib in actual code.
        ssl_sock.write("""GET / HTTP/1.0\r
        Host: www.verisign.com\n\n""")

        # Read a chunk of data.  Will not necessarily
        # read all the data returned by the server.
        data = ssl_sock.read()

        # note that closing the SSLSocket will also close the underlying socket
        ssl_sock.close()

def main():
    # Welcome message
    print("\n" + printStyle.moneyBag + printStyle.bold + printStyle.purple + " CITS3002 CLIENT " + printStyle.reset + printStyle.moneyBag + "\n")
    
    # Request the host and port number of the serverfrom the user
    host = input("Please enter the HOST address of the server: ")
    port = input("Please enter the PORT number you wish to use: ")
    
    # Use default values if no info is given
    if len(host)==0:
        host = "127.0.0.1" # localhost
    if len(port) == 0:
        port = 5009 # default port
    
    # Create the socket with the given user info
    createSocket(host, port)

if __name__ == '__main__':
    main()