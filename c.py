import asyncio
import ssl

class Client:
    reader = None
    writer = None
    sockname = None

    def __init__(self, name):
        self.name = name
        self.host = 'localhost'
        self.port = 9696

    def send_msg(self, msg):
        msg = '{}\n'.format(msg).encode()
        self.writer.write(msg)

    @asyncio.coroutine
    def register_name(self):
        mainloop = asyncio.get_event_loop()
        mainloop.call_soon_threadsafe(self.send_msg, self.name)

    def message_received(self, msg):
        print("RECEIVED:",msg)

    @asyncio.coroutine
    def connect(self):
        try:
            sc = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='certs/selfsigned.cert')
            reader, writer = yield from asyncio.open_connection(self.host, self.port, ssl=sc)
            asyncio.async(self.register_name())
            
            self.reader = reader
            self.writer = writer
            self.sockname = writer.get_extra_info('sockname')
            while not reader.at_eof():
                msg = yield from reader.readline()
                if msg:
                    decoded = '{}'.format(msg.decode().strip())
                    self.message_received(decoded)
            print('ERROR: Server disconnected')
            self.writer = None
        except ConnectionRefusedError as e:
            print('Connection refused: {}'.format(e))
            self.close()

def main():
    loop = asyncio.get_event_loop()
    client = Client("bob")

    # asyncio.async(client.connect())


    asyncio.async(asyncio.async(client.connect()))
    try:
        print("here1")
        loop.run_forever()
        print("here2")
    finally:
        loop.close()
    print("can i run some stuff?")


if __name__ == '__main__':
    main()