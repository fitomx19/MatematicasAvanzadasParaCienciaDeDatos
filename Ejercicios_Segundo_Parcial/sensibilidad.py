import simplex
import dualsimplex
import numpy as np

def is_basic(x):
    if x == 0:
        return True
    return False

#cambio en la funcion costo
def change_cost(A, b, c, x, index):
    if is_basic(c[index]):
        c[index] = c[index] + (c[index] - x)
        simplex.simplex(A, b, c)
    else:
        for j in range(len(c)):
            if j != index:
                c[j] = c[j] + (x - c[index]) * (A[index][j])
        c[index] = x
        simplex.simplex(A, b, c)

#cambio en la funcion b
def still_optimal(B):
    for i in range(len(B)):
        if B[i] < 0:
            return False
    return True

def change_b(A, b, c, new_b, B):
    basic = np.dot(np.linalg.inv(B),new_b)
    if still_optimal(basic):
        return A, basic, c, 
    else:
        dualsimplex.dual_simplex(A, basic, c)
