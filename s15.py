import asyncio
import ssl


class MyServer:
    """
    The class which controls the networking server
    """
    def __init__(self, is_server, port, loop):
        if is_server:
            self.connections = {}

            sc = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            sc.load_cert_chain('selfsigned.cert', 'selfsigned.key')

            coro = asyncio.start_server(self.accept_connection, 'localhost', port, ssl=sc, loop=loop)
            self.server = loop.run_until_complete(coro)

            print('Serving on {}'.format(self.server.sockets[0].getsockname()))
        else:
            print("running as client...")
            sc = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='selfsigned.cert')

    @asyncio.coroutine
    def accept_connection(self, reader, writer):
        """
        new connection to server
        """
        writer.write(b'Welcome!')
        # writer.write(("Welcome! You are connected to " + self.server.sockets[0].getsockname() + "\n").encode("utf-8"))
        username = (yield from self.prompt_username(reader, writer))
        if username is not None:
            self.broadcast("User %r has joined the room" % (username,))
            yield from self.handle_connection(username, reader)
            self.broadcast("User %r has left the room" % (username,))
        yield from writer.drain()

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

    def broadcast(self, message):
        for reader, writer in self.connections.values():
            writer.write((message + "\n").encode("utf-8"))

def startServer():
    print("Starting as server")
    loop = asyncio.get_event_loop()
    server = MyServer(4455, loop)
    try:
        loop.run_forever()
    finally:
        loop.close()



# @asyncio.coroutine
# def tcp_echo_client(loop):
#     print("client thing")
#     SC = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='selfsigned.cert')
#     port = 4455
#     reader, writer = yield from asyncio.open_connection('localhost', port, ssl=SC, loop=loop)
#     writer.write(b'ping\n')
#     yield from writer.drain()
#     data = yield from reader.readline()
#     # assert data == b'pong\n', repr(data)
#     print("Client received {!r} from server".format(data))
#     writer.close()
#     print('Client done')

def startClient():
    print("Starting as client")
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(tcp_echo_client(loop))
    # loop.run_forever()


def getTask():
    task = input("Server or Client? (use s or c)")
    if task == 's':
        startServer()
    elif task == 'c':
        startClient()
    else:
        getTask()

def main():
    getTask()

if __name__ == "__main__":
    main()
