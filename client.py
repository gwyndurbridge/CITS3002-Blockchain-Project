import pprint
import socket
import ssl

import printStyle as ps

'''
init(name or pem file directory)
getBal() returns actual/available balance - split in two if you want
sendCoins(recipient, amountAvail, amountSent, amountChange) returns True if it was sent successfuly (maybe?)
        amountAvail = trans $$$ input
        amountSent = recipient $$$ received
        amountChange = sender $$$ received back
        you shouldn't need the sender's name as that should come from init()
        I'm happy to format this differently (i.e. as a dict or a json.dump() or a json) if you want
            but the values being inputted shouldn't need to change

I don't think I'll need to get anything else from the wallet.
Maybe a transaction history? that'd probably be an extension task if you want to implement it
    just pass it back as a list of strings (i.e. json.dump()?) that I can run through to print out
'''

def createSocket(host, port):
    print("Creating socket with: " + host + ":", port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_sock = ssl.wrap_socket(s, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)
    ssl_sock.connect((host, port))

    print(repr(ssl_sock.getpeername()))
    print(ssl_sock.cipher())
    print(pprint.pformat(ssl_sock.getpeercert()))

    ssl_sock.write("Test Message!".encode())

    if False:  # from the Python 2.7.3 docs
        # Set a simple HTTP request -- use httplib in actual code.
        ssl_sock.write("""GET / HTTP/1.0\r
        Host: www.verisign.com\n\n""")

        # Read a chunk of data.  Will not necessarily
        # read all the data returned by the server.
        data = ssl_sock.read()

        # note that closing the SSLSocket will also close the underlying socket
        ssl_sock.close()


def send(data):
    print("Attempting to send...")


def main():
    # Welcome message
    print("\n" + ps.MONEY_BAG + ps.BOLD + ps.PURPLE + " CITS3002 CLIENT " + ps.RESET + ps.MONEY_BAG + "\n")

    # Request the host and port number of the serverfrom the user
    host = input("Please enter the HOST address of the server: ")
    port = input("Please enter the PORT number you wish to use: ")

    # Use default values if no info is given
    if len(host) == 0:
        host = "127.0.0.1"  # localhost
    if len(port) == 0:
        port = 9999  # default port

    # Create the socket with the given user info
    createSocket(host, port)


if __name__ == '__main__':
    main()
