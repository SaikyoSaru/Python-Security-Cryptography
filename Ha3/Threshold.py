import sys

def simpLagrange(x,y):
    res = 0
    for i in range(len(y)):
        s = 1
        for j in range(len(y)):
            if i == j:
                continue
            s *= (x[j])/(x[j] - x[i])
        res += y[i]*s
    return res

def treshold(k, n, privPol, polShares, x, y):
    if (len(x) < k ):
        print("too few participants!!, get more friends!")
        sys.exit()

    f1 = sum(privPol) + sum(polShares)
    y.insert(0,f1)
    simp = simpLagrange(x,y)
    return simp


f1 = [15, 14, 18, 13, 6]
polShares = [38, 67, 65 ,67, 63]
x = [1, 2, 3, 5, 6]
y = [1963, 7468, 48346, 96691]

print ("result:", treshold(5,6, f1, polShares, x ,y))
