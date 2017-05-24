import socket
import sys
import ssl

HOST, PORT = "localhost", 9997
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

    ssl_sock = ssl.wrap_socket(sock, certfile="cert.pem", cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_TLSv1_2)
    ssl_sock.connect((HOST, PORT))
    ssl_sock.write("Hi".encode())
    ssl_sock.sendall("Hello".encode())
    ssl_sock.sendall(bytes(data + "\n", "utf-8"))
    received = str(ssl_sock.recv(1024), "utf-8")

    # Connect to server and send data
    # sock.connect((HOST, PORT))
    # sock.sendall(bytes(data + "\n", "utf-8"))

    # Receive data from the server and shut down
    # received = str(sock.recv(1024), "utf-8")

print("Sent:     {}".format(data))
print("Received: {}".format(received))


# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ssl_sock = ssl.wrap_socket(s,
#                            ca_certs="cert.pem",
#                            cert_reqs=ssl.CERT_REQUIRED,
#                            ssl_version=ssl.PROTOCOL_TLSv1)
# ssl_sock.connect(('127.0.0.1',9999))
# ssl_sock.send('hello ~MySSL !')
# print(ssl_sock.recv(4096))
# ssl_sock.close()