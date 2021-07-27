#python3

# creamos una variable x_{ij} que es true si el nodo i est'a coloreado con 
#el color j 1<=j<= 3. 
import itertools
import os


n , m = [int(x) for x in input().split()]


conexiones =[]
for i in range(m):
    p,q = [int(x) for x in input().split()]
    conexiones.append((p,q))



clauses=[]
digits = [1,2,3]


def varnum(i,j):
    assert(j in digits)
    return (j-1)*n+i


def exactly_one_of(literals):
    clauses.append([l for l in literals])
    
    for pair in itertools.combinations(literals,2):
        clauses.append([-l for l in pair])

# cada nodo tiene exactamente un color
for i in range(1,n+1):
    exactly_one_of([varnum(i,j) for j in digits])
    
#dos vertices juntos no son del mismo color    
for i in range(m):
    p,q = conexiones[i]
    clauses.append([  -p, -q])    
    clauses.append([-n - p,-n - q])    
    clauses.append([-2*n - p,-2*n -q])    
    

l = len(clauses)
v = 3*n
res =[l,v]

def imprime(clauses):
    print(*res)
    for i in range(l):
        clauses[i].append(0)
        print(*clauses[i])

imprime(clauses)
