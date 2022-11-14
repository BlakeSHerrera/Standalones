from PIL import Image, ImageGrab
import tkinter
import random
import mouse

print('be sure to play on 1st screen')

class RGB:

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return '%d %d %d' % (self.r, self.g, self.b)

    def copy(self):
        return RGB(self.r, self.g, self.b)

    def to_hex(self):

        def h(c):
            s = hex(c)[2:]
            return '0' * (2 - len(s)) + s

        return h(self.r) + h(self.g) + h(self.b)

    def half(self):
        return RGB(self.r // 2, self.g // 2, self.b // 2)

    def is_dark(self):
        return self.r < 100 and self.g < 100 and self.b < 100
    
    def __eq__(self, other):
        t = type(other)
        if t is tuple:
            return (self.r, self.g, self.b) == other
        elif t is RGB:
            return self.r == other.r and self.g == other.g and self.b == other.b
        else:
            raise ValueError("Can't RGB == " + str(r))

    def r2(self, p):
        return (self.r - p[0]) ** 2 + (self.g - p[1]) ** 2 + (self.b - p[2]) ** 2

NULL = RGB(0, 0, 0)
WHITE = RGB(247, 246, 246)
BLACK = RGB(24, 24, 24)
RED = RGB(246, 55, 65)
YELLOW = RGB(246, 246, 4)
PURPLE = RGB(206, 111, 166)
BLUE = RGB(127, 198, 246)
GREEN = RGB(148, 236, 0)
ORANGE = RGB(246, 166, 0)
PINK = RGB(246, 198, 230)
COLORS = {
    'w' : WHITE,
    'r' : RED,
    'y' : YELLOW,
    'l' : PURPLE,
    'b' : BLUE,
    'g' : GREEN,
    'o' : ORANGE,
    'p' : PINK}
HALF_COLORS = {
    'W' : WHITE.half(),
    'R' : RED.half(),
    'Y' : YELLOW.half(),
    'L' : PURPLE.half(),
    'B' : BLUE.half(),
    'G' : GREEN.half(),
    'O' : ORANGE.half(),
    'P' : PINK.half()}

UL = (509, 239)
BR = (837, 574)
DIFF = (BR[0] - UL[0], BR[1] - UL[1])
DXDY = (DIFF[0] // 8, DIFF[1] // 8)

root = tkinter.Tk()
canvas = tkinter.Canvas(
    root,
    width = 400,
    height = 400,
    bg = '#' + NULL.to_hex())
canvas.pack()
BS = 50

def drawblocks(canvas):
    try:
        data = get_data()
        for r in range(len(data)):
            data[r] = list(data[r])
        for r in range(len(data)):
            for c in range(len(data[r])):
                try:
                    b = in_a_row(data, r, c)
                    color = COLORS[data[r][c]]
                except KeyError:
                    color = RGB(128, 128, 128)
                except IndexError:
                    color = RGB(128, 128, 128)
                canvas.create_rectangle(
                    (c * BS,
                     r * BS,
                     (c + 1) * BS,
                     (r + 1) * BS),
                    fill = '#' + color.to_hex())
                if b:
                    canvas.create_rectangle(
                        (c * BS + 10,
                         r * BS + 10,
                         (c + 1) * BS - 10,
                         (r + 1) * BS - 10),
                        fill = '#000000')
    finally:
        root.after(1000, drawblocks, canvas)

def in_a_row(data, r, c):

    def ib(x):
        return 0 <= x < 8

    debug = False

    if debug:
        print(r, c, data[r][c])

    for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        #3rd space, same dir
        if ib(r + 3 * dr) and ib(c + 3 * dc):
            if debug:
                print('one', 3 * dr, 3 * dc, end = ' ')
                print(data[r + 3 * dr][c + 3 * dc])
            if data[r][c] == data[r + 3 * dr][c + 3 * dc]:
                #2nd space, same dir
                if debug:
                    print('two', 2 * dr, 2 * dc, end = ' ')
                    print(data[r + 2 * dr][c + 2 * dc])
                if data[r][c] == data[r + 2 * dr][c + 2 * dc]:
                    return True
        #1 space over
        if ib(r + dr) and ib(c + dc):
            #orthogonal dir 1
            if ib(r + dr + dc) and ib(c + dc + dr):
                if debug:
                    print('three', dr + dc, dc + dr, end = ' ')
                    print(data[r + dr + dc][c + dc + dr])
                if data[r][c] == data[r + dr + dc][c + dc + dr]:
                    #3 in a row
                    if ib(r + dr + 2 * dc) and ib(c + dc + 2 * dr):
                        if debug:
                            print('four', dr + 2 * dc, dc + 2 * dr, end = ' ')
                            print(data[r + dr + 2 * dc][c + dc + 2 * dr])
                        if data[r][c] == data[r + dr + 2 * dc][c + dc + 2 * dr]:
                            return True
                    #opposite side
                    if ib(r + dr - dc) and ib(c + dc - dr):
                        if debug:
                            print('five', dr - dc, dc - dr, end = ' ')
                            print(data[r + dr - dc][c + dc - dr])
                        if data[r][c] == data[r + dr - dc][c + dc - dr]:
                            return True
            #orthogonal dir 2
            if ib(r + dr - 2 * dc) and ib(c + dc - 2 * dr):
                if debug:
                    print('six', dr - 2 * dc, dc - 2 * dr, end = ' ')
                    print(data[r + dr - 2 * dc][c + dc - 2 * dr])
                if data[r][c] == data[r + dr - 2 * dc][c + dc - 2 * dr]:
                    #3 in a row
                    if debug:
                        print('seven', -dc, -dr, end = ' ')
                        print(data[r + dr - dc][c + dc - dr])
                    if data[r][c] == data[r + dr - dc][c + dc - dr]:
                        return True
                    #no need to check opposite side again
    if debug:
        print('-----------------------------')
    return False
                
def get_data():
    im = ImageGrab.grab()
    data = []
    for r in range(8):
        data.append('')
        for c in range(8):
            l = 'x'
            for y in range(UL[1] + r * DXDY[1], UL[1] + (r + 1) * DXDY[1], 1):
                for x in range(UL[0] + c * DXDY[0], UL[0] + (c + 1) * DXDY[1], 1):
                    b = False
                    p = im.getpixel((x, y))
                    for i in COLORS.keys():
                        j = COLORS[i]
                        if j == p:
                            data[-1] += i
                            b = True
                            break
                    if b:
                        break
                else:
                    continue
                break
    return data
                        

root.after(1000, drawblocks, canvas)
root.mainloop()
