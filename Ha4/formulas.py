import hashlib
import pandas as pd
import numpy as np
import binascii

"""
converts int to byte array
__________
param:
n_int : the integer that you want to convert
size : the size in bytes that you want
--------
___________
returns:
the int representated as bytes

"""
def fromIntToByte(n_int, size):
    a = (n_int).to_bytes(size, byteorder = 'big')
    return a

"""
makes hashcode with sha-1
___________
param:
message : the message that you want to encrypt (a byte array)
___________
returns :
a byte array
"""
def toSha1(message):
    message = hexToByte(message)
    m = hashlib.sha1()
    m.update(message)
    return byteToHex(m.digest())

"""
converts hexadecimal rep to bytearray
_________
param:
message : the mesage we want to convert from hex to byte array
_________
returns :
a byte array
"""
def hexToByte(message):
    #n = bytes(message, 'utf-8')
    n = bytearray.fromhex(message)
    #n = binascii.hexlify(message) #to make it pretty
    return n
"""
Converts bytearray to hexadecimal representation
_________
param:
n : byte array
_________
returns:
hexadecimal representation of byte array
"""
def byteToHex(n):
    return (binascii.hexlify(n)).decode('ascii')


"""
Converts bytearray to int with the byteorder "big endian"
________
param:
n : byte array
________
returns:
integer representation of the byte array
"""
def fromByteToInt(n):
    return int.from_bytes(n, byteorder = 'big')



"""
Converts integer to string
"""

def intToHex(n):
    return str(n)






def modinv(a,m):
	g,x,y = egcd(a,m)
	if g != 1:
		return None
	else:
		return x%m

"""
extended euclidan algorithm
"""
def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y
