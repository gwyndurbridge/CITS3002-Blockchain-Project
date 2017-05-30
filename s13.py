import asyncio
import ssl

PORT = 9000

class MyServer:
    """
    The class which controls the networking server
    """
    def __init__(self, port, loop):
        self.connections = {}
        self.server = loop.run_until_complete(
            asyncio.start_server(self.accept_connection, "", port, loop=loop))
    
def main(argv):
    loop = asyncio.get_event_loop()
    server = MyServer("Test Server", 4455, loop)
    try:
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    main()
