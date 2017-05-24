"""
Server
"""

from threading import Thread
from socketserver import ThreadingMixIn
import socket
import ssl
import PrintStyle as ps

HOST = "localhost"
ALICE_PORT = 9001
BOB_PORT = 9002

class ClientThread(Thread):
    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print("New server socket thread started for " + ip + ":" + str(port))
    def run(self):
        while True:
            data = conn.recv(2048)
            print("Server received data:", data)
            MESSAGE = input("Multithreaded Python server : Enter Response from Server/Enter exit:")
            if MESSAGE == 'exit':
                break
            conn.send(MESSAGE.encode())  # echo 

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
    _thread.start_new_thread(connect_to_port(HOST, ALICE_PORT))
    _thread.start_new_thread(connect_to_port(HOST, BOB_PORT))

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
