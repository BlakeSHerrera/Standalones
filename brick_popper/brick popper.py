#brick popper.py

from winsound import Beep
from time import time, sleep
from PIL import Image
import ctypes

start = time()

class Game:

    def __init__(
            self,
            blocks,
            score = 0,
            groups = None,
            colors = None):
        self.blocks = blocks
        self.groups = []
        self.score = score
        if groups is None:
            self.groupify()
        else:
            self.groups = groups
        if colors is None:
            self.colors = {}
            for r in self.blocks:
                for b in r:
                    if b is not None:
                        try:
                            self.colors[b.color] += 1
                        except KeyError:
                            self.colors[b.color] = 1
        else:
            self.colors = colors

    def __repr__(
            self):
        s = ''
        for r in self.blocks[::-1]:
            for c in r:
                if c is not None:
                    s += c.color
                else:
                    s += '-'
            s += '\n'
        return s

    def print_parts(
            self):
        for c in self.colors.keys():
            for r in self.blocks[::-1]:
                for b in r:
                    if b is not None and b.color == c:
                        print(c, end = '')
                    else:
                        print(' ', end = '')
                print('')
            print('')

    def print_groups(
            self):
        for i in self.groups:
            print(i)

    def is_solved(
            self):
        if len(self.groups) == 0:
            for r in self.blocks:
                for b in r:
                    if b is not None:
                        return 'go'
            return 'yes'
        return 'no'

    def copy(
            self):
        blocks = []
        for r in self.blocks:
            blocks.append([])
            for c in r:
                if c is not None:
                    blocks[-1].append(c.copy())
                else:
                    blocks[-1].append(None)
        return Game(
            blocks,
            score = self.score,
            groups = [i.copy() for i in self.groups],
            colors = self.colors.copy())

    def t_max_score(
            self):
        s = self.score
        for i in self.colors.keys():
            if self.colors[i] == 1:
                return -1
            s += self.colors[i] * (self.colors[i] - 1)
        return s
    
    def delete(
            self,
            group):
        bs = group.blocks
        self.colors[bs[0].color] -= len(bs)
        self.score += len(bs) * (len(bs) - 1)
        for b in bs:
            self.blocks[b.r][b.c] = None
        self.groups.remove(group)
        self.shift_blocks()

    def shift_blocks(
            self):
        def shift_left(
                r,
                c):
            if self.oob(r, c) or self.oob(r, c - 1):
                return False
            if self.blocks[r][c] is None:
                return False
            if self.blocks[r][c - 1] is None:
                self.move(r, c, r, c - 1)
                shift_left(r + 1, c)
                return True
            return False
        def shift_down(
                r,
                c):
            if self.oob(r, c) or self.oob(r - 1, c):
                return False
            if self.blocks[r][c] is None:
                return False
            if self.blocks[r - 1][c] is None:
                self.move(r, c, r - 1, c)
                shift_down(r - 1, c)
                return True
            return False
        for r in range(len(self.blocks)):
            for c in range(len(self.blocks[r])):
                b = self.blocks[r][c]
                if b is not None:
                    shift_down(r, c)
        for c in range(len(self.blocks[0])):
            b = self.blocks[0][c]
            if b is not None:
                while shift_left(0, b.c):
                    pass
        
        self.clean_up()
        self.groupify()

    def clean_up(
            self):
        to_remove = []
        for r in self.blocks[::-1]:
            for c in r:
                if c is not None:
                    break
            else:
                to_remove.append(r)
                continue
            break
        for r in to_remove:
            self.blocks.remove(r)
        if len(self.blocks) == 0:
            return
        for c in range(len(self.blocks[0]))[::-1]:
            if c is not None:
                for r in range(len(self.blocks)):
                    self.blocks[r] = self.blocks[r][0:c + 1]
                break

    def groupify(
            self):
        def helper(
                b,
                r,
                c,
                g):
            if self.oob(r, c) or self.blocks[r][c] is None:
                return
            if b.color != self.blocks[r][c].color:
                return
            if self.blocks[r][c].group is not None:
                return
            g.add(self.blocks[r][c])
            helper(b, r - 1, c, g)
            helper(b, r, c - 1, g)
            helper(b, r + 1, c, g)
            helper(b, r, c + 1, g)
        for row in self.blocks:
            for b in row:
                if b is not None:
                    b.group = None
        self.groups = []
        for row in self.blocks:
            for b in row:
                if b is not None:
                    g = Group([])
                    helper(b, b.r, b.c, g)
                    if len(g.blocks) >= 2:
                        self.groups.append(g)

    def oob(
            self,
            r,
            c):
        return r < 0 or c < 0 or r >= len(self.blocks) or c >= len(self.blocks[r])

    def ib(
            self,
            r,
            c):
        return not self.oob(r, c)

    def move(
            self,
            from_r,
            from_c,
            to_r,
            to_c):
        self.blocks[to_r][to_c] = self.blocks[from_r][from_c]
        self.blocks[from_r][from_c] = None
        self.blocks[to_r][to_c].r = to_r
        self.blocks[to_r][to_c].c = to_c

