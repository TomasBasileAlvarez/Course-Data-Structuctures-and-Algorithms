'''
Bidirectional dijkstra (con lista de adyacencia )
import numpy as np
from math import *
import sys, threading
sys.setrecursionlimit(10**9) # max depth of recursion
threading.stack_size(2**27) 
import queue
import copy

class nodos:
    #cada nodo tiene sus conexiones y tiene una distancia inicializada en infinito
    #tambien tienen la propiedad de previo, que es el vector anterior en el camino
    # y el self.vis dice si fue visitado o no.
    def __init__(self, ind, conex):
        self.conex = conex
        self.ind = ind
        self.dist = inf
        self.vis = 0
        self.prev = None
        
    #El m\'etodo lt define cual sera la funcion less than al comparar
    #dos objetos de la clasr (para que al usar funciones como min, max,
    #sort, el programa sepa que criterio de less than usar.
    #dice que un nodo es menot que otro si la distancia dist es menor

    def __lt__(self, other):
        return self.dist < other.dist



# tomamos los numeros n y m del input
n , m = [int(x) for x in input().split()]

# luego, nos dan los m ejes direccionados  con los pesos
#definimos el array de los nodos con conexiones por ahora vacias y el grafo inverso
# con las conexiones tambien vacias
grafo_o = [nodos(i,[]) for i in range(n)]
grafo_r_o = [nodos(i,[]) for i in range(n)]


#para cada entrada de los ejes
for i in range(m):
    p , q , c = [int(x) for x in input().split()]
    #creamos una conexion de p a q en el grafo de ida y con peso c. 
    #Es decir, las conexiones contenienen un array de dos elementos con la direccion a la que 
    #conectan y el peso.
    #el grafo inverso tiene las conexiones al rev'es. 
    grafo_o[p-1].conex.append([q-1,c])
    grafo_r_o[q-1].conex.append([p-1,c])
    
    
    
    
    
    
#dado un grafo y su grafo inverso, y el indice inicial y final, va a dar el camino y distancia
def bidij(grafo_o,grafo_r_o, princ, fin):
    
    grafo = copy.deepcopy(grafo_o)
    grafo_r = copy.deepcopy(grafo_r_o)
    
    if princ == fin:
        return([0,princ])
    mu = np.inf
    # el primer vertice tiene una distancia 0.
    grafo[princ].dist = 0
    #el primer vertice del camino inverso tambien tiene una distancia 0.
    grafo_r[fin].dist = 0
    

    #creamos una priorityQueue, que es beuna para sacar minimos de una lista
    pq = queue.PriorityQueue()
    #y creamos una pq para el camino inverso.
    pq_r = queue.PriorityQueue()
    
    #ponemos el nodo desde el que empezamos en el camino directo y en el inverso.
    #en pq ponemos el nodo, no el indice. 
    pq.put(grafo[princ])
    pq_r.put(grafo_r[fin])
    
    
    while not pq.empty() and not pq_r.empty():
        #sacamos el elemento minimo (el de menor distancia)
        # que es el que sabemos que su distancia ya est'a fija seg'un el algoritmo.
        u = pq.get()
        u_r = pq_r.get()
        # lo hacemos tanto en el camino directo como en el inverso.
        
        #print("u",u.ind)
        #marcamos que u ya est'a visitado en graf
        #y que u_r est'a visitado en graf_r
        u.vis = 1
        u_r.vis=1


        # vamos a ir recorriendo las conexiones de u
        for i in range(len(u.conex)):
            
            # vamos viendo las conexiones de u.
            #v es el indice del nodo al que u est'a conectado
            v = u.conex[i][0]
            

            #si la distancia actual que tiene el nodo v es mayor que la distancia que 
            #tendria si pasamos por u y le sumamos el costo de ir desde u hasta v,
            if grafo[v].dist > u.dist + u.conex[i][1]:
                
                #entonces, relajamos la distancia de v, y marcamos que se lleg'o a v desde u.ind
                grafo[v].dist = u.dist + u.conex[i][1]
                grafo[v].prev = u.ind
                # y ponemos este vertice en el queue para revistalo despues
                pq.put(grafo[v])
                
            if grafo_r[v].vis == 1:
                if u.dist+ u.conex[i][1] + grafo_r[v].dist < mu:
                    mu =  u.dist+ u.conex[i][1] + grafo_r[v].dist
                    mejorconex=[u.ind,v]
        
        #hacemos lo mismo para el camino inverso.
        for i in range(len(u_r.conex)):
            v = u_r.conex[i][0]
            
            
            if grafo_r[v].dist > u_r.dist + u_r.conex[i][1]:
                
                
                grafo_r[v].dist = u_r.dist + u_r.conex[i][1]
                grafo_r[v].prev = u_r.ind
                
                
                pq_r.put(grafo_r[v])
                
            if grafo[v].vis == 1:
                if u_r.dist+ u_r.conex[i][1] + grafo[v].dist < mu:
                    mu =  u_r.dist+ u_r.conex[i][1] + grafo[v].dist
                    mejorconex=[v,u_r.ind]
        
        
        #si el u que acabamos de visitar tiene un indice que ya fue visitado por el camino de regreso
        #significa que el camino de ida y de vuelta ya intersectaron
        if grafo_r[u.ind].vis == 1:
            return([mu,-1])
            #return(shortestpath(princ,proc,proc_r,fin,mejorconex,mu))
            break

    return([-1,-1])


def shortestpath(princ,proc,proc_r,fin,mejorconex,mu):
    path = []
    lastida = mejorconex[0]    

    
    while lastida != princ:
        path.append(lastida)       
        lastida = grafo[lastida].prev
    path.append(princ)
    path.reverse()
    
    
    
    lastreg = mejorconex[1]
    path.append(lastreg)
    
    while lastreg != fin:
        lastreg = grafo_r[lastreg].prev
        path.append(lastreg)
    
    return(mu,path)

#princ = 0
#fin = 4
#print(bidij(grafo,grafo_r,princ,fin))

#q es el nunmero de queries
q = int(input())

for m in range(q):
    princ, fin = [int(x)-1 for x in input().split()]
    res = bidij(grafo_o,grafo_r_o,princ,fin)
    print(res[0])
    #print(res[1])
'''


