#python3
''' Gauss Jordan convertir a row echelon'''
import numpy as np

def swap(matriz,i,j):
    ''' swapea el renglon i y el j de la matriz'''
    matriz[i] , matriz[j] = matriz[j] , matriz[i]

def multiplica(matriz,i,c):
    '''Multiplica el renglon i por c'''
    matriz[i] = [x*c for x in matriz[i]]

def suma(matriz,i,j,c):
    '''le suma al renglon j el renglon i'''
    listoflists = [[x*c for x in matriz[i]],matriz[j]]
    matriz[j] = [sum(x) for x in zip(*listoflists)]




def encuentrapivote(matriz,pivotes,n,m):
    #encuentra el renglon del siguiente pivote, dado que ya encontramos n pivs
    # lo que hace es encontrar el renglon con la menor cantidad de 0s
    #por ahora, la menor cantidad es tener infinitos 
    mejor = np.inf
    #checa todos los renglones que no son pivotes(los pivotes ya los puso hasta arriba)
    for i in range(pivotes,n):
        #empieza en el iesimo renglon en el pivotesimo columna (porque ya sabe que todas
        #las columnas a la izquierda deben de ser ceros)
        j = pivotes
        #mientras tengamos un 0
        while j<m and matriz[i][j] == 0:
            #vamos aumentando la j (recorremos hacia la derecha)
            j=j+1
            if j ==m-1:
                return(-1)
                break
        #eventualmente, llegamos al primer no cero. Entonces, j cont'o la cantidad de ceros
        #desde la columna pivotesima. 
        #si el i-esimo renglon tiene menos 0s que el mejor, actualiza el mejor y el ind que vamos 
        # a imprimir
        if j < mejor:
            mejor =j 
            ind = i
        #si no hubo ningun 0 a la derecha de los pivotes, ya acabamos, pues este renglon es el 
        #pivote
        if j == pivotes:
            #imprimimos el renglon y la columna del pivote
            return((i,j))
    #imprimos el renglon y la columna del pivote
    return((ind, mejor))


def echelon(matriz,n,m):
    pivotes= 0
    i=0
    while i < n and pivotes<n:
        #print('nuevo')
        #nuevopiv tiene la posicion del nuevo piv
        #print('cantidad de piv', pivotes)
        #print('matriz-:', matriz)
        nuevopiv = encuentrapivote(matriz,pivotes,n,m+1)
        

        if nuevopiv == -1:
            #print('fin')
            return(matriz)
        #print('nuevopiv',nuevopiv[0],nuevopiv[1])
        #print('cantidad de pivs:', pivotes)
        #print(matriz)
        swap(matriz,nuevopiv[0],pivotes)    
        #print(matriz)
        
        escalar = matriz[nuevopiv[0]][nuevopiv[1]]
        
        if escalar != 0:
            multiplica(matriz,pivotes, 1/escalar)
            pivotes = pivotes+1
            
            #print("cantidad de pivos", pivotes)
            #print(matriz)
        
            for j in range(0,n):
                if matriz[j][nuevopiv[1]] != 0 and j != pivotes-1:
                    suma(matriz,pivotes-1,j,-matriz[j][nuevopiv[1]])
                    #print(nuevopiv[0],nuevopiv[1])
                    #print(pivotes)
                    #print(matriz)
        i=i+1
    return(matriz)
        

    

n = int(input())
m=n
if n ==0:
    print('')
else:
    matriz= np.zeros((n,n+1))
    for i in range(n):
        res=[int(x) for x in input().split()]
        for j in range(len(res)):
            matriz[i,j]=res[j]

    matriz = matriz.transpose()

    resul = matriz[-1]
    matriz = np.delete(matriz,n,0)


    matriz = matriz.transpose()

    x = np.linalg.solve(matriz,resul)
    print(*x) 
    
    
 
