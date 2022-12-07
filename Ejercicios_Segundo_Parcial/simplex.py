
def max_value(a):
    max = -1000000
    for i in range(len(a)):
        if max < a[i] and a[i] > 0:
            max = a[i]
    return max

def max_index(a):
    max = -10000000
    index = 0
    for i in range(len(a)):
        if max < a[i] and a[i] > 0:
            max = a[i]
            index = i
    return index

def min_index(a):
    min = 10000000
    index = 0
    for i in range(len(a)):
        if min > a[i] and a[i] > 0:
            min = a[i]
            index = i
    return index

def base_index(a):
    base = []
    for i in range(len(a)):
        if a[i] == 0:
            base.append(i)
    return base

def replace(a,k,r):
    for i in range(len(a)):
        if a[i] == k:
            a[i] = r
    return a

def simplex(A,b,c):
    indexes = base_index(c)
    print(indexes)
    while(max(c) > 0):
        #determinamos la variable que entra con indice k
        k = max_index(c)
        #temp {b/a}
        temp = []
        for i in range(len(A)):
            temp.append(b[i]/(A[i][k]))
        #hacemos una matriz temporal para poder calcular r
        r = min_index(temp)
        #Pivoteamos las restricciones y el costo
        #Pivote
        pivot = A[r][k]
        #Modificamos la fila r
        for i in range(len(A[r])):
            A[r][i] = A[r][i] / pivot
        b[r] = b[r] / pivot
        #Actualizamos las demas filas
        for i in range(len(A)):
            if i == r:
                continue
            temp = []
            temp2 = []
            #Actualizamos b
            b[i] = b[i] - (b[r] * A[i][k])
            #Actualizamos A
            for x in range(len(A[r])):
                temp.append(A[r][x] * A[i][k])
                temp2.append(A[r][x] * c[k])
            for j in range(len(A[i])):
                A[i][j] = A[i][j] - temp[j]
            #Actualizamos c
            for j in range(len(c)):
                c[j] = c[j] - temp2[j]
        #Modificamos los indices 
        print("k=",k)
        print("r=",r)
        replace(indexes,k,r)
        print(indexes) 
    return indexes,b

A = [[1.0,1.0,1.0,1.0,0.0,0.0],[2.0,1.0,-1.0,0.0,1.0,0.0],[-1.0,3.0,0.0,0.0,0.0,1.0]]
b = [12.0,6.0,9.0]
c = [1.0,-2.0,1.0,0.0,0.0,0.0]
base,sol = simplex(A,b,c)
print("Base:",base)
print("Solucion:",sol)