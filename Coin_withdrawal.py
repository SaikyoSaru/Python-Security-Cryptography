
import numpy as np
import formulas as form
import pandas as pd
import fractions

"""
The xor function
"""
def encrypt(var, key):
    return bytes(a ^ b for a, b in zip(var, key))

"""
Creates 2k quadruples of random mod n values
param:
k : amount of quadruples
n : the number we will take modulo for
"""
def quadRuples(k,n):
    set_of_quad = pd.DataFrame(np.random.randint(0, 2*n,
    size =(2*k,4))%n, columns = ['a','c','d','r'])
    res = set_of_quad['r'].values
    res = [fractions.gcd(x,n) for x in res]
    print ("gcd of r and n", res)
    return set_of_quad
"""
Computes Bi from the 2k quadrules
param:
quads: the quadruples
ID: Alice ID
n : the calulated value from the two pries p and q
e : the exponent
"""
def computeBi(quads, ID, n, e):
    a = quads['a'].apply(lambda x : form.byteToHex(form.fromIntToByte(x, 8)))
    c = quads['c'].apply(lambda x : form.byteToHex(form.fromIntToByte(x, 8)))
    d = quads['d'].apply(lambda x : form.fromIntToByte(x, 8))

    a = a + c #concatenation of a and c
    y = [form.byteToHex(encrypt(x, ID)) for x in d]
    d = quads['d'].apply(lambda x : form.byteToHex(form.fromIntToByte(x, 8)))
    y = y + d #concatenation of y and d
    y = pd.DataFrame([form.toSha1(val) for val in y]).values
    x = pd.DataFrame([form.toSha1(val) for val in a]).values
    f = x + y #concatenation of x and y
    f = pd.DataFrame([form.toSha1(val[0]) for val in f]).values
    B = quads['r'].apply(lambda x : pow(x, e, n))
    f = [form.hexToInt(val[0]) for val in f]

    B = (B*f) # the final Bi values
    B = pd.DataFrame([ hex(val) for val in B])
    return B


"""
gets the selected indices from the random generated values
#cut and choose
"""
def getIndices(indices):
    ak = quad['a'].iloc[indices]
    ck = quad['c'].iloc[indices]
    dk = quad['d'].iloc[indices]
    rk = quad['r'].iloc[indices]

    quads = pd.DataFrame({'a' : ak, 'c' : ck, 'd' : dk, 'r' : rk})
    return quads


"""
bank checks if the values are correct
"""
def checkBi(Bi, indices, ID, e):
    Bi = Bi.iloc[indices]
    quads = getIndices(indices) #the chosen indices
    #print ("Chosen values from Bi:", Bi)
    recalc = computeBi(quads, ID, n, e) # the recomputed values
    recalc.index = indices
    #print ("Recalculated values:", recalc)

    for i in range(0, len(Bi)): # checks if they match
        if(str(Bi.iloc[i].item()) != str(recalc.iloc[i].item())):
            return False
    return True
"""
Calculates the modulo inverse
"""
def modinv(a,m):
	g,x,y = form.egcd(a,m)
	if g != 1:
		return None
	else:
		return x%m

"""
Bank calculates p*q = n , exponent e and e^-1
as well as the secret exponent
The values chosen for p and q :
p : 127
q : 151
n : 19177
phi : (p-1)(q-1)
e : 1 < e < phi
"""
p = 127
q = 151
n = 19177
phi = (p-1)*(q-1)
print ("phi", phi)
r = np.random.randint(2, 100) # For efficiency 2 < e < 100

while True:
	if fractions.gcd(r, phi) == 1:
		break
	else:
		r += 1
e = r
D = modinv(e, phi)
print ("e:", e)
print ("d:", D)

"""
Alice knows e,n and creates 2k quadRuples mod n
And creates Bi such as Bi = (ri^e)(f(x,y) mod n)
"""

ID = 1331237 # Alice ID
ID = form.fromIntToByte(ID, 8)

quad = quadRuples(20, n)
Bi = computeBi(quad, ID, n, e)
print ("Bi", Bi)

"""
The bank selects k indices from Alice 2k Bi
and demands the quadruples for those indices.
And checks if they are correct.
"""
indices = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
print ("check: ", checkBi(Bi, indices, ID, e))


"""
bank computes blind signatures
"""
#e1 = modinv(e, n)

indices = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

values = Bi.iloc[indices].values
values = [form.hexToInt(val[0]) for val in values]
values = [pow(val, D, n) for val in values]
print (values)

blind_sign = 1
for val in values:
    blind_sign *= val
blind_sign = blind_sign % n
print ("blind signature", blind_sign)
coin = '1337'


"""
Alice gets the blind signatures and the unsigned coin from the bank and
extracts the signatures with the r values
"""
print ("e*d:", (e*D) % phi)
r_values = quad['r'].iloc[indices]
r_val = 1
for val in r_values:
    r_val *=  val
r_val = modinv(n, r_val)
signature = blind_sign*r_val

print ("signature:", signature)

"""
Alice can now sign the coin with the banks signature!
"""




"""
While noSuccess:
    tryAgain()
    if Dead:
        return

"""
