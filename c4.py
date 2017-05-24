"""
Python TCP Client A
"""
import socket

# HOST = socket.gethostname()
HOST = ''
PORT = 2004
BUFFER_SIZE = 2000
MESSAGE = input("tcpClientA: Enter message/ Enter exit:")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    sock.send("Hi".encode())

    while MESSAGE != 'exit':
        sock.send(MESSAGE.encode())
        DATA = sock.recv(BUFFER_SIZE)
        print(" Client2 received data:", DATA)
        MESSAGE = input("tcpClientA: Enter message to continue/ Enter exit:")
 
# CLIENTA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# CLIENTA.connect((HOST, PORT))

