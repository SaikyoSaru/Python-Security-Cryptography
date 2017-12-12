import numpy as np
import socket
import secrets
import formulas as form
import hashlib
import binascii

def diff_exchange(g1,b,p):

        g_a = soc.recv(4096).decode('utf8').strip()
        g_a = int(g_a, 16)
        g_b = pow(g1, b, int(p, 16))
        g_b_str = format(g_b, 'x')
        soc.send(g_b_str.encode('utf8'))
        res = soc.recv(4096).decode('utf8').strip()

        return pow(g_a, b ,int(p,16))



def SMP(g1, p, message, hash=hashlib.sha1):
    y = secrets.randbits(pow(10, 2)) #y
    b2 = secrets.randbits(pow(10, 2))
    b3 = secrets.randbits(pow(10, 2))

    g_xy = diff_exchange(g1, y, p)
    dh_key = g_xy
    #print ("dh_key", dh_key)
    g_xy = g_xy.to_bytes((g_xy.bit_length() + 7) // 8, 'big')
    ss = 'eitn41 <3'.encode('utf-8')

    y = hash((g_xy + ss)).hexdigest()
    #print ("y", y)

    g2 = diff_exchange(g1, b2, p)
    g3 = diff_exchange(g1, b3, p)

    #p3
    b = secrets.randbits(pow(10, 2))
    p_b = pow(g3, b, int(p, 16))
    q_b = pow(g1, b, int(p,16)) * pow(g2, int(y, 16), int(p, 16))
    q_b_inv = form.modinv(q_b, int(p, 16))

    """
    exchange time!!
    """
    p_a = soc.recv(4096).decode('utf8').strip()
    p_a = int(p_a, 16)
    p_b_str = format(p_b, 'x')
    soc.send(p_b_str.encode('utf8'))
    rec = soc.recv(4096).decode('utf8').strip()
    #print ("p_b:", rec)

    q_a = soc.recv(4096).decode('utf8').strip()
    q_a = int(q_a, 16)
    q_b_str = format(q_b, 'x')
    soc.send(q_b_str.encode('utf8'))
    rec = soc.recv(4096).decode('utf8').strip()
    #print ("Qb:", rec)

    qa_qb_inv_a3 = soc.recv(4096).decode('utf8').strip()
    qa_qb_inv_a3 = int(qa_qb_inv_a3, 16)


    qa_qb_inv_b3 = pow((q_a*q_b_inv), b3, int(p, 16))
    qa_qb_inv_b3_str = format(qa_qb_inv_b3, 'x')
    soc.send(qa_qb_inv_b3_str.encode('utf8'))
    rec = soc.recv(4096).decode('utf8').strip()
    #print ("qa_qb_inv_b3:", rec)
    #authentication time!!
    rec = soc.recv(4096).decode('utf8').strip()
    print ("authentication:", rec)

    m = int(message, 16)
    #print ("integer representation of message:", m)
    em = m ^ dh_key
    #print ("integer encrypted message:", em)
    fin = format(em, 'x')
    #print ("encrypted message:", fin)
    soc.send(fin.encode('utf-8'))
    response = soc.recv(4096).decode('utf8').strip()
    print ("response:", response, len(response))
    return response


"""
Main
"""
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(("eitn41.eit.lth.se", 1337))

g = g1 = 2
s_s = 'eitn41 <3'

p = 'FFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1\
29024E088A67CC74020BBEA63B139B22514A08798E3404DD\
EF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245\
E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7ED\
EE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3D\
C2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F\
83655D23DCA3AD961C62F356208552BB9ED529077096966D\
670C354E4ABC9804F1746C08CA237327FFFFFFFFFFFFFFFF'

message = 'ff8f27a723d4f1524b369cce7efa3589c17915ff'
SMP(g1, p, message)
