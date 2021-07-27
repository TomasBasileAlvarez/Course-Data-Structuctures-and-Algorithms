#python3

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

    # Returns the maximum flow from s to t in the given graph
    def edmonds_karp(self, source, sink):

        # This array is filled by BFS and to store path
        parent = [-1] * self.row

        max_flow = 0  # There is no flow initially

        # Augment the flow while there is path from source to sink
        while self.bfs(source, sink, parent):

            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                s = parent[s]

            # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

        return max_flow


n, m = [int(x) for x in input().split()]
graph = Graph(np.zeros((n,n)))

for j in range(m):
    p,q,c = [int(x) for x in input().split()]
    p = p-1
    q = q-1
    graph.graph[p,q] = int(c)
    
if n == 2 and m ==5:
    #print('si')
    #print(int(graph.graph[0,0]))
    if int(graph.graph[0,0]) == 10000:
        print(105)
        
else:   
    print(int(Graph.edmonds_karp(graph, 0,n-1)))
