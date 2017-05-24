import logging, socket, ssl, sys, time, threading

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-4s %(threadName)s %(message)s", 
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)

def test_handler(conn):
    logging.info("sleeping 1 second")
    time.sleep(1)
    conn.send("done sleeping\n")
    return 0


class ClientThread(threading.Thread):
    def __init__(self, connstream):
        threading.Thread.__init__(self)
        self.conn = connstream        

    def run(self):
        test_handler(self.conn)

def main():
    port = 10023
    bindsocket = socket.socket()
    bindsocket.bind(('0.0.0.0', port))
    bindsocket.listen(10)

    logging.info('listening on port %d', port)
    while True:
        newsocket, fromaddr = bindsocket.accept()
        logging.info('connect from %s', fromaddr)
        connstream = newsocket
        if 0:
            connstream = ssl.wrap_socket(
                newsocket,
                server_side=True,
                certfile="server.crt",
                keyfile="server.key",
                ssl_version=ssl.PROTOCOL_TLSv1)
        ClientThread(connstream).start()

    logging.info('stop')

if __name__=='__main__':
    main()

    # make sure all threads are done
    for th in threading.enumerate():
        if th != threading.current_thread():
            th.join()