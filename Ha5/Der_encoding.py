import formulas as form
import math
import binascii
import base64
"""
DER encoder
____________________
returns: DER encoded values
param:
val = the value that you want to encode
T = the tag representing what kind of value it is
"""
def DER(val, T = '02'):
    val_bin = bin(val)[2:]
    if (val_bin[0]) or len(val_bin)%8:
        #for padding purposes when the leading bit = 1
        val_bin = val_bin.zfill(len(val_bin) + (8-(len(val_bin)%8)))

    V_L = int(len(val_bin)/8)
    V = format(int(val_bin,2), 'x')
    V = V.zfill(V_L*2)
    L = ""
    # checks which form is needed to represent the value
    if (V_L > 127):
        #long definite form
        V_h = format(V_L, 'x')
        if len(V_h)%2:
            V_h = '0' + V_h #pad if uneven representation
        #create the value that displays the lenght needed
        first_octet = format((2**7 + int(len(V_h)/2)), 'x')
        L = first_octet + V_h
    else:
        # short definite form
        L = format(V_L, 'x').zfill(2)
    # Tag + Length + Value
    output = T + L + V
    #print ("output:", output)

    return T + L + V

"""
RSA-key generator
_________________
returns:
an private RSA-key
param:
q,p : the primes you have chosen
"""
def RSA(p, q, e=65537):
    """
    calulate integer values
    """
    ver = 0
    n = p*q
    phi = (p-1)*(q-1)
    d = form.modinv(e, phi)
    e1 = d % (p-1)
    e2 = d % (q-1)
    coeff = form.modinv(q,p)
    """
    print ("version:", ver, "\nn", n, "\ne", e,
           "\np", p, "\nq:", q,
           "\nd:", d, "\ne1:", e1 ,
           "\ne2", e2, "\ncoefficient:", coeff)
    """
    """
    encode integer values as DER
    """
    D_v = DER(ver)
    D_n = DER(n)
    D_e = DER(e)
    D_d = DER(d)
    D_p = DER(p)
    D_q = DER(q)
    D_e1 = DER(e1)
    D_e2 = DER(e2)
    D_coeff = DER(coeff)

    D = D_v + D_n + D_e + D_d + D_p + D_q + D_e1 + D_e2 + D_coeff
    # the value 30 signifies that is a sequence
    priv_key = DER(int(D, 16), '30') # 30 is the tag for SEQUENCE
    #print ("RSA private key", priv_key)

    priv_key = base64.b64encode(binascii.unhexlify(priv_key))

    #print ("b6a encoded private key:", priv_key.decode('utf-8'))
    #print ("2 + 2 is 4, - 1 is 3\n Qick Math!")
    return priv_key
