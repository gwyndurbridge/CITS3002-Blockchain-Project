class Client:
    def __init__(self, name, is_miner):
        """
        name: (string) wallet name
        is_miner: (boolean) is client for miner
        """
        self.name = name
        self.is_miner = is_miner

    """
    Wallet related functions
    """

    def check_balance(self):
        """
        total, pending (leftover unprocessed i.e. total = 50, sent (unprocessed) = 30 therefore pending = 20)
        """
        return (50, 20)

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

    def start_miner(self):
        """
        Returns (string) message to print in CLI
        """
        return "Success"

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


c = Client("alice", False)
print(c.set_miner_difficulty(22))
