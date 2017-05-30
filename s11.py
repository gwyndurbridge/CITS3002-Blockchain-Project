"""
https://gist.github.com/messa/22398173f039d1230e32
https://docs.python.org/3/library/multiprocessing.html#module-multiprocessing

http://www.giantflyingsaucer.com/blog/?p=5557
"""

import asyncio
import multiprocessing
import os
import ssl
from time import sleep

port = 9000

def startServer():
    print("Starting as server")
    q = multiprocessing.Queue()
    data = [5, 10, 13, -1]
    assert os.path.isfile('selfsigned.cert')
    server_process = multiprocessing.Process(target=server, name='server',args=(data, q))
    server_process.start()
    print("process name: ", server_process.name)
    queue_process = multiprocessing.Process(target=myqueue, name='myqueue',args=(q,))
    queue_process.start()
    print("process name: ", queue_process.name)
    
        
def startClient():
    print("Starting as client")
    assert os.path.isfile('selfsigned.cert')
    client_process = multiprocessing.Process(target=client, name='client')
    client_process.start()
    try:
        print("trying")
        client_process.join(1)
        assert not client_process.is_alive()
    finally:
        print("finally")
        client_process.terminate()
        client_process.join()

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

def server(data, q):

    # print('data: ', data)
    # print("queue: ", q.get())


    @asyncio.coroutine
    def handle_connection(reader, writer):
        """
        handle correction
        """
        addr = writer.get_extra_info('peername')
        data = yield from reader.readline()
        q.put([{"data":data}])
        print("Server received {!r} from {}".format(data, addr))
        assert data == b'ping\n', repr(data)
        writer.write(b'pong\n')
        yield from writer.drain()
        writer.close()
        print('Server done')

    sc = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sc.load_cert_chain('selfsigned.cert', 'selfsigned.key')

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_connection, 'localhost', port, ssl=sc, loop=loop)
    server = loop.run_until_complete(coro)

    print('Serving on {}'.format(server.sockets[0].getsockname()))
    loop.run_forever()


def client():
    print("something1")

    @asyncio.coroutine
    def tcp_echo_client(loop):
        print("something2")
        SC = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='selfsigned.cert')

        reader, writer = yield from asyncio.open_connection('localhost', port, ssl=SC, loop=loop)
        writer.write(b'ping\n')
        yield from writer.drain()
        data = yield from reader.readline()
        assert data == b'pong\n', repr(data)
        print("Client received {!r} from server".format(data))
        writer.close()
        print('Client done')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client(loop))
    loop.close()

def myqueue(q):

    @asyncio.coroutine
    def check_queue(q, loop):
        """
        check queue
        """
        print("QUEUE:", q.get())

    loop = asyncio.get_event_loop()
    # coro = asyncio.check_queue(check_queue(q, loop))
    loop.run_forever(check_queue(q, loop))

    print("Starting queue checker...")
    loop.run_forever()

if __name__ == '__main__':
    main()