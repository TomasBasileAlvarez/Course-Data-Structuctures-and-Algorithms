#python3
''' hacemos basicamente lo mismo que en el anterior, solo que todos los pesos son 1
y agregamos un source y un sink'''
''' Ademas, al confirmar un flow, ya tenemos asignado un cierto crew para un cierto vuelo
por lo que vamos a guardar una lista de asignados'''

import collections
import numpy as np
''' Usamos adjacency matrix porque son pocos nodos (100) y entonces tiene un tamano max de 10,000'''
class Graph:
    """This class represents a directed graph using adjacency matrix representation."""

    def __init__(self, graph):
        #definimos un grafo y su row es la longitud
        # el grafo est'a en la representacion de matriz. En la graph(i,j) se pone la capacidad que 
        # conecta el eje i al eje j. 
        self.graph = graph  # residual graph
        self.row = len(graph)

        
    def bfs(self, s, t, parent):
        # bfs hace una busqueda bfs del grafo desde s hasta t. 

        
        # Primero marcamos todos los grafos como no visitados.
        visited = [False] * self.row

        # Creamos una queue que vamos a usar para el algoritmo. 
        queue = collections.deque()

        
        # Marcamos el source como visitado y lo agregamos al queue para explorarlo
        queue.append(s)
        visited[s] = True

        # Vamos revisando los adyacentes y agregandolos a la queue.
        while queue:
            # primero hay que sacar el primer elemento del queue (que es el que fue agregado
            # antes).
            u = queue.popleft()

            # va viendo la adyacencia de el nodo u
            # ind es el indice del nodo que est'a buscando y val ser'a la capacidad del eje que va del 
            #nodo u al nodo ind. 
            for ind, val in enumerate(self.graph[u]):
                #si se trata de un nodo no visitado a'un y que sea un eje que tenga un valor
                # lo visita y lo agrega al queue para explorarlo despues. Adem;as, pone que el padre
                # de ind es u. 
                if (visited[ind] == False) and (val > 0):
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        # If we reached sink in BFS starting from source, then return
        # true, else false
        return visited[t]

    #edmonds karp da el mayor flow desde source hasta sink
    def edmonds_karp(self, source, sink):
        
        # primero creamos el array de parents inicializado en -1
        parent = [-1] * self.row
        global asignado
        asignado = [-1] * self.row
        #el max_flow inicial es 0
        max_flow = 0

        #mientras haya un flow desde source hasta sink (en el grafo recidual), vamos aumentando 
        #el flow maximo
        #aplicamos el bfs a nuestro grafo desde source hasta sink, lo que actualiza el array
        #parent
        while self.bfs(source, sink, parent):

            
            # encontramos un flow desde source hasta sink en el residual actual
            #iniciamos la variable path flow, en la que pondremos el flujo de este camino residual
            path_flow = float("Inf")
            #s es el sink
            s = sink
            
            # vamos recorriendo el camino que encontr'o bfs al reves hasta llegar al source
            # y tenemos que guardar el valor del eje con minima capacidad. 
            #que es el valor que le vamos a dar al flow
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            #Agregamos este flow encontrado al max flow, seg'un la regla |f+g| = |f|+|g| 
            #vista en las notas
            max_flow += path_flow

            # tenemos que actualizar los ejes del grafo residual
            #empezamos de nuevo en el sink
            v = sink
            while v != source:
                #y vamos recorriendo hasta llegar al source
                #Disminuimos el flujo de ida y creamos un flujo de regreso.
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                asignado[u] = v
                v = parent[v]
        return max_flow


#inicializamos el grafo
n, m = [int(x) for x in input().split()]
#el grafo tiene n+m+2 elementos
graph = Graph(np.zeros((n+m+2,n+m+2)))

#conectamos el source con todos los crew
for i in range(1,n+1):
    graph.graph[0,i] = 1
    
#conectamos los vuelos con el sink
for i in range(n+1,n+m+1):
    graph.graph[i,n+m+1]=1

#creamos la matriz de adyacencia en el grafo.
for j in range(1,n+1):
    inpu = [int(x) for x in input().split()]
    for k in range(m):
        if inpu[k] == 1:
            graph.graph[j][n+1+k]=1


            
Graph.edmonds_karp(graph, 0,n+m+1)

res = []

for i in range(1,n+1):
    if asignado[i] != -1:
        res.append(asignado[i]-n)
    else:
        res.append(-1)
print(*res)
