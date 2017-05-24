import socket, ssl, select
import printStyle as ps

# Dictionary of all sock connections
# Key: Public Key
# Object: Socket object
# socks = {}
# poll = select.poll()

# http://stackoverflow.com/questions/17539859/how-to-create-multi-server-sockets-on-one-client-in-python

# def startMultipleSevers():
#     sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     socks[sock1.fileno()] = sock1
#     poll = select.poll()
#     for sock in socks:
#         poll.register(sock)
#     while 1:
#         fd, event = poll.poll() # Optional timeout parameter in seconds
#         sock = socks[fd]
#         sock.recv(1024) # Do stuff


# def startServerOLD():
#     bindsocket = socket.socket()
#     bindsocket.bind(('', 5009))
#     bindsocket.listen(5) # (backlog) specifies the number of unaccepted connections that the system will allow before refusing new connections

#     print("Sock fileno: ", bindsocket.fileno())
#     print("Starting server")
#     print("Host address: " + socket.gethostname())
#     # print("Sock address: " + bindsocket.getsockname()[0])

#     def do_something(connstream, data):
#         print("do_something:", data)
#         return False

#     def deal_with_client(connstream):
#         data = connstream.read()
#         while data:
#             if not do_something(connstream, data):
#                 break
#             data = connstream.read()

#     while True:
#         newsocket, fromaddr = bindsocket.accept()
#         connstream = ssl.wrap_socket(newsocket,
#                                     server_side=True,
#                                     certfile="cert.pem")
#         try:
#             deal_with_client(connstream)
#         finally:
#             connstream.shutdown(socket.SHUT_RDWR)
#             connstream.close()

def sendTo(someone):
    return

def sendToAll():
    return

def addSocket(port):
    print("Adding socket to port: ", port)
    sock = socket.socket()
    sock.bind(('',port))
    sock.listen(5)

    socks[sock.fileno()] = sock
    # poll = select.poll()
    poll.register(sock)
    print("socket added?")

def startServer():
    print("Starting server...")

    def do_something(connstream, data):
        print("do_something:", data)
        return False

    def deal_with_client(connstream):
        data = connstream.read()
        while data:
            if not do_something(connstream, data):
                break
            data = connstream.read()
    
    print("did i get here?")



    while True:
        print("hi")
        #fd, event = poll.poll() # Optional timeout parameter in seconds
        fd, event = poll.poll()[0]
        print("fd: ", fd)
        sock = socks[fd]
        
        newsocket, fromaddr = sock.accept()
        # stuff = sock.recv(1024) # Do stuff
        # print("stuff?: ", stuff)
        connstream = ssl.wrap_socket(sock,server_side=True,certfile="cert.pem")
        try:
            print("dealing with stream")
            deal_with_client(connstream)
        finally:
            print("finally of try reached")
            # connstream.shutdown(socket.SHUT_RDWR)
            # connstream.close()

def main():
    # Welcome message
    print("\n" + ps.moneyBag + ps.bold + ps.purple + "  CITS3002 SERVER " + ps.reset + ps.moneyBag + "\n")
    
    # startServer()

    addSocket(9999)
    startServer()

if __name__ == '__main__':
    main()