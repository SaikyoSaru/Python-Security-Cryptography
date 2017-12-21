import formulas as form
import numpy as np
import hashlib
import binascii
import numpy as np

"""
calculates the jacobi symbol
"""
def jacobi (a, m):
	j = 1
	a %= m
	while a:
		t = 0
		while not a & 1:
			a = a >> 1
			t += 1
		if t&1 and m%8 in (3, 5):
			j = -j
		if (a % 4 == m % 4 == 3):
			j = -j
		a, m = m % a, a
	return j if m == 1 else 0

def pkg(id_, p, q, M, hash = hashlib.sha1):
    ok = 0
    a = 0
    id_ = id_.encode('utf-8')
    while not ok is 1:
        id_ = hash(id_).digest()
        id_t = binascii.hexlify(id_)

        a = int(id_t, 16)
        ok = jacobi(a, M)
    r = pow(a, (M + 5 -p-q)//8, M)
    r_2 = pow(r,2, M)
    if (r_2 == (a%M)) or -a%M: # checks if the r value is ok
        print ("r is ok")
    else:
        print ("nein")
    return r, id_t

"""
decryption of message
"""
def decrypt(r, M, bit_list):
    d_m = ""
    for bit in bit_list:
        bit = int(bit, 16)
        bit = jacobi(bit - 2*r, M)
        if bit == 1:
            d_m += '1'
        else:
            d_m += '0'
    return d_m
"""
Cocks IBE-scheme
"""
def cocks(id_, p, q, bit_list, hash=hashlib.sha1):
    p = int(p, 16)
    q = int(q, 16)
    M = p*q
    r, a = pkg(id_, p, q, M)
    dec_mes = decrypt(r, M, bit_list)

    print ("r:", format(r, 'x'))
    print ("a:", a)
    print ("decrypted message:", int(dec_mes, 2))

    return dec_mes

#a = '25a4d152bf555e0f61fb94ac4ee60962decbbe99'


p = '9240633d434a8b71a013b5b00513323f'
q = 'f870cfcd47e6d5a0598fc1eb7e999d1b'
identity = 'faythe@crypto.sec'

Encrypted_bits = ['60bddfa36cdc174c4875b17bc4c6353ac3337369c3cdb464162f0514bf9754f8',
'0d10af339c7a199b97839fed1618d59acd5e8262d35f12e3c3523b7e79af82b4',
'873598c2e8beecc35ba986bc76163039a55211f5e3d2bc5e14bf5700e1ebff71',
'157da3a6c5a27311c5ba3aee9900ba9cf38a403896bf44fbd94e949746b2e896',
'5b0379f952784bbce6100805e46c9ea4e9e333b3be86b9efbe69c8fb73872af2',
'45ad5a4f8dcb2f1d3f2557d89a0c5952ac4600870a096d034d10cfb08408039b',
'65cd9c8eda1ec2e3001604b861dc9b69cafca09a34eef59d546c5743e2ce8adf',
'0106ae2139260de452085455676eee88fde900bca69059d0dd231cc7ff53864c']
cocks(identity, p, q, Encrypted_bits)
