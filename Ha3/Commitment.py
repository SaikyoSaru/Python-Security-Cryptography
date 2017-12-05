import numpy as np
import formulas as form
import hashlib as h
import random as randy
import pandas as pd
import binascii
import matplotlib.pyplot as plt


def commitment(v, k, t):
    m = h.sha256()
    m.update((v+k).encode('utf-8'))

    out = m.hexdigest()[0:t]
    return out

def prob_bind(t):
    hash_0 = set()
    hash_1 = set()
    v = str(bin(1)[2:])
    new_v = str(bin(0)[2:])
    bind = 0
    counter = 0
    for i in range(pow(2,16)):
        k = str(bin(i)[2:].zfill(16))
        temp1 = commitment(v, k, t)
        if temp1 in hash_1:
            counter += 1
        hash_1.add(temp1)
    for j in range(pow(2,16)):
        k = str(bin(j)[2:].zfill(16))
        temp2 = commitment(new_v, k, t)
        if temp2 in hash_1:
            counter += 1
            bind = 1

        elif temp2 in hash_0:
            counter += 1

        hash_0.add(temp2)

    return bind, counter


fin = []

for i in range(64):

    fin.append(prob_bind(i))


result = pd.DataFrame(data = fin, columns = ['bind', 'collisions'])
result.drop([0])

print ("result", result)
