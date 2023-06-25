import json
import random

def update_payload():

    with open('config/names.txt', 'r', encoding='utf-8') as f:
        names = f.read().splitlines()

    with open('config/pfps.txt', 'r', encoding='utf-8') as f:
        pfps = f.read().splitlines()

    name_pfp_pairs = list(zip(names, pfps))

    pair_index = random.randint(0, len(name_pfp_pairs) - 1)

    return name_pfp_pairs[pair_index]