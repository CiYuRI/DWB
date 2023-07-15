import random

def uwupayload():
    with open('config/uwunames.txt', 'r', encoding='utf-8') as f:
        names = f.read().splitlines()

    with open('config/uwupfps.txt', 'r', encoding='utf-8') as f:
        pfps = f.read().splitlines()

    uwus = list(zip(names, pfps))

    pair_index = random.randint(0, len(uwus) - 1)

    return uwus[pair_index]

def chadpayload():
    with open('config/chadnames.txt', 'r', encoding='utf-8') as f:
        names = f.read().splitlines()

    with open('config/chadpfps.txt', 'r', encoding='utf-8') as f:
        pfps = f.read().splitlines()

    chads = list(zip(names, pfps))

    pair_index = random.randint(0, len(chads) - 1)

    return chads[pair_index]