''' solucion a partir de la solucion de dijsktra mejor de week 4'''




''' Bidirectional dijkstra (con lista de adyacencia )'''
import numpy as np
from math import *
import sys, threading
sys.setrecursionlimit(10**9) # max depth of recursion
threading.stack_size(2**27) 
import queue




class nodos:
    #cada nodo tiene sus conexiones y tiene una distancia inicializada en infinito
    #tambien tienen la propiedad de previo, que es el vector anterior en el camino
    # y el self.vis dice si fue visitado o no.
    def __init__(self, ind, conex, tipo):
        self.conex = conex
        self.ind = ind
        self.tipo = tipo        
    
    def __lt__(self, other):
        if self.tipo == 0:
            return dist[self.ind] < dist[other.ind]
        else:
            return dist_r[self.ind] < dist_r[other.ind]



n , m = [int(x) for x in input().split()]


grafo = [nodos(i,[],0) for i in range(n)]
grafo_r = [nodos(i,[],1) for i in range(n)]


for i in range(m):
    p , q , c = [int(x) for x in input().split()] 
    grafo[p-1].conex.append([q-1,c])
    grafo_r[q-1].conex.append([p-1,c])
    

def bidij(grafo,grafo_r,n, princ, fin):
    
    global dist
    dist = n*[np.inf]
    global vis
    vis = n*[0]
    global dist_r
    dist_r = n*[np.inf]
    global vis_r
    vis_r = n*[0]
    
    dist[princ] = 0
    dist_r[fin] = 0
    
    vis[princ] = 1
    vis_r[fin] = 1
    
    if princ == fin:
        return(0)
    
    
    pq = queue.PriorityQueue()
    pq_r = queue.PriorityQueue()
    
    
    mu = np.inf
    # el primer vertice tiene una distancia 0.
    
    

    
    #ponemos el nodo desde el que empezamos en el camino directo y en el inverso.
    #en pq ponemos el nodo, no el indice. 
    pq.put(grafo[princ])
    pq_r.put(grafo_r[fin])
    
    
    while not pq.empty() or not pq_r.empty():
        #sacamos el elemento minimo (el de menor distancia)
        # que es el que sabemos que su distancia ya est'a fija seg'un el algoritmo.
        u = pq.get()
        u_r = pq_r.get()
        # lo hacemos tanto en el camino directo como en el inverso.
        
        #print("u",u.ind)
        #marcamos que u ya est'a visitado en graf
        #y que u_r est'a visitado en graf_r
        vis[u.ind] = 1
        vis_r[u_r.ind] = 1


        # vamos a ir recorriendo las conexiones de u
        for i in range(len(u.conex)):
            
            # vamos viendo las conexiones de u.
            #v es el indice del nodo al que u est'a conectado
            v = u.conex[i][0]
            

            #si la distancia actual que tiene el nodo v es mayor que la distancia que 
            #tendria si pasamos por u y le sumamos el costo de ir desde u hasta v,
            if dist[v] > dist[u.ind] + u.conex[i][1]:
                
                #entonces, relajamos la distancia de v, y marcamos que se lleg'o a v desde u.ind
                dist[v] = dist[u.ind] + u.conex[i][1]
                # y ponemos este vertice en el queue para revistalo despues
                
                if vis[v] == 0:
                    pq.put(grafo[v])
                    vis[v] = 1
                
            if vis_r[v] == 1:
                if dist[u.ind] + u.conex[i][1] + dist_r[v] < mu:
                    mu = dist[u.ind] + u.conex[i][1] + dist_r[v]
                    mejorconex=[u.ind,v]
        
        #hacemos lo mismo para el camino inverso.
        for i in range(len(u_r.conex)):
            v = u_r.conex[i][0]
            
            
            if dist_r[v] > dist_r[u_r.ind] + u_r.conex[i][1]:
                
                dist_r[v] = dist_r[u_r.ind] + u_r.conex[i][1]
                
                if vis_r[v] == 0:
                    pq_r.put(grafo_r[v])
                    vis_r[v]= 1
                
                
            if vis[v] == 1:
                if dist_r[u_r.ind] + u_r.conex[i][1] + dist[v] < mu:
                    mu = dist_r[u_r.ind] + u_r.conex[i][1] + dist[v]
                    mejorconex=[v,u_r.ind]
        
        
        #si el u que acabamos de visitar tiene un indice que ya fue visitado por el camino de regreso
        #significa que el camino de ida y de vuelta ya intersectaron
        if vis_r[u.ind] == 1 or vis[u_r.ind] == 1:
            return(mu)
            break

    return(-1)

q = int(input())

for m in range(q):
    princ, fin = [int(x)-1 for x in input().split()]
    res = bidij(grafo,grafo_r,n,princ,fin)
    print(res)
    








