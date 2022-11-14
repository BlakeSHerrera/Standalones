#knight's tour.py

'''
For any m by n board with m <= n,
a closed knight's tour is always possible unless
1. m and n are both odd
2. m = 1, 2, or 4
or
3. m = 3 and n = 4, 6, or 8
'''

from PIL import Image, ImageDraw
import os
import colorsys

KNIGHT_MOVES = [(2, 1), (2, -1), (1, 2), (1, -2),
                (-1, 2), (-1, -2), (-2, 1), (-2, -1)]

class Board:

    def __init__(self, rows, cols):
        self.dimensions = (rows, cols)
        self.num_squares = rows * cols
        self.board = [[Square(r, c) for c in range(cols)] for r in range(rows)]
        for r in self.board:
            for s in r:
                for ri, ci in KNIGHT_MOVES:
                    if self.in_bounds(s.r + ri, s.c + ci):
                        s.neighbors.append(self[s.r + ri][s.c + ci])

    def in_bounds(self, r, c):
        return r >= 0 and c >= 0 and r < len(self.board) and c < len(self.board[r])

    def __getitem__(self, i):
        return self.board[i]

    def __len__(self):
        return len(self.board)

class Square:

    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.neighbors = []
        self.visited = False

    def get_open_neighbors(self):
        for i in self.neighbors:
            if not i.visited:
                yield i

    def sort_neighbors(self):
        self.neighbors = sorted(self.neighbors,
                                key = Square.num_open_neighbors,
                                reverse = True)

    def num_open_neighbors(self):
        n = 0
        for i in self.neighbors:
            if not i.visited:
                n += 1
        return n

    def __str__(self):
        return '(%d, %d)%s' % (self.r, self.c,
                               'X' if self.visited else 'O')

    def __repr__(self):
        return 'Square' + str(self)

def warnsdorff_heuristic(board, r, c):
    global backtrack
    path = []

    stack = [board[r][c]]
    while(len(stack) > 0):
        s = stack.pop()
        if s == 'POP':
            path.pop().visited = False
            backtrack += 1
            #print(s)
            continue
        if s.visited:
            continue
        #print(s)
        s.visited = True
        path.append(s)
        if len(path) >= board.num_squares:
            #path.append(path[0])
            return path
        stack.append('POP')
        s.sort_neighbors()
        for n in s.neighbors:
            stack.append(n)
    print('No solutions found.')
    return False

def warnsdorff_180(board, r, c, file):
    global backtrack
    path_1 = []
    path_2 = []
    file.write('%d %d\n' % (len(board), len(board[0])))
    solutions = 0

    stack_1 = [board[r][c]]
    r, c = rotate_180(len(board), r, c)
    stack_2 = [board[r][c]]
    while(len(stack_1) > 0):
        s_1 = stack_1.pop()
        s_2 = stack_2.pop()
        if s_1 == 'POP':
            #assert s_2 == 'POP'
            path_1.pop().visited = False
            path_2.pop().visited = False
            backtrack += 1
            continue
        if s_1.visited:
            #assert s_2.visited
            continue
        s_1.visited = True
        s_2.visited = True
        path_1.append(s_1)
        path_2.append(s_2)
        if len(path_1) + len(path_2) >= board.num_squares:
            if is_knight_move(path_1[-1].c,
                              path_1[-1].r,
                              path_2[0].c,
                              path_2[0].r):
                #assert is_knight_move(path_2[-1], path_1[0])
                p = path_1 + path_2 + [path_1[0]]
                return p
                solutions += 1
                #print(solutions, 'solutions,', backtracks, 'backtracks.', end = '\r')
                for i in p:
                    file.write('%d %d ' % (i.r, i.c))
                file.write('\n')
        stack_1.append('POP')
        stack_2.append('POP')
        #s_1.sort_neighbors()
        for n in s_1.neighbors:
            stack_1.append(n)
            r, c = rotate_180(len(board), n.r, n.c)
            stack_2.append(board[r][c])
    print(solutions, 'solutions.')
    return False
    
def rotate_90(l, r, c):
    return (c, l - r - 1)

def rotate_180(l, r, c):
    return (l - r - 1, l - c - 1)

def is_knight_move(xi, yi, xf, yf):
    return all((abs(xi - xf) + abs(yi - yf) == 3,
                xi != xf,
                yi != yf))

def is_closed(path):
    return is_knight_move(path[0].c, path[0].r, path[-1].c, path[-1].r)

def plot(r, c, path):
    cell_size = 20
    padding = 1

    mode = 'RGB'
    bg_color = (255, 255, 255)
    im_width = cell_size * c + padding * 2
    im_height = cell_size * r + padding * 2
    im = Image.new(mode, (im_width, im_height), bg_color)
    draw = ImageDraw.Draw(im, mode)

    grid_color = (0, 0, 0)
    grid_thickness = 1
    for i in range(r + 1):
        draw.line((padding,
                   padding + i * cell_size,
                   padding + c * cell_size,
                   padding + i * cell_size),
                  grid_color,
                  grid_thickness)
    for i in range(c + 1):
        draw.line((padding + i * cell_size,
                   padding,
                   padding + i * cell_size,
                   padding + r * cell_size),
                  grid_color,
                  grid_thickness)
    
    line_thickness = 3
    for i in range(1, len(path)):
        line_color = hsv2rgb((i - 1) / len(path))
        yi = path[i - 1].r * cell_size + padding + cell_size / 2
        xi = path[i - 1].c * cell_size + padding + cell_size / 2
        yf = path[i].r * cell_size + padding + cell_size / 2
        xf = path[i].c * cell_size + padding + cell_size / 2
        draw.line((xi, yi, xf, yf),
                  line_color, line_thickness)
    
    url = 'temp.png'
    im.save(url)
    #os.system('powershell -c ' + url)

def hsv2rgb(h, s = 1, v = 1):
    return tuple(int(round(i * 255)) for i in colorsys.hsv_to_rgb(h, s, v))

rows = 8
cols = 8

board = Board(rows, cols)
backtrack = 0
file = open('8x8 180 symmetry.txt', 'w+')
try:
    path = warnsdorff_180(board, rows // 2, cols // 2, file)
    if path is False:
        print('No tours.')
    else:
        plot(rows, cols, path)
    print(backtrack)
except KeyboardInterrupt as ki:
    print(ki)
finally:
    file.close()


