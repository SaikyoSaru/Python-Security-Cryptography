import numpy as np
"""
Luhns algorithm
param:
______
input: credit card number
x : the bit that is unknown
"""
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
