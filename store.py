FILENAME = "money.txt"

def write_money(money):
    with open(FILENAME, "w") as file:
        file.write((str(money)))

def read_money():
    with open(FILENAME, "r") as file:
        line = file.readline()

    money = float(line)
    return money