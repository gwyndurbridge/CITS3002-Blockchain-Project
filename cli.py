import json
import os
import re

# import Wallet
# import miner
base = "0"
green = "0;32;0"
purple = "0;35;0"
orange = "0;33;0"
red = "0;31;0"
testTrans = [{'sender': 'Andy', 'receiver': 'jerry', 'value': 50, 'payment': 40, 'change': 5,
              'signature': 'u4h298h4g92'},
             {'sender': 'James', 'receiver': 'Billy', 'value': 35, 'payment': 10, 'change': 15,
              'signature': 'u4h298h4g92'}]


def isnum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


'''
lookup %20f for formatting print() functions
lookup ansi code for colouring print() functions
make sure class/object stuff is working in the cli
'''


def minerCLI(init):
    # actual = Miner(init)
    while True:
        print("Available Functions: ")
        print("\x1b[%sm %19s \x1b[0m" % (green, 'help;'))
        print("\x1b[%sm %19s \x1b[0m" % (green, 'whoami'))
        print("\x1b[%sm %19s \x1b[0m" % (orange, 'testTransaction;'))
        print("\x1b[%sm %19s \x1b[0m" % (orange, 'preBuiltTrans;'))
        print("\x1b[%sm %19s \x1b[0m" % (purple, 'run;'))
        print("\x1b[%sm %19s \x1b[0m" % (red, 'exit;'))
        var = input("Please choose from the above functions: ")
        if var == "help":
            cont = "N"
            while cont != 'y' and cont != "Y":
                print("-===HELP===-")
                print("	testTransaction:- create and process a transaction")
                print("	preBuiltTrans:- process a pre-made transaction")
                print("	exit will return you to the Miner/Wallet selection")
                cont = input("  continue? Y/N: ")
        elif var == "preBuiltTrans":
            transactions = []
            for transaction in testTrans:
                print(transaction)
                transactions.append(json.dumps(transaction))
                # actual.run(transactions)
        elif var == "testTransaction":
            print("Known names: ")
            f = []
            for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
                print("%s" % os.getcwd())
                for filename in filenames:
                    a = re.findall('^(\w+)Public\.pem$', filename)
                    if not a:
                        continue
                    f += a
            for name in f:
                print("name: %s" % name)
            sender = input("Please enter the name of the sender: ")
            while not (sender in f):
                for name in f:
                    print("name: %s" % name)
                sender = input("Please enter one of the names listed above for the sender: ")
            recipient = input("Please enter the name of the recipient: ")
            while not (recipient in f) & (recipient != sender):
                for name in f:
                    if name != sender:
                        print("name: %s" % name)
                recipient = input("Please enter one of the names listed above for the recipient: ")
            inputValue = input("Please enter the amount you are putting into the transaction: ")
            while not (isnum(inputValue)) or float(inputValue) <= 0:
                inputValue = input(
                    "Please enter a numerical amount, greater than 0 that you are putting into the transaction: ")
            outputValue = input("Please enter the amount you are paying %s: " % recipient)
            while not (isnum(outputValue)) or (outputValue > inputValue) or float(outputValue) <= 0:
                outputValue = input(
                    "Please enter a numerical value lower than or equal to %s but greater than 0, that you are paying to %s: " % (
                        inputValue, recipient))
                # actual.run('stuff')
        elif var == "run":
            # actual.run()?
            pass
        elif var == "whoami":
            cont = 'n'
            while cont != 'y' and cont != 'Y':
                print("You are: %20s" % init)
                cont = input("continue? Y/N: ")
        elif var == "exit":
            break
        else:
            print("Please enter either 'help', 'testTransaction', 'preBuiltTransaction' or 'exit'")


