
import numpy as np

def is_candidate(c):
    for i in range(len(c)):
        if c[i] > 0:
            return False
    return True

def is_optimal(b):
    for i in range(len(b)):
        if b[i] < 0:
            return False
    return True

def pivot_row(b):
    if is_optimal(b):
        return -1
    index = 0
    min = np.inf
    for i in range(len(b)):
        if b[i] < min and b[i] < 0:
            min = b[i]
            index = i
    return index

def is_unfeasible(a):
    temp = 0
    for i in range(len(a)):
        if a[i] >= 0:
            temp += 1
    if temp == len(a):
        return True
    return False

def pivot_column(a,c):
    if is_unfeasible(a):
        return -1
    index = 0
    min = np.inf
    for i in range(len(a)):
        if a[i] >= 0:
            continue
        ratio = c[i]/a[i]
        if ratio < min and a[i] < 0:
            min = ratio
            index = i
    return index

def pivot(A,b,c,r,k):
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
        #creamos dos listas temporales para poder hacer la resta
        for x in range(len(A[r])):
            temp.append(A[r][x] * A[i][k])
            temp2.append(A[r][x] * c[k])
        #Actualizamos A
        for j in range(len(A[i])):
            A[i][j] = A[i][j] - temp[j]
        #Actualizamos c
        for j in range(len(c)):
            c[j] = c[j] - temp2[j]
    return A,b,c

def dual_simplex(A,b,c):
    while(pivot_row(b) != -1):
        r = pivot_row(b)
        if pivot_column(A[r],c) == -1:
            print("No hay solucion")
            break
        k = pivot_column(A[r],c)
        A,b,c = pivot(A,b,c,r,k)
    return b

    
A = [[-1.0,-2.0,-1.0,1.0,0.0],[-2.0,1.0,-3.0,0.0,1.0]]
b = [-3.0,-4.0]
c = [-2.0,-3.0,-4.0,0.0,0.0]
print(dual_simplex(A,b,c))