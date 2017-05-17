import socket, ssl, select
import printStyle as ps

# http://stackoverflow.com/questions/17539859/how-to-create-multi-server-sockets-on-one-client-in-python

def startServer():
    bindsocket = socket.socket()
    bindsocket.bind(('', 5009))
    bindsocket.listen(5) # (backlog) specifies the number of unaccepted connections that the system will allow before refusing new connections

    print("Starting server")
    print("Host address: " + socket.gethostname())
    # print("Sock address: " + bindsocket.getsockname()[0])

    def do_something(connstream, data):
        print("do_something:", data)
        return False

    def deal_with_client(connstream):
        data = connstream.read()
        while data:
            if not do_something(connstream, data):
                break
            data = connstream.read()

    while True:
        newsocket, fromaddr = bindsocket.accept()
        connstream = ssl.wrap_socket(newsocket,
                                    server_side=True,
                                    certfile="cert.pem")
        try:
            deal_with_client(connstream)
        finally:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()


def main():
    # Welcome message
    print("\n" + ps.moneyBag + ps.bold + ps.purple + "  CITS3002 SERVER " + ps.reset + ps.moneyBag + "\n")
    startServer()

if __name__ == '__main__':
    main()