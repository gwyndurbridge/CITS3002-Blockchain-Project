"""
Server

https://docs.python.org/3/library/socketserver.html



http://stackoverflow.com/questions/8582766/adding-ssl-support-to-socketserver
http://stackoverflow.com/questions/6001644/tcp-server-over-ssl-using-socketserver-tcpserver
"""

import socket
import ssl
import PrintStyle as ps
import threading
# import socketserver

class ClientThread(threading.Thread):


    def connect_to_port(self, host, port):
        """
        Create socket for desired host and port
        """
        print("Connecting to port:", port)

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.bind((host, port))
        except socket.error:
            print("Bind failed.")
        # (backlog) specifies the number of unaccepted connections that the
        # system will allow before refusing new connections
        sock.listen(5)
        newsocket, fromaddr = sock.accept()
        print("Accepted connection with address: ")
        # print("Sock fileno: ", sock.fileno())
        # print("Starting server")
        # print("Host address: " + socket.gethostname())
        # print("Sock address: " + sock.getsockname()[0])
        try:
            connstream = ssl.wrap_socket(newsocket, server_side=True, certfile="cert.pem")
            print("Socket succeeded")
        except socket.error:
            print("SSL wrap failed")
        while True:
            data = connstream.recv(1024)
            if data:
                print("data recieved: " + str(data))

    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        print("[+] New thread started for " + host + ":" + str(port))
        connect_to_port(host, port)

    def run(self):    
        print("Running")

    


HOST = "localhost"
ALICE_PORT = 9001
BOB_PORT = 9002

def connect_to_port(host, port):
    """
    Create socket for desired host and port
    """
    print("Connecting to port:", port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.bind((host, port))
    except socket.error:
        print("Bind failed.")
    # (backlog) specifies the number of unaccepted connections that the
    # system will allow before refusing new connections
    sock.listen(5)
    newsocket, fromaddr = sock.accept()
    print("Accepted connection with address: ")
    # print("Sock fileno: ", sock.fileno())
    # print("Starting server")
    # print("Host address: " + socket.gethostname())
    # print("Sock address: " + sock.getsockname()[0])
    try:
        connstream = ssl.wrap_socket(newsocket, server_side=True, certfile="cert.pem")
        print("Socket succeeded")
    except socket.error:
        print("SSL wrap failed")
    while True:
        data = connstream.recv(1024)
        if data:
            print("data recieved: " + str(data))

def start_server():
    """
    Create sockets required for server
    """
    # _thread.start_new_thread(connect_to_port(HOST, ALICE_PORT))
    # _thread.start_new_thread(connect_to_port(HOST, BOB_PORT))

    thread1 = ClientThread(HOST, ALICE_PORT)
    thread2 = ClientThread(HOST, BOB_PORT)
    thread1.start()
    thread2.start()


    # alice_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.socket()
    # try:
    #     alice_sock.bind((HOST, ALICE_PORT))
    # except socket.error:
    #     print("Bind failed.")
    # # (backlog) specifies the number of unaccepted connections that the
    # # system will allow before refusing new connections
    # alice_sock.listen(5)
    # newsocket, fromaddr = alice_sock.accept()
    # print("Accepted connection with address: ")

    # print("Sock fileno: ", alice_sock.fileno())
    # print("Starting server")
    # print("Host address: " + socket.gethostname())
    # print("Sock address: " + alice_sock.getsockname()[0])

    # def do_something(connstream, data):
    #     print("do_something:", data)
    #     return False

    # def deal_with_client(connstream):
    #     data = connstream.read()
    #     while data:
    #         if not do_something(connstream, data):
    #             break
    #         data = connstream.read()

    # while True:
    #     newsocket, fromaddr = alice_sock.accept()
    #     connstream = ssl.wrap_socket(newsocket, server_side=True, certfile="cert.pem")
        
        
    #     try:
    #         deal_with_client(connstream)
    #     finally:
    #         print("Finally?")
    #         # connstream.shutdown(socket.SHUT_RDWR)
    #         # connstream.close()

def main():
    """
    Main function for server
    """
    print(ps.title("CITS3002 Server"))

    try:
        ip_address = socket.gethostbyname(HOST)
        print("IP = " + ip_address)
    except socket.gaierror:
        print("Host name could not be resolved")

    print("Starting server at: ")
    start_server()

if __name__ == '__main__':
    main()
