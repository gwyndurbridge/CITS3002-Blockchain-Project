"""
Inspired by:
http://www.andy-pearce.com/blog/posts/2016/Jul/the-state-of-python-coroutines-asyncio-callbacks-vs-coroutines/
"""

"""
To create certificates:

openssl req -x509 -newkey rsa:2048 -keyout selfsigned.key -nodes -out selfsigned.cert -sha256 -days 1000
with common name being the host (localhost is default)
"""

import asyncio
import ssl
import json

class MyServer:

    def __init__(self, server_name, port, loop):
        self.server_name = server_name
        self.connections = {}

        socket_connection = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        socket_connection.load_cert_chain('certs/selfsigned.cert', 'certs/selfsigned.key')

        coro = asyncio.start_server(
            self.accept_connection, 'localhost', port, ssl=socket_connection, loop=loop)
        self.server = loop.run_until_complete(coro)

        print("Starting '" + self.server_name + "' on", self.server.sockets[0].getsockname())


    def wrap_message(self, sender, message):
        wrapped = {
            'sender':sender,
            'message':message
        }
        return json.dumps(wrapped).encode()

    def broadcast(self, message):
        """
        Broadcast 'message' to all connected users
        """
        for reader, writer in self.connections.values():
            writer.write((message + "\n").encode("utf-8"))

    @asyncio.coroutine
    def prompt_username(self, reader, writer):
        while True:
            data = (yield from reader.readline()).decode()
            if not data:
                return None
            username = data.strip()
            if username and username not in self.connections:
                self.connections[username] = (reader, writer)
                return username
            writer.write("ERROR: Username already taken.\n".encode("utf-8"))

    @asyncio.coroutine
    def handle_connection(self, username, reader):
        while True:
            data = (yield from reader.readline()).decode("utf-8")
            if not data:
                del self.connections[username]
                return None
            self.broadcast(username + ": " + data.strip())

    @asyncio.coroutine
    def accept_connection(self, reader, writer):
        writer.write(self.wrap_message("Miner", "Successfully connected to '" + self.server_name + "'"))
        writer.write("\n".encode())
        username = (yield from self.prompt_username(reader, writer))
        if username is not None:
            print("-> User %r has connected" % (username))
            yield from self.handle_connection(username, reader)
            print("-> User %r has disconnected" % (username))
        yield from writer.drain()


def main():
    loop = asyncio.get_event_loop()
    server = MyServer("Miner Server", 9696, loop)
    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == "__main__":
    main()
