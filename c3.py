# -*- coding: utf-8 -*-
import ssl
import socket

SSL_CERT_PERM = "/ssl/server.crt"

socket_file_path = "/tmp/myservice.sock"

sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
s = ssl.wrap_socket(sock,ca_certs=SSL_CERT_PERM,cert_reqs=ssl.CERT_REQUIRED,ssl_version=ssl.PROTOCOL_TLSv1)
s.connect(socket_file_path)
s.send("hello world!")
s.close()