import time

import numpy as np


class GridSquare2D:
    width: int
    height: int
    cells: np.array

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = np.zeros((height, width), dtype=int)  # изменить, чтобы сам создавал нужный массив

    # Устанавливает случайные значения в матрицу
    def set_random(self):
        self.cells = np.random.randint(2, size=(self.height, self.width))  # изменить, чтобы сам создавал нужный рандом

    def clear(self):
        self.cells = np.zeros((self.height, self.width), dtype=int)

    def set_point(self):
        i = self.height//2
        j = self.width//2
        self.cells[i][j] = 1
        self.cells[i][j-1] = 1
        self.cells[i][j+1] = 1

    def get_neighbors_moore(self, x, y):
        live_neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (y + j) == self.width:
                    j = -1
                if (x + i) == self.height:
                    i = -1
                if self.cells[x + i][y + j] == 1 and not (i == 0 and j == 0):
                    live_neighbors += 1
        return live_neighbors

    def next_gen(self, n=1):
        def gen():

            new_cells = np.zeros((self.height, self.width), dtype=int)
            ftime = 0.0
            for i in range(self.height):
                for j in range(self.width):
                    # проход для каждой клетке
                    #stime = time.time()
                    neighbors = self.get_neighbors_moore(i, j)
                    #etime = time.time() - stime
                    #ftime += etime
                    cur_status = self.cells[i][j]
                    new_status = 0
                    if cur_status == 1 and (neighbors == 3 or neighbors == 2):
                        new_status = 1
                    else:
                        if neighbors == 3 and cur_status == 0:
                            new_status = 1
                    new_cells[i][j] = new_status  # изменить правило

            self.cells = new_cells

            #print(ftime)

        for i in range(n):
            gen()

    def print(self):
        cells_list = self.cells.tolist()
        res = ''
        for i in cells_list:
            i = map(lambda x: str(x), i)
            res = res + ''.join(i) + '\n'
        print(res)

    def getCellStatus(self, x, y):
        return self.cells[x][y]
