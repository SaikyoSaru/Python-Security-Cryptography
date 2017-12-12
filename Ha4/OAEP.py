import formulas as form
import numpy as np
import hashlib
import math
import binascii
"""
does a bitwiss xor
"""
def xor_b(var, key):
    return bytes(a ^ b for a, b in zip(var, key))

def I2OSP(x, xLen):
    if (x > 256**xLen):
        print("integer too big!!")
        return
    res = []
    while (x):
        res.append(x % 256)
        x //= 256

    return "".join(map(str,res[::-1])).zfill(8)


def MGF1(mgf_seed, mask_len, hash=hashlib.sha1):
    T = ''
    h_len = hashlib.sha1().digest_size
    max_c = math.ceil(mask_len/h_len)

    if mask_len > pow(2,32):
        print("masklen too long!!", mask_len)
        return

    for counter in range(max_c):
        C = I2OSP(counter, 4)
        T += hash(binascii.unhexlify(mgf_seed + C)).hexdigest()
    return T[:mask_len*2]


def OAEP_encode(M, mgfSeed, hash = hashlib.sha1):
    k = 128 # the lenght of the encoded message
    h_len = hashlib.sha1().digest_size
    h_l = hash(binascii.unhexlify("")).hexdigest()
    pad_l = k - len(M)/2 - 2*h_len - 2
    pad_s = "0".zfill(2*int(pad_l))
    DB = h_l + pad_s + "01" + M
    db_mask = MGF1(seed, k - h_len - 1)
    masked_db = xor_b(binascii.unhexlify(DB), binascii.unhexlify(db_mask))
    masked_db = binascii.hexlify(masked_db).decode('utf-8')
    seed_mask = MGF1(masked_db, h_len)
    masked_seed = xor_b(binascii.unhexlify(seed), binascii.unhexlify(seed_mask))
    masked_seed = binascii.hexlify(masked_seed).decode('utf-8')
    EM = "00" + masked_seed + masked_db
    return EM


def OAEP_decode(EM, hash=hashlib.sha1):
    k = 128
    h_len = hashlib.sha1().digest_size
    h_l = hash(binascii.unhexlify("")).hexdigest()

    Y = EM[:2]
    if (int(Y)):
        print ("decryption error")
        return
    maskedSeed = EM[2:2*h_len+2]
    maskedDB = EM[2+2*h_len:(2+2*h_len + (2*k-2*h_len-1))]
    seedMask = MGF1(maskedDB, h_len)
    seed = xor_b(binascii.unhexlify(seedMask), binascii.unhexlify(maskedSeed))
    seed = binascii.hexlify(seed).decode('utf-8')
    db_mask = MGF1(seed, k - h_len - 1)
    DB = xor_b(binascii.unhexlify(maskedDB), binascii.unhexlify(db_mask))
    DB = binascii.hexlify(DB).decode('utf-8')
    l_hash = DB[:h_len*2]
    if (l_hash != h_l):
        print ("decryption error")
    DB = DB[2*h_len:]
    if ("01" not in DB):
        print ("decryption error")
    where = DB.find("01")
    #print ("there he is:", where)

    M = DB[where+2:]

    return M


mgfSeed = 'ab61395aa98b49f0a6de254e933e391eb8'
maskLen = 30

M = 'f56bb84aff6f2240e8da52fb34f9f48ffd3e891c75df2abac46d29ab3a'
seed = '2142138dc59ad2367e5091d72d84046f99547e32'

EM = '00b2f73d91326091417ed768c1bab03bdf7d32cb15d2345866989457444e4884\
695e81d6241ec8130c631733247498de28d4b5acfa50496127730f60b29cfad2\
157ca073fc373e40305f7eaeadcd30a7d591185f84876ca9e9d417f8441127df\
b137ff4faf8437bd955e5dc03ed9094e6ea8429fa67e15173c42b2839afbd156'

print ("result mgf", MGF1(mgfSeed, maskLen))


print ("result OAEP encode:",OAEP_encode(M,seed))
print ("result OAEP decode:",OAEP_decode(EM))
