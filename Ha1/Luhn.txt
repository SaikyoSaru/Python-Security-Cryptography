import numpy as np

def Luhn(input,x):
    s = 0
    nDigits = len(input)
    parity = (nDigits)%2
    for i in range(0,nDigits):
        if input[i] == 'X':
            digit = x
        else:
            digit = int(input[i])
        if (i%2 == parity):
            digit = digit*2
            if (digit > 9):
                digit = digit - 9
        s += digit
    return ((s%10) == 0)


"""
tests
"""

a = '42222222222X2'
res = []
#print a
print (Luhn(a,2))
for i in range(0,len(a)):

    for x in range(0,10):

    #if Luhn('7992739871X', x):
        if Luhn(a[i],x ):
#            print ("result:", x)
            res.append(x)
            break

#print "result:", res




"""
test quiz
"""
f = open('inputForLuhn.txt','r')
l = []
for line in f:
    line = line[:-1]
    l.append(line)
#print "test read", l[0]

newRes = []
sol = 0
for i in range(0,len(l)):

    for x in range(0,10):

    #if Luhn('7992739871X', x):
        if Luhn(l[i],x ):
#            print ("result:", x)
            newRes.append(x)
            sol = sol*10 + x
            break
print ("result:", newRes, "\nsol:", sol)
