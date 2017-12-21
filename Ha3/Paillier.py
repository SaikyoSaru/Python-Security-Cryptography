import numpy as np
import formulas as form


"""
Calculates the least common multiplier
"""
def lcm(x, y):
   if x > y:
       biggger = x
   else:
       bigger = y

   while(True):
       if((bigger % x == 0) and (bigger % y == 0)):
           lcm = bigger
           break
       bigger += 1

   return lcm
"""
Modular inverse m of a
"""
def modinv(a,m):
	g,x,y = form.egcd(a,m)
	if g != 1:
		return None
	else:
		return x%m


def Lfunc(x, n):

    return (x - 1) / n

"""
Paillier scheme
"""
def paillier(p, q, g, votes):
    n = p*q # 35
    phi = (q-1)*(p-1)
    c = 1
    for i in votes:
        c *= int(i)

    c = c % pow(n,2)


    lamda = lcm(p-1, q-1) #ok
    c = c**lamda  % pow(n,2)
    g = (g**lamda) % (n**2)
    L = Lfunc(g, n)
    L2 = Lfunc(c, n)
    u = modinv(L,n)
    m = (L2 * u) % n
    print ("m", m)
    m = m - n
    return m




f = open('/Users/mattias/Documents/Avancerad websäkerhet/python/Ha3/paillier.txt', 'r')

votes = []
for line in f:
    line = line[:-1]
    votes.append(int(line))

p = 1117
q = 1471
g = 652534095028

m = paillier(p, q, g, votes)

print ("final reslut of the votes:", m)
