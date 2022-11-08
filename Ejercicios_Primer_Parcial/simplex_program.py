import math
import numpy as np

def to_tableau(c, A, b):
    #introduce el valor a utilizar
    xb = [eq + [x] for eq, x in zip(A, b)]
    print(xb)
    z = c + [0]
    print(z)
    return xb + [z]
def can_be_improved(tabla):
    z = tabla[-1]
    
    return any(x > 0 for x in z[:-1])

def get_pivot_position(tabla):
    z = tabla[-1]
    column = next(i for i, x in enumerate(z[:-1]) if x > 0)
    
    restrictions = []
    for eq in tabla[:-1]:
        el = eq[column]
        restrictions.append(math.inf if el <= 0 else eq[-1] / el)

    row = restrictions.index(min(restrictions))
    return row, column
def pivot_step(tabla, pivot_position):
    nueva_tabla = [[] for eq in tabla]
    
    i, j = pivot_position
    pivot_value = tabla[i][j]
    nueva_tabla[i] = np.array(tabla[i]) / pivot_value
    
    for eq_i, eq in enumerate(tabla):
        if eq_i != i:
            #aqui se pone el multiplicador de cada uno de los pasos de pivoteo
            multiplicador = np.array(nueva_tabla[i]) * tabla[eq_i][j]
            nueva_tabla[eq_i] = np.array(tabla[eq_i]) - multiplicador
   
    return nueva_tabla
def is_basic(columna):
    return sum(columna) == 1 and len([c for c in columna if c == 0]) == len(columna) - 1

def get_solution(tabla):
    columns = np.array(tabla).T
    soluciones = []
    for column in columns:
        solucion = 0
        if is_basic(column):
            one_index = column.tolist().index(1)
            solucion = columns[-1][one_index]
        soluciones.append(solucion)
        
    return soluciones
def simplex(c, A, b):
    tabla = to_tableau(c, A, b)

    while can_be_improved(tabla):
        pivot_position = get_pivot_position(tabla)
        tabla = pivot_step(tabla, pivot_position)

    return get_solution(tabla)
