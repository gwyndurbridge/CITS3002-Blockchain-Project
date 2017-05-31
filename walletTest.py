from client import Client
import PrintStyle as ps

def createClient(name):
    c = Client(name)
    print(c.name)

    loop = asyncio.get_event_loop()
    client = Client()
    asyncio.async(asyncio.async(client.connect()))
    try:
        loop.run_forever()
    loop.close()

def main():
    print(ps.title('CITS3002 Client'))

    client_name = input('client name: ')
    createClient(client_name)

main()