class Group:

    def __init__(
            self,
            blocks):
        self.blocks = blocks
        for i in blocks:
            i.group = self

    def __repr__(
            self):
        if len(self.blocks) == 0:
            return 'Empty Group'
        return 'Group with %s' % self.blocks[0]

    def print_all(
            self):
        for c in self.blocks:
            print(c)

    def add(
            self,
            block):
        self.blocks.append(block)
        block.group = self

    def copy(
            self):
        return Group([i.copy() for i in self.blocks])

class Block:

    def __init__(
            self,
            r,
            c,
            color,
            group = None):
        self.r = r
        self.c = c
        self.color = color
        self.group = group
    
    def __repr__(
            self):
        return 'r=%d c=%d color=%s' % (self.r, self.c, self.color)
    def copy(
            self):
        return Block(
            self.r,
            self.c,
            self.color,
            self.group)

def parse_data(s):
    data = s.split('\n')
    blocks = []
    for r in range(len(data))[::-1]:
        blocks.append([])
        for c in range(len(data[r])):
            if data[r][c] == '-':
                blocks[-1].append(None)
            else:
                blocks[-1].append(Block(
                    len(data) - r - 1, c, data[r][c]))
    return Game(blocks)

def main(
        data):
    global maxx, best_chain, max_score
    start_left = 1889
    start_up = 251
    end_right = 2184
    end_down = 547
    inc_ud = (end_down - start_up) / 9
    inc_lr = (end_right - start_left) / 9
    
    arr = data.split('\n\n')
    for i in arr:
        game = parse_data(i)
        print(game)
        game.print_parts()
        print(len(game.groups))
        start = time()
        maxx = 0
        for i in game.colors.keys():
            if game.colors[i] > maxx:
                maxx = game.colors[i]
                key = i
        maxx = 0
        for i in game.colors.keys():
            if i == key:
                maxx += game.colors[i] * (game.colors[i] - 1)
            else:
                maxx += game.colors[i] * 2
        print(maxx)
        print(game.t_max_score())
        max_score = 0
        best_chain = []
        input(':')
        try:
            x = solve(game)
            print(x[0])
        except KeyboardInterrupt:
            print('')
        input(time() - start)
        autosolve = ''
        for j in range(len(best_chain)):
            if not autosolve:
                autosolve = input('%d %s' % (j, best_chain[j]))
            else:
                print(j, best_chain[j])
                sleep(3)
            b = best_chain[j].blocks[0]
            r = end_down - b.r * inc_ud
            c = start_left + b.c * inc_lr
            click(int(c), int(r))
    input(':')

def solve(
        game,
        g_chain = [],
        depths = []):
    global max_score, best_chain
    s = game.is_solved()
    if s == 'yes':
        return (game.score, g_chain)
    if s == 'go':
        return (-game.score, g_chain)
    if game.t_max_score() <= max_score:
        return (0, g_chain)
    if len(depths) < 21:
        s = str(int(time() - start))
        s += ' ' + str(max_score)
        s += ' ' + str(game.score) + '\t'
        for i in range(0, len(depths), 2):
            s += ' %d/%d'
        print(s % tuple(depths))
    best_g_chain = g_chain
    best_s = -game.score
    for i in range(len(game.groups)):
        ng = game.copy()
        grp = ng.groups[i]
        ng.delete(ng.groups[i])
        score, chain = solve(
            ng,
            g_chain = g_chain + [grp],
            depths = depths + [i, len(game.groups)])
        if score > max_score:
            print(score, max_score)
            max_score = score
            best_g_chain = chain
            best_chain = chain
            Beep(440, 100)
        if best_s < score:
            best_s = score
    return (best_s, best_g_chain)

def closest_color(c):
    white = (255, 255, 255, '-')
    red = (255, 109, 114, 'r')
    green = (14, 177, 156, 'g')
    yellow = (253, 178, 54, 'y')
    blue = (79, 150, 242, 'b')
    purple = (179, 111, 238, 'p')
    black = (151, 136, 116, 'k')
    curr = ('r', 255 ** 2 * 3)
    for i in (white, red, green, yellow, blue, purple, black):
        r2 = 0
        for j in range(3):
            r2 += (c[j] - i[j]) ** 2
        if r2 < curr[1]:
            curr = (i[3], r2)
    return curr[0]

def click(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(0x0002)
    ctypes.windll.user32.mouse_event(0x0004)

start_left = 1889
start_up = 251
end_right = 2184
end_down = 547
inc_ud = (end_down - start_up) / 9
inc_lr = (end_right - start_left) / 9
im = Image.open(r'C:\Users\Blake\Downloads\Untitled.png')
rgb_im = im.convert('RGB')
data = ''
r = start_up
while r < end_down + 1:
    c = start_left
    while c < end_right + 1:
        x = int(c)
        y = int(r)
        data += closest_color(rgb_im.getpixel((x, y)))
        c += inc_lr
    data += '\n'
    r += inc_ud
data = data.strip()
maxx = 0
max_score = 0
best_chain = []
main(data)