def walletCLI(init):
    # act = Wallet(init)
    while True:
        print("Available Functions: ")
        print("\x1b[%sm %19s \x1b[0m" % (green, 'help;'))
        print("\x1b[%sm %19s \x1b[0m" % (green, 'whoami'))
        print("\x1b[%sm %19s \x1b[0m" % (purple, 'checkBalance;'))
        print("\x1b[%sm %19s \x1b[0m" % (orange, 'sendCoins;'))
        print("\x1b[%sm %19s \x1b[0m" % (red, 'exit;'))
        var = input("Please choose from the above functions: ")
        if var == "help":
            cont = 'N'
            while cont != 'Y' and cont != 'y':
                print("-===HELP===-")
                print(" Function '\x1b[%sm %s \x1b[0m' will respond with your username" % (green, 'whoami'))
                print(" Function '\x1b[%sm %s \x1b[0m' will inform you of your current available and actual funds" % (
                    purple, 'checkBalance'))
                print(" Function '\x1b[%sm %s \x1b[0m' will create a transaction to a person of your choosing" % (
                    orange, 'sendCoins'))
                print(" Function '\x1b[%sm %s \x1b[0m' will return you to the wallet/miner selection screen" % (
                    red, 'exit'))
                cont = input("  continue? Y/N: ")
        elif var == "checkBalance":
            print("Checking your balance")
            print("Account: \x1b[%sm %10s \x1b[0m" % (purple, init))
            # print("Available: %20s" % act.availableFunds())
            # print("Total Balance: %20s" % act.actualBalance())
        elif var == "sendCoins":
            f = []
            for name in f:
                if name != init:
                    print("name: %s" % name)
            recipient = input("Please enter the recipient: ")
            """This loop ensures that you are not entering an invalid name"""
            while not (recipient in f) & (recipient != init):
                for name in f:
                    if name != init:
                        print("name: %s" % name)
                recipient = input("Please enter one of the names listed above for the recipient: ")
            value = input("Please enter how much you are putting into the transaction: ")
            while not (isnum(value)) or float(value) <= 0:
                value = input(
                    "Please enter a numerical amount, greater than 0 that you are putting into the transaction: ")
            payment = input("Please enter how much you are sending to %s: " % recipient)
            while not (isnum(payment)) or float(payment) > float(value) or float(payment) <= 0:
                payment = input(
                    "Please enter a numerical value lower than or equal to %s but greater than 0, that you are paying to %s: " % (
                        value, recipient))
            minerFee = input("Please enter how much you are paying the miner: ")
            while not (isnum(minerFee)) or float(minerFee) > (float(value) - float(payment)) or float(
                    minerFee) < 0:
                minerFee = input(
                    "Please enter a numerical value between 0 and %d, that you are paying to the miner: " % (
                        float(value) - float(payment)))
            change = float(value) - float(payment) - float(minerFee)
            print(
                "You are creating a transaction with a value of %s, with %s being sent to %s and %s being sent to the miner. You will be receiving %s as change"
                % (value, payment, recipient, minerFee, change))
            '''actual.generateTransaction(recipient, value, payment, change)'''
        elif var == "whoami":
            cont = 'n'
            while cont != 'y' and cont != 'Y':
                print("You are: %20s" % init)
                cont = input("continue? Y/N: ")
        elif var == "exit":
            break
        else:
            print("Please enter either 'help', 'checkBalance', 'createTransaction' or 'exit'")


def main():
    exit = 'N'
    while exit != 'Y' and exit != 'y':
        print("Known accounts: ")
        f = []
        for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
            for filename in filenames:
                a = re.findall('^(\w+)Public\.pem$', filename)
                if not a:
                    continue
                f += a
        for name in f:
            print("name: %10s" % name)
        init = input("Who are you signing in as? ")
        while init not in f:
            init = input("Please choose one of the names above: ")
        print("At any choice-junction you may input 'whoami' to find out who you are signed in as.")
        while True:
            start = input("Would you like to start a miner or a wallet? ")
            if start == "wallet":
                walletCLI(init)
            elif start == "miner":
                minerCLI(init)
            elif start == "whoami":
                print("You are: %10s" % init)
            elif start == "exit":
                break
            else:
                print("Please enter either 'miner', 'wallet', 'whoami' or 'exit'")
        exit = input("Would you like to exit the program? Y/N: ")


if __name__ == "__main__":
    main()
