import json
import os
import re

from client import Client

nameCol = "0;0;0"
base = "0"
green = "0;32;0"
purple = "0;35;0"
orange = "0;33;0"
red = "0;31;0"
blue = "0;34;0"
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
    # act = Miner(init)
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
                # act.run(transactions)
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
                # act.run('stuff')
        elif var == "run":
            # act.run()?
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


def helpWallet():
    cont = False
    while not cont:
        print("-===HELP===-")
        print(" Function '\x1b[%sm %s \x1b[0m' will respond with this" % (green, 'help'))
        print(" Function '\x1b[%sm %s \x1b[0m' will respond with your username" % (green, 'whoami'))
        print(" Function '\x1b[%sm %s \x1b[0m' will inform you of your current available and actual funds" % (
            purple, 'checkBalance'))
        print(" Function '\x1b[%sm %s \x1b[0m' will create a transaction to a person of your choosing" % (
            orange, 'sendCoins'))
        print(" Function '\x1b[%sm %s \x1b[0m' will return you to the wallet/miner selection screen" % (
            red, 'exit'))
        cont = input("  press any key to continue: ")


def walletCLI(init, fname):
    act = Client(init, False)
    while True:
        print("Available Functions: ")
        print("1. \x1b[%sm %17s \x1b[0m" % (green, 'help;'))
        print("2. \x1b[%sm %17s \x1b[0m" % (green, 'whoami'))
        print("3. \x1b[%sm %17s \x1b[0m" % (purple, 'checkBalance;'))
        print("4. \x1b[%sm %17s \x1b[0m" % (orange, 'sendCoins;'))
        print("5. \x1b[%sm %17s \x1b[0m" % (red, 'exit;'))
        var = input("Please choose from the above functions: ")
        print("")
        if var == "help" or var == "1":
            helpWallet()
            print("")
        elif var == "checkBalance" or var == "3":
            print("Checking your balance")
            print("Account: \x1b[%sm %10s \x1b[0m" % (purple, init))
            x, y = act.check_balance()
            print("Total: %13s \nAvailable: %9s\n" % (x, y))
        elif var == "sendCoins" or var == "4":
            print("Collecting relevant information")
            for name in fname:
                if name != init:
                    print("\x1b[%sm name | %s \x1b[0m" % (blue, name))
            recipient = input("Please enter the recipient: ")
            if recipient.strip() == 'break' or recipient.strip() == '':
                continue
            """This loop ensures that you are not entering an invalid name"""
            while not (recipient in fname) & (recipient != init):
                for name in fname:
                    if name != init:
                        print("\x1b[%smname: %s\x1b[0m" % (blue, name))
                recipient = input("Please enter one of the names listed above for the recipient: ")
                if recipient.strip() == 'break' or recipient.strip() == '':
                    break
            if recipient.strip() == 'break' or recipient.strip() == '':
                continue
            value = input("Please enter how much you are putting into the transaction: ")
            if value.strip() == 'break' or value.strip() == '':
                continue
            chuck, available = act.check_balance()
            while not (isnum(value)) or float(value) <= 0 or float(value) > available:
                if not isnum(value):
                    value = input(
                        "Please enter a numerical amount: ")
                elif float(value) <= 0:
                    value = input("Please enter a value greater than 0: ")
                elif float(value) > available:
                    value = input(
                        "You only have %s in your account, please enter a value less than or equal to this: " % available)
                if value.strip() == 'break' or value.strip() == '':
                    break
            if value.strip() == 'break' or value.strip() == '':
                continue
            payment = input("Please enter how much you are sending to %s: " % recipient)
            if payment.strip() == 'break' or payment.strip() == '':
                continue
            while not (isnum(payment)) or float(payment) > float(value) or float(payment) <= 0:
                if not isnum(payment):
                    payment = input(
                        "Please enter a numerical value that you are paying to %s: " % (
                            recipient))
                elif float(payment) <= 0:
                    payment = input(
                        "Please enter a numerical value greater than 0 that you are paying to %s" % recipient)
                elif float(payment) > float(value):
                    payment = input(
                        "Please enter a numerical value less than %s that you are paying to %s" % (value, recipient))
                if payment.strip() == 'break' or payment.strip() == '':
                    break
            if payment.strip() == 'break' or payment.strip() == '':
                continue
            minerFee = input("Please enter how much you are paying the miner: ")
            if minerFee.strip() == 'break' or minerFee.strip() == '':
                continue
            while not (isnum(minerFee)) or float(minerFee) > (float(value) - float(payment)) or float(
                    minerFee) < 0:
                minerFee = input(
                    "Please enter a numerical value between 0 and %d, that you are paying to the miner: " % (
                        float(value) - float(payment)))
                if minerFee.strip() == 'break' or minerFee.strip() == '':
                    break
            if minerFee.strip() == 'break' or minerFee.strip() == '':
                continue
            change = float(value) - float(payment) - float(minerFee)
            print(
                "You are creating a transaction with a value of %s, with %s being sent to %s and %s being sent to the miner. You will be receiving %s as change"
                % (value, payment, recipient, minerFee, change))
            print("Success: %s\n" % act.send_transaction(recipient, value, payment, change))
        elif var == "whoami" or var == "2":
            print("\x1b[%sm You are: %20s \x1b[0m\n" % (blue, init))
        elif var == "exit" or var == "5":
            break
        else:
            helpWallet()
            # print("Please enter either 'help', 'checkBalance', 'createTransaction' or 'exit'")


def main():
    exit = 'N'
    while exit != 'Y' and exit != 'y':
        while True:
            start = input(
                "Would you like to start a \x1b[%smminer\x1b[0m or a \x1b[%smwallet\x1b[0m? " % (purple, green))
            if start == "wallet":
                print("Known accounts: ")
                f = []
                for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
                    for filename in filenames:
                        a = re.findall('^(\w+)Public\.pem$', filename)
                        if not a:
                            continue
                        f += a
                for name in f:
                    print("\x1b[%sm name | %10s \x1b[0m" % (blue, name))
                init = input("Who are you signing in as? ")
                while init not in f:
                    init = input("Please choose one of the names above: ")
                print("At most points in this program you may input 'whoami' to find out who you are signed in as.\n")
                print("\n%s\n" % '--------------------')
                walletCLI(init, f)
            elif start == "miner":
                print("\n%s\n" % '--------------------')
                minerCLI(init)
            elif start == "whoami":
                print("You are: \x1b[%sm %10s \x1b[0m" % (blue, init))
            elif start == "exit":
                break
            else:
                print("Please enter either 'miner', 'wallet', 'whoami' or 'exit'")
        exit = input("Would you like to exit the program? Y/N: ")


if __name__ == "__main__":
    main()
