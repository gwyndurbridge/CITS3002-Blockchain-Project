from miner import Miner
from Wallet import Wallet
from networkclient import NetworkClient

import asyncio
import ssl

"""
background stuff: http://www.curiousefficiency.org/posts/2015/07/asyncio-background-calls.html
"""

# import itertools, time
# def tick_5_sync():
#     for i in range(5):
#         print(i)
#         time.sleep(1)
#     print("Finishing")

def call_in_background(target, *, loop=None, executor=None):
    if loop is None:
        loop = asyncio.get_event_loop()
    if callable(target):
        return loop.run_in_executor(executor, target)
    raise TypeError("target must be a callable, "
                    "not {!r}".format(type(target)))

class Client:
    def __init__(self, name):
        """
        name: (string) wallet name
        """
        self.name = name

        print("init")
        #Empty wallet and miner objects
        self.wallet = None
        self.miner = None

        if name == "miner":
            #starting as miner
            self.init_miner()
        else:
            #startign as miner
            self.init_wallet()

    """
    Wallet related functions
    """

    def init_wallet(self):
        print("Initialising wallet as %r" % (self.name))
        self.wallet = Wallet(self.name)
        nc = NetworkClient(self.name)



    def check_balance(self):
        """
        total, pending
        """
        return (50,20)

    def send_transaction(self, receiver, value, payment, change):
        """
        reciever: (string) name of receiver
        value: (number) total amount to send from wallet
        payment: (number) how much the receiver recieves
        change: (number) how much the sender recieves

        Returns (string) message to print in CLI
        """
        return "Success"


    """
    Miner related functions
    """

    def init_miner(self):
        self.miner = Miner()
        return

#     def start_miner(self):
#         """
#         Returns (string) message to print in CLI
#         """
#         return "Success"

    def get_miner_difficulty(self):
        """
        Returns (Number) difficulty that miner is set to
        """
        return 35

    def set_miner_difficulty(self, difficulty):
        """
        Returns (Number) difficulty that miner is set to
        """
        return "Successfully set difficulty to " + str(difficulty)
