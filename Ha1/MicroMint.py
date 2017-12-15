import numpy as np
import formulas as f
import random



"""
returns the amount of iterations needed to create the
specified amount of coins
_______________
param
k : the number of collisions needed for a coin to be generated
u : the number of bits used for identifying the bin
c : the desired amount of coins
_______________
internal param
t : the amount of iterations
c_c : coints created
c_h : holder of coins
b : amount of bins
"""
def MicroMint(u, k, c):
    t = 0 #starting time
    b = pow(2,u) # amount of bins
    c_c = 0 # coins created
    c_h = [0]*(b) # holder of coins
    while (c_c < c):
        t+=1
        i = random.randint(0,b-1)
        c_h[i]+=1
        if (c_h[i] == k):
            c_c+=1

    return t
"""
Example
"""

lam = 3.66 # the lambda value for 99.9% confidence interval
res = [] # the matrix holding the samples
width = 4783 # confidence interval width
t_w = width*10 # the current width
n = 0 # the amount of samples taken
while(t_w > width):
    n += 1
    res.append(MicroMint(20,7,10000))
    std = np.std(res)
    avg = np.mean(res)
    if std != 0 :
        t_w = (2*lam*std)/(np.sqrt(n))
    print (std , avg , t_w)


print ("result:", avg)
