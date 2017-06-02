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


def isfloat(s):
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


def helpMiner():
    cont = False
    while not cont:
        print("-===HELP===-")
        print("	testTransaction:- create and process a transaction")
        print("	preBuiltTrans:- process a pre-made transaction")
        print("	exit will return you to the Miner/Wallet selection")
        cont = input("  press any key to continue: ")


def minerCLI():
    act = Client('miner')
    while True:
        print("Available Functions: ")
        print("1. \x1b[%sm %19s \x1b[0m" % (green, 'help;'))
        print("2. \x1b[%sm %19s \x1b[0m" % (green, 'whoami'))
        print("3. \x1b[%sm %19s \x1b[0m" % (purple, 'getDifficulty;'))
        print("4. \x1b[%sm %19s \x1b[0m" % (orange, 'setDifficulty;'))
        print("5. \x1b[%sm %19s \x1b[0m" % (red, 'exit;'))
        var = input("Please choose from the above functions: ")
        if var == "help" or var == '1':
            helpMiner()
        elif var == "getDifficulty" or var == '3':
            print("Current difficulty is set at %s" % act.get_miner_difficulty())
        elif var == "setDifficulty" or var == '4':
            diff = act.get_miner_difficulty()
            newdiff = input("Current Difficulty is set at %s\nPlease enter the difficulty that you want: " % diff)
            if newdiff.strip() == 'break' or newdiff.strip() == '':
                continue
            while not newdiff.isdigit() or 255 < int(newdiff) < 1:
                if not newdiff.isdigit():
                    newdiff = input("Please enter an integer value for the difficulty that you want: ")
                elif 255 < int(newdiff) < 1:
                    newdiff = input("Please enter a value between 0 and 255: ")
                if newdiff.strip() == 'break' or newdiff.strip() == '':
                    break
            if newdiff.strip() == 'break' or newdiff.strip() == '':
                continue
            if newdiff != diff:
                act.set_miner_difficulty(newdiff)
        elif var == "whoami" or var == '2':
            print("\x1b[%smYou are: %20s\x1b[0m" % (blue, 'miner'))
        elif var == "exit" or var == '5' or var.strip() == 'break' or var.strip() == '':
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
    act = Client(init)
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
                if name != init or name != 'miner':
                    print("\x1b[%sm name | %10s \x1b[0m" % (blue, name))
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
            """This loop ensures that you are not entering an invalid value"""
            while not (isfloat(value)) or float(value) <= 0 or float(value) > available:
                if not isfloat(value):
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
            """This loop ensures that you are not entering an invalid value"""
            while not (isfloat(payment)) or float(payment) > float(value) or float(payment) <= 0:
                if not isfloat(payment):
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
            """This loop ensures that you are not entering an invalid value"""
            while not (isfloat(minerFee)) or float(minerFee) > (float(value) - float(payment)) or float(
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
        elif var == "exit" or var == "5" or var.strip() == 'break' or var.strip() == '':
            break
        else:
            helpWallet()
            # print("Please enter either 'help', 'checkBalance', 'createTransaction' or 'exit'")


def main():
    print("%16s\n%15s" % ('Welcome to ', '<OURCOIN>'))
    print("At most opportunities, entering 'break' or just spaces will break you out of the function")
    print("Otherwise, you can enter in the (case-sensitive) function name or the functions' number\n"
          " to enter that function")
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
                    if 'miner' not in a:
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
            minerCLI()
        elif start == "exit":
            exit(0)
        else:
            print("Please enter either 'miner', 'wallet', or 'exit'")


if __name__ == "__main__":
    main()
