import numpy as np

MAX_MODE = 'MAX'
MIN_MODE = 'MIN'


class SimplexMethod:
    def __init__(self, c, a, b, mode):  
        # 2 variable  # number of variables #shape given the number of columns of numpy array
        # 2 variables # numero de variables #shape da el numero de columnas de un array de numpy
        self.main_variables_count = a.shape[1]
        # 4 restricciones  # numero de restriciones
        self.restrictions_count = a.shape[0]
        self.variables_count = self.main_variables_count + \
            self.restrictions_count  # 6  # numero de variables
        self.mode = mode  # recordamos el modelo de operacion
        # coficiente de las funciones
        self.c = np.concatenate([c, np.zeros((self.restrictions_count + 1))])
        # valores de la funcion F (zj-cj)
        self.f = np.zeros((self.variables_count + 1))
        # indices de las variables basicas
        self.basis = [
            i + self.main_variables_count for i in range(self.restrictions_count)]
        #(0+2,1+2,2+2,3+2)

        self.init_table(a, b)

    # Inicializar la tabla
    def init_table(self, a, b):
        # coeficiente de tabla 4x7
        self.table = np.zeros(
            (self.restrictions_count, self.variables_count + 1))
       #insertar los valores de a en la tabla
        for i in range(self.restrictions_count):
            for j in range(self.main_variables_count):
                self.table[i][j] = a[i][j]

            for j in range(self.restrictions_count):
                # variables artificiales
                self.table[i][j + self.main_variables_count] = int(i == j)
                self.table[i][-1] = b[i]

  
    # obtener un string para la fila con el valor de b mas negativo
    def get_negative_b_row(self):  # que variable?
        row = -1
        for i, a_row in enumerate(self.table):
            if a_row[-1] < 0 and (row == -1 or abs(a_row[-1]) > abs(self.table[row][-1])):
                row = i
        return row

    # obteniendo una columna con el elemento de modulo maximo en una fila
    
    # dejando variable col la mas negativa
    def get_negative_b_column(self, row):
        column = -1

        for i, aij in enumerate(self.table[row][:-1]):
            if aij < 0 and (column == -1 or abs(aij) > abs(self.table[row][column])):
                column = i

        return column

   
    # remover los coeficientes libres negativos
    def remove_negative_b(self):
        while True:
            row = self.get_negative_b_row()  #estamos buscando una fila que contenga un b negativo
            if row == -1: # si no hay ninguno
                return True # exito

            # buscnado una columna permissive
            column = self.get_negative_b_column(row)

            if column == -1:
                return False  # fallido para borrar
            self.gauss(row, column)  # aplicando el metodo de gauss
            self.calculate_f()
            print('\nLeaving variable has been removed in row:', row + 1)
            self.print_table()


    def gauss(self, row, column):  # column --> leaving variable row -->entering variable
        # self.table[row][column] - pivot element
        self.table[row] /= self.table[row][column]
        #self.table[row] - leaving var row
        for i in range(self.restrictions_count):
            if i != row:  # neglecting the leaving variable row
                # entering variable ooda corresponding col
                self.table[i] -= self.table[row] * self.table[i][column]

        # changing the the variable number in table based on leaving and entering variable
        self.basis[row] = column

    # calculation of F values

    def calculate_f(self):
        for i in range(self.variables_count + 1):
            self.f[i] = -self.c[i]

            for j in range(self.restrictions_count):
                self.f[i] += self.c[self.basis[j]] * self.table[j][i]

    # calculation of simplex relations for column column

    def get_relations(self, column):
        q = []

        for i in range(self.restrictions_count):
            if self.table[i][column] == 0:
                # if any value results in infinity we return it and stop
                q.append(np.inf)

            else:
                q_i = self.table[i][-1] / \
                    self.table[i][column]  # ratio calculation
                q.append(q_i if q_i >= 0 else np.inf)

        return q

    # obteniendo la solucion
    def get_solve(self):
        y = np.zeros((self.variables_count))

        # llena los valores de las variables basicas
        for i in range(self.restrictions_count):
            y[self.basis[i]] = self.table[i][-1]

        return y

    # decision
    def solve(self):
        print('\nIteration 0')
        self.calculate_f()
        self.print_table()

        if not self.remove_negative_b():  # if the b value is not there then it is infeasible
            print('Solve does not exist')
            return False

        iteration = 1

        while True:
            self.calculate_f()
            print('\nIteration', iteration)
            self.print_table()

            # if the plan is optimal
            if all(fi >= 0 if self.mode == MAX_MODE else fi <= 0 for fi in self.f[:-1]):
                break  # then we finish the work

            column = (np.argmin if self.mode == MAX_MODE else np.argmax)(
                self.f[:-1])  # we get the resolving column
            # we get simplex relations for the found column
            q = self.get_relations(column)

            if all(qi == np.inf for qi in q):  # if the resolving string could not be found
                # we inform you that there is no solution
                print('Solve does not exist')
                return False

            self.gauss(np.argmin(q), column)  # performing a Gaussian exception
            iteration += 1

        return True  # there is a solution

    # simplex table output
    def print_table(self):
        print('     |' + ''.join(['   y%-3d |' % (i + 1)
              for i in range(self.variables_count)]) + '    b   |')

        for i in range(self.restrictions_count):
            print('%4s |' % ('y' + str(self.basis[i] + 1)) + ''.join(
                [' %6.2f |' % aij for j, aij in enumerate(self.table[i])]))

        print('   F |' + ''.join([' %6.2f |' % aij for aij in self.f]))
        print('   y |' + ''.join([' %6.2f |' % xi for xi in self.get_solve()]))

    # coefficient output #horizontal y1,y2,y3,...
    def print_coef(self, ai, i):
        if ai == 1:
            return 'y%d' % (i + 1)

        if ai == -1:
            return '-y%d' % (i + 1)

        return '%.2fy%d' % (ai, i + 1)

    # salida de la tarea
    def print_task(self, full=False):
        print(' + '.join(['%.2fy%d' % (ci, i + 1) for i, ci in enumerate(
            self.c[:self.main_variables_count]) if ci != 0]), '-> ', self.mode)

        for row in self.table:
            if full:
                print(' + '.join([self.print_coef(ai, i) for i, ai in enumerate(
                    row[:self.variables_count]) if ai != 0]), '=', row[-1])
            else:
                print(' + '.join([self.print_coef(ai, i) for i, ai in enumerate(
                    row[:self.main_variables_count]) if ai != 0]), '<=', row[-1])


# traduciendo a una tarea dual


def make_dual(a, b, c):
    return -a.T, -c, b


c = np.array([1, -7, 10, -3])  # RHS
a = np.array([
    [1, -1, 1, 0],
    [1, -1, 2, -1]
])

b = np.array([-3, -2])  # objective fn

a, b, c = make_dual(a, b, c)  # turned into a dual task
simplex = SimplexMethod(c, a, b, MAX_MODE)  # turn into max mode

print("Dual task:")
simplex.print_task()
simplex.solve()
