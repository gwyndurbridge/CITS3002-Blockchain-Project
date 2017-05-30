import asyncio
import ssl


@asyncio.coroutine
def handle_client(reader, writer):
    data = yield from reader.read(100)
    print(data)
    writer.write(b'bye')
    yield from writer.drain()
    writer.close()


@asyncio.coroutine
def client(addr, ssl_ctx):
    reader, writer = yield from asyncio.open_connection(*addr, ssl=ssl_ctx)
    writer.write(b'hello')
    data = yield from reader.read(100)
    print(data)
    writer.close()

# addr = ('127.0.0.1', 5555)
addr = ('localhost', 5555)
loop = asyncio.get_event_loop()

# Setup server
server_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
server_ctx.load_cert_chain('selfsigned.cert', 'selfsigned.key')
coro = asyncio.start_server(handle_client, *addr, ssl=server_ctx)
server = loop.run_until_complete(coro)

# Run client
client_ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='selfsigned.cert')
client_ctx.check_hostname = True
client_ctx.load_cert_chain('selfsigned.cert', 'selfsigned.key')

loop.run_until_complete(client(addr, client_ctx))

# Shutdown
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
