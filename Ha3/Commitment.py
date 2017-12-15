import numpy as np
import formulas as form
import hashlib
import random as randy
import pandas as pd
import binascii
import matplotlib.pyplot as plt

def prob_bind(t, hash=hashlib.sha256):

    hash_0 = set()
    hash_1 = set()

    v1 = bin(1)[2:]
    v0 = bin(0)[2:]


    bind = 0
    counter = 0
    for i in range(pow(2,16)):
        k = bin(i)[2:].zfill(16)
        t1 = int(v1 + k, 2)
        t2 = int(v0 + k, 2)
        temp1 = bin(int((hash((v1+k).encode('utf-8')).hexdigest()), 16))[2:t]
        temp2 = bin(int((hash((v0+k).encode('utf-8')).hexdigest()), 16))[2:t]
        if temp1 in hash_1:
            counter += 1
        hash_1.add(temp1)
        if temp2 in hash_1:
            bind = 1
            counter +=1
        if temp2 in hash_0:
            counter +=1
        hash_0.add(temp2)
        if temp1 in hash_0:
            bind = 1
            counter +=1

    return bind, counter


fin = []
for i in range(60):
    fin.append(prob_bind(i))

result = pd.DataFrame(data = fin, columns = ['bind', 'collisions'])
#result.drop([0])
result['proc'] = result.apply(lambda row : 100/(row.collisions +1) ,axis =1)
result['bind'] = result.apply(lambda row : 100*row.bind, axis = 1)
fig, axes = plt.subplots(nrows=3, sharex=True)

result['bind'].plot(ax = axes[0], title = 'Binding property',grid =True)
result['proc'].plot(ax= axes[1], title= 'Concealing property', grid = True)
ax1 = result['collisions'].plot(ax = axes[2], title = 'Amount of collsions',grid =True)
ax1.set_xlabel('amount of bits')
plt.xticks(np.arange(0, len(result), 2.0), rotation = 45)
plt.tight_layout()
plt.show()



print ("result", result)
