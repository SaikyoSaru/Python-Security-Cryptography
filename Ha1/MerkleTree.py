import numpy as np
import formulas as form


f = open('inputSpv.txt','r')
l = ''


for line in f:
    if line[0] == 'R':
        l = l + line[1:-1]
        l = form.toSha1(l)
    elif line[0] == 'L':
        l = line[1:-1] + l
        l = form.toSha1(l)
    else:
        l += line[:-1]

print  ("Merkel root:", l)

f.close()

def merkelTree(i,j,leaves):

    #path = []
    return recMerk(leaves)


def recMerk(i,j,leaves):
    new = []
    if (len(leaves) == 1):
        return leaves[0]

    if len(leaves)%2 != 0:
        leaves.append(leaves[len(leaves)-1])
    ch = (i-1 if i%2 else i+1)
    path.append((('L' if (i%2) else 'R') + leaves[ch]))
    i = int(round(i/2))
    for k in range(0, len(leaves), 2):
        new.append(form.toSha1((leaves[k] + leaves[k+1])))
    return recMerk(i, j, new)


g = open('inputMerkleTree.txt', 'r')

path = []
leaves = g.readlines()
g.close()
i = int(leaves[0])
j = int(leaves[1])

leaves = [x.strip() for x in leaves]

leaves = leaves[2:]
print ("merkleroot:", recMerk(i, j, leaves))
print ("full path:", path)
print ("path node at level",j,":", path[len(path)-j])
