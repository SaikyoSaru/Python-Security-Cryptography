import formulas as form
import numpy as np
import binascii


"""
Dining Cryptographers
_______________________
SA: my shared 16-bit secret with Alice
DA: broadcasted data sent by Alice
SB: my shared 16-bit sectret with Bob
DB: broadcasted data sent by Bob
b: deciding bit for message
M: my message
"""
def diningCrypt(SA, DA, SB, DB, M, b):
    sa = bin(int(SA, 16))
    sb = bin(int(SB, 16))
    da = bin(int(DA, 16))
    db = bin(int(DB, 16))
    m = bin(int(M, 16))

    if (b == 0):
        res1 = bin((int(sa, 2) ^ int(sb, 2)))
        res2 = hex(((int(da, 2) ^ int(db,2) ) ^ int(res1, 2)))
        res1 = hex(int(res1, 2))
        output = res1 + res2
    else:
        output = hex(int(bin((int(sa, 2) ^ int(sb, 2) ^ int(m,2))),2))
    return output





"""
input:
"""
SA = 'D75C'
SB = 'EE87'
DA = 'C568'
DB = 'FCB3'
M = '4674'
b = 1


print ("output:", diningCrypt(SA, DA, SB, DB, M, b))
