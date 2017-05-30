"""
Inspired by:
http://www.andy-pearce.com/blog/posts/2016/Jul/the-state-of-python-coroutines-asyncio-callbacks-vs-coroutines/
"""

"""
To create certificates:

openssl req -x509 -newkey rsa:2048 -keyout selfsigned.key -nodes -out selfsigned.cert -sha256 -days 1000
"""

import asyncio
import ssl

class MyServer:

    def __init__(self, server_name, port, loop):
        self.server_name = server_name
        self.connections = {}

        socket_connection = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        socket_connection.load_cert_chain('selfsigned.cert', 'selfsigned.key')

        coro = asyncio.start_server(
            self.accept_connection, 'localhost', port, ssl=socket_connection, loop=loop)
        self.server = loop.run_until_complete(coro)

        print("Starting '" + self.server_name + "' on", self.server.sockets[0].getsockname())

    def broadcast(self, message):
        """
        Broadcast 'message' to all connected users
        """
        for reader, writer in self.connections.values():
            writer.write((message + "\n").encode("utf-8"))

    @asyncio.coroutine
    def prompt_username(self, reader, writer):
        while True:
            writer.write("Enter username: ".encode("utf-8"))
            data = (yield from reader.readline()).decode("utf-8")
            if not data:
                return None
            username = data.strip()
            if username and username not in self.connections:
                self.connections[username] = (reader, writer)
                return username
            writer.write("Sorry, that username is taken.\n".encode("utf-8"))

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
        writer.write(("Welcome to " + self.server_name + "\n").encode("utf-8"))
        username = (yield from self.prompt_username(reader, writer))
        if username is not None:
            self.broadcast("User %r has joined the room" % (username,))
            yield from self.handle_connection(username, reader)
            self.broadcast("User %r has left the room" % (username,))
        yield from writer.drain()


def main():

    loop = asyncio.get_event_loop()
    server = MyServer("Miner Server", 4455, loop)
    try:
        loop.run_forever()
    finally:
        loop.close()


if __name__ == "__main__":
    main()