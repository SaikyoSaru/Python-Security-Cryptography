import formulas as form
import numpy as np
import binascii
from pcapfile import savefile
import pandas as pd
import socket
import struct

"""
ip : the ip of the target
mixIp : the ip of the mixer
pcap : the pcap file
"""
def collectData(AbuIp, mixIp, pcap):
    sets = []
    tmp_set = set()
    Abu, collect = False, False
    old_ip_src = 0;
    old_ip_dst = 0;
    for pkt in capfile.packets:
        timestamp = pkt.timestamp
        ip_src = pkt.packet.payload.src.decode('UTF8')
        ip_dst = pkt.packet.payload.dst.decode('UTF8')
        if (ip_src == AbuIp):
            Abu = True
        if (Abu):
            if (ip_src == mixIp):
                collect = True
            if (collect and (old_ip_src == mixIp)):
                tmp_set.add(old_ip_dst)
                if (ip_dst == mixIp):
                    sets.append(tmp_set)
                    tmp_set = set()
                    collect = Abu = False
        old_ip_dst = ip_dst
        old_ip_src = ip_src
    if (len(tmp_set) != 0):
        sets.append(tmp_set)
    return sets

def checkDisjoint(sets):
    disjoint_sets = []
    not_disjoint_sets = []
    disjoint = True
    for s in sets:
        for n in disjoint_sets:
            if not s.isdisjoint(n):
                not_disjoint_sets.append(s)
                disjoint = False
                break
        if (disjoint):
            disjoint_sets.append(s)
        disjoint = True
    return disjoint_sets, not_disjoint_sets

def exclusion(disSet, sets):
    for s in sets:
        disjoint = []
        for dis in disSet:
            if  not s.isdisjoint(dis):
                disjoint.append(dis) # appends Ri

        if len(disjoint) == 1:
            old_Ri = disjoint[0]
            disSet.remove(old_Ri)
            new_Ri = old_Ri & s
            disSet.append(new_Ri)
    result = [dis.pop() for dis in disSet]
    return (result)

def convert(ip): #converts ip to integer representation
    return struct.unpack("!I", socket.inet_aton(ip))[0]

def disclosureA(ip, mixIp, n , capfile):
    """
    Learning phase
    """
    sets = collectData(ip, mixIp, capfile)
    disSet, notDisSet = checkDisjoint(sets)
    """
    Exluding phase
    """
    partnersIP = exclusion(disSet, sets)
    """
    Convert ip addresses to integers
    """
    partners = [convert(x) for x in partnersIP]
    sum_ip = sum(partners)
    print ("partners ip:", partnersIP)
    print("result:", sum_ip)


cap = open('cia.log.3.pcap','rb') # open file, read bytes
capfile = savefile.load_savefile(cap, layers=2, verbose=True)
ip = '61.152.13.37'
mixIp = '95.235.155.122'
n = 8
disclosureA(ip, mixIp, n, capfile)
#19776094811
