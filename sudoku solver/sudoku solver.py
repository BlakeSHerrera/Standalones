#sudoku solver.py

from time import sleep
from mouse import *
import itertools

data = '''
?17|??8|94?
?84|???|???
??3|?2?|???
---+---+---
8??|?7?|??2
?2?|???|?6?
7??|?3?|??4
---+---+---
???|?9?|4??
???|???|61?
?79|1??|38?
'''

class Sudoku:

    def __init__(self, data, n):
        data2 = [[0 for j in range(n ** 2)] for i in range(n ** 2)]
        for i in range(len(data)):
            data2[i // n ** 2][i % n ** 2] = data[i]
        data = data2
        self.data = data
        for r in data:
            for c in r:
                print(c, end = ' ')
            print('')
        self.n = n
        self.has_changed = False
        self.rows = [None for i in range(n ** 2)]
        self.cols = [None for i in range(n ** 2)]
        self.boxes = [None for i in range(n ** 2)]
        # setting up row groups
        for r in range(n ** 2):
            self.rows[r] = Sudoku.Group('Row' + str(r), self)
            for c in range(n ** 2):
                cell = Sudoku.Cell(r, c, self)
                self.rows[r].add(cell)
                cell.add(self.rows[r])
        # setting up col groups
        for r in range(n ** 2):
            self.cols[r] = Sudoku.Group('Col' + str(r), self)
            for c in range(n ** 2):
                self.cols[r].add(self.get(c, r))
                self.get(c, r).add(self.cols[r])
        # setting up box groups
        r = 0
        for i in range(0, n ** 2, n):
            for j in range(0, n ** 2, n):
                self.boxes[r] = Sudoku.Group('Box' + str(r), self)
                for y in range(n):
                    for x in range(n):
                        self.boxes[r].add(self.get(i + y, j + x))
                        self.get(i+ y, j + x).add(self.boxes[r])
                r += 1
        # setting up possibles
        for r in range(n ** 2):
            for c in range(n ** 2):
                if data[r][c] != 0:
                    self.get(r, c).remove_all_but(data[r][c])
        # solving
        self.solve()

    def input_solution(self, data):
        for r in range(self.n ** 2):
            for c in range(self.n ** 2):
                if data[r][c] == 0:
                    continue
                self.get(r, c).remove_all_but(data[r][c])

    def convert_data(data):
        data2 = []
        for c in data:
            if c in '0123456789':
                data2.append(int(c))
            elif c == '?':
                data2.append(0)
        print(len(data2))
        return data2

    def get(self, r, c):
        return self.rows[r].get(c)

    def __str__(self):
        s = ''
        for r in range(self.n ** 2):
            if r != 0 and r % self.n == 0:
                for c in range(self.n ** 2):
                    if c != 0 and c % self.n == 0:
                        s += '+'
                    s += '-'
                s += '\n'
            for c in range(self.n ** 2):
                if c != 0 and c % self.n == 0:
                    s += '|'
                s += str(self.get(r, c))
            s += '\n'
        return s

    def is_solved(self):
        for r in self.rows:
            for c in r:
                if not c.is_solved():
                    return False
        return True

    def is_correct(self):
        for cga in (self.rows, self.cols, self.boxes):
            for g in cga:
                for c1 in g:
                    for c2 in g:
                        if True in [c1 is c2,
                                    not c1.is_solved(),
                                    not c2.is_solved()]:
                            continue
                        if c1.get(0) == c2.get(0):
                            return False
        return True

    def cheat(self, sleep_time = 0.25, possibles = False):
        grid = {'y0':244, 'x0':1907, 'y1':510, 'x1':2170}
        buttons = {'y0':563, 'x0':1890, 'y1':563, 'x1':2181}
        grid['dy'] = (grid['y1'] - grid['y0']) // 8
        grid['dx'] = (grid['x1'] - grid['x0']) // 8
        buttons['dy'] = (buttons['y1'] - buttons['y0']) // 8
        buttons['dx'] = (buttons['x1'] - buttons['x0']) // 8
        if possibles:
            setCursor(1925, 602)
        else:
            setCursor(1894, 602)
        mouseEvent('LEFT CLICK')
        for i in range(self.n ** 2):
            setCursor(buttons['x0'] + i * buttons['dx'],
                      buttons['y0'] + i * buttons['dy'])
            mouseEvent('LEFT CLICK')
            sleep(sleep_time)
            for r in range(self.n ** 2):
                for c in range(self.n ** 2):
                    cell = self.get(r, c)
                    if possibles and True in (
                            cell.is_solved(),
                            self.data[r][c] != 0,
                            not i + 1 in cell.possibles):
                        continue
                    elif not possibles and True in (
                            not cell.is_solved(),
                            not cell.get(0) == i + 1,
                            self.data[r][c] != 0):
                        continue
                    setCursor(grid['x0'] + c * grid['dx'],
                              grid['y0'] + r * grid['dy'])
                    mouseEvent('LEFT CLICK')
                    sleep(sleep_time)

    def cheat_possibles(self, sleep_time = 0.1):
        grid = {'y0':244, 'x0':1907, 'y1':510, 'x1':2178}
        buttons = {'y0':563, 'x0':1890, 'y1':563, 'x1':2190}
        grid['dy'] = (grid['y1'] - grid['y0']) // 8
        grid['dx'] = (grid['x1'] - grid['x0']) // 8
        buttons['dy'] = (buttons['y1'] - buttons['y0']) // 8
        buttons['dx'] = (buttons['x1'] - buttons['x0']) // 8
        for i in range(self.n ** 2):
            setCursor(buttons['x0'] + i * buttons['dx'],
                      buttons['y0'] + i * buttons['dy'])
            mouseEvent('LEFT CLICK')
            sleep(sleep_time)
            for r in range(self.n ** 2):
                for c in range(self.n ** 2):
                    cell = self.get(r, c)
                    if True in (cell.is_solved(),
                                self.data[r][c] != 0,
                                not i + 1 in cell.possibles):
                        continue
                    setCursor(grid['x0'] + c * grid['dx'],
                              grid['y0'] + r * grid['dy'])
                    mouseEvent('LEFT CLICK')
                    sleep(sleep_time)

    def solve(self):
        # TODO
        n = self.n
        while(self.has_changed and not self.is_solved()):
            self.has_changed = False
            print(self)
            # hidden singles
            for g in self.groups():
                for i in range(1, n ** 2 + 1):
                    if g.has_solved(i):
                        continue
                    count = 0
                    x = None
                    for c in g:
                        if c.has_possible(i):
                            x = c
                            count += 1
                    if count == 1:
                        x.remove_all_but(i)
            # naked/hidden n-pairs
            for g in self.groups():
                for r in range(2, n ** 2 + 1):
                    perms = g.choose(r)
                    for p in perms:
                        s = set()
                        for cell in p:
                            for i in cell.possibles:
                                s.add(i)
                        if len(s) == r:
                            for cell in g:
                                if not cell in p:
                                    cell.remove_all(*s)
            # intersection removal
            for ga in self.groups():
                for gb in self.groups():
                    intersection = ga.intersection(gb)
                    if len(intersection) != n:
                        continue
                    for i in range(1, n ** 2 + 1):
                        t = 0
                        ta = 0
                        tb = 0
                        for j in intersection:
                            if j.has_possible(i):
                                t += 1
                        for j in ga:
                            if j.has_possible(i):
                                ta += 1
                        for j in gb:
                            if j.has_possible(i):
                                tb += 1
                        if (ta == t) == (tb == t):
                            continue
                        if ta == t:
                            for c in gb:
                                if not c in intersection:
                                    c.remove_all(i)
                        # tb will come in opposite iteration
                        
            
        if not self.has_changed:
            print('Unable to complete the Sudoku.')
        if not self.is_correct():
            print('Sudoku is not correct.')
        print(self)

    def groups(self):
        return self.rows + self.cols + self.boxes

    class Cell:

        def __init__(self, r, c, outer):
            self.outer = outer
            self.r = r
            self.c = c
            self.possibles = [i + 1 for i in range(self.outer.n ** 2)]
            self.groups = []

        def add(self, g):
            self.groups.append(g)

        def get(self, index):
            return self.possibles[index]

        def is_solved(self):
            return len(self.possibles) == 1

        def __str__(self):
            if not self.is_solved():
                return "?"
            return str(self.get(0))

        def has_possible(self, i):
            return i in self.possibles

        def remove_possible(self, i):
            if self.is_solved():
                return False
            b = True
            try:
                self.possibles.remove(i)
                #print('removing', i)
            except ValueError:
                b = False
            if self.is_solved():
                print('(%d,%d)=%d' % (self.r, self.c, self.get(0)))
                for g in self.groups:
                    g.solved[self.get(0) - 1] = True
                    for c in g:
                        c.remove_possible(self.get(0))
            self.outer.has_changed = b or self.outer.has_changed
            return b

        def remove_all(self, *args):
            for i in args:
                self.remove_possible(i)
        
        def remove_all_but(self, x):
            #print('removing all but', x)
            if type(x) is int:
                x = [x]
            for i in x:
                for j in range(self.outer.n ** 2):
                    if i != j + 1:
                        self.remove_possible(j + 1)
            
    class Group(list):

        def __init__(self, name, outer):
            self.outer = outer
            self.name = name
            self.solved = [False for i in range(self.outer.n ** 2)]

        def add(self, c):
            self.append(c)
            if c.is_solved():
                self.solved[c.get(0)] = True

        def has_solved(self, i):
            return self.solved[i - 1]

        def __str__(self):
            s = self.name + ":"
            for c in self:
                s += '(%d,%d)' % (c.r, c.c)
            return s

        def get(self, index):
            return self[index]

        def choose(self, r):
            perms = []
            for i in itertools.combinations(self, r):
                if not any(j.is_solved() for j in i):
                    perms.append(i)
            return perms

        def intersection(self, other):
            intersect = []
            for i in self:
                if i in other:
                    intersect.append(i)
            return intersect

x = Sudoku(Sudoku.convert_data(data), 3)
input('Enter to exit...')
