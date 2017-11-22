import numpy as np
import struct
import hashlib
import formulas
import binascii


n = 2897

n = formulas.fromIntToByte(n,4)

#n = binascii.hexlify(n)

print ("1:", binascii.hexlify(n))

n = formulas.toSha1(n)
#n = binascii.hexlify(n)
#n = formulas.byteToHex(n)
print ("2:", n)


n = '0123456789abcdef'
c = binascii.hexlify(n.encode('utf-8'))

#b = bytes(n, 'utf-8')
b = bytearray.fromhex(n)

print ("b:", b, "c:", c)
print (len(c))
b = formulas.fromByteToInt(b)
#b = int.from_bytes(b, byteorder = 'big')
#print ("b ", b)
#b = int.from_bytes(b, byteorder = 'little')
#b = bytearray()
#n = b.extend(n.encode())
#b = b

print ("3:", b)

e = formulas.hexToByte('fedcba9876543210')
print ("tester:", e)
e = bytes('fedcba9876543210', 'utf-8')
print ("tester 2", e)
n = '0123456789abcdef'

b = bytearray.fromhex(n)
#b = int.from_bytes(b, byteorder = 'big')
b = formulas.toSha1(b)

print ("sha-1 hex:", binascii.hexlify(b))

#b = int.from_bytes(b, byteorder = 'big')
b = formulas.fromByteToInt(b)
print ("4:", b)

#print (pow((2*3.66 * 4675.15958097)/(4783), 2) )
