import asyncio
import ssl

def watch_stdin():
    msg = input()
    return msg


class Client:
    reader = None
    writer = None
    sockname = None

    def __init__(self, host='localhost', port=4455):
        self.host = host
        self.port = port

    def send_msg(self, msg):
        msg = '{}\n'.format(msg).encode()
        self.writer.write(msg)

    def close(self):
        print('Closing.')
        if self.writer:
            self.send_msg('close()')
        mainloop = asyncio.get_event_loop()
        mainloop.stop()

    @asyncio.coroutine
    def create_input(self):
        while True:
            mainloop = asyncio.get_event_loop()
            future = mainloop.run_in_executor(None, watch_stdin)
            input_message = yield from future
            if input_message == 'close()' or not self.writer:
                self.close()
                break
            elif input_message:
                mainloop.call_soon_threadsafe(self.send_msg, input_message)

    @asyncio.coroutine
    def connect(self):
        print('Connecting...')
        try:
            sc = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='selfsigned.cert')
            reader, writer = yield from asyncio.open_connection(self.host, self.port, ssl=sc)

            # reader, writer = yield from asyncio.open_connection(self.host, self.port)
            asyncio.async(self.create_input())
            self.reader = reader
            self.writer = writer
            self.sockname = writer.get_extra_info('sockname')
            while not reader.at_eof():
                msg = yield from reader.readline()
                if msg:
                    print('{}'.format(msg.decode().strip()))
            print('The server closed the connection, press <enter> to exit.')
            self.writer = None
        except ConnectionRefusedError as e:
            print('Connection refused: {}'.format(e))
            self.close()


def main():
    loop = asyncio.get_event_loop()
    client = Client()
    asyncio.async(asyncio.async(client.connect()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        # Raising and going through a keyboard interrupt will not interrupt the Input
        # So, do not stop using ctrl-c, the program will deadlock waiting for watch_stdin()
        print('Got keyboard interrupt <ctrl-C>, please send "close()" to exit.')
        loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()
