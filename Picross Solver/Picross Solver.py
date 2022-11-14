#Picross Solver
from time import time
start = time()

def solve(v_data, h_data):
    global pcount
    
    def is_solved():
        for c in v_data + h_data:
            if c != []:
                 return False
        return True;

    def mark_off_solved():
        for r in range(v):
            if len(v_data[r]) == 0:
                continue
            for c in range(h):
                if data[r][c] == 0:
                    break
            else:
                v_data[r] = []
        for c in range(h):
            if len(h_data[c]) == 0:
                continue
            for r in range(v):
                if data[r][c] == 0:
                    break
            else:
                h_data[c] = []

    def get_perms(row, row_data):
        if len(row_data) == 1 and row_data[0] == 0:
            return [[2] * len(row)]
        #wiggle room
        wr = len(row) - sum(row_data) - len(row_data) + 1
        xdata = [0] * len(row_data)
        perms = [xdata.copy()]
        xpos = 0
        while xpos < len(xdata):
            if xdata[xpos] >= wr:
                xdata[xpos] = 0
                xpos += 1
            else:
                xdata[xpos] += 1
                xpos = 0
                if sum(xdata) <= wr:
                    perms.append(xdata.copy())
        permutations = []
        for p in perms:
            xdata = []
            tdata = [0] * len(row)
            for c in range(len(p)):
                xdata.append(p[c])
                xdata.append(row_data[c])
            s = ''
            b = False
            for c in xdata:
                s += ('1' * c if b else '2' * (c + 1))
                b = not b
            s += '2' * (len(row) - len(s) + 1)
            s = list(s[1:])
            for c in range(len(s)):
                s[c] = int(s[c])
                if row[c] == 1 and s[c] == 2:
                    break
                if row[c] == 2 and s[c] == 1:
                    break
            else:
                permutations.append(s)
        return permutations

    def reduce_to_forced(perms):
        xdata = perms[0]
        for x in range(len(xdata)):
            for p in perms:
                if p[x] != xdata[x]:
                    xdata[x] = 0
                    break
        return xdata
    
    v = len(v_data)
    h = len(h_data)
    data = [[0 for c in range(h)] for c in range(v)]
    n = 0
    while not is_solved():
        print('Pass:', n)
        print('Time:', time() - start)
        n += 1
        print_data(data)
        changed = False
        for r in range(v):
            #print('r =', r)
            if len(v_data[r]) == 0:
                continue
            permutations = get_perms(data[r], v_data[r])
            forced = reduce_to_forced(permutations)
            tchange = False
            for c in range(h):
                if forced[c] == 1 or forced[c] == 2:
                    if data[r][c] != forced[c] and data[r][c] != 0:
                        print('error')
                    if data[r][c] == 0:
                        changed = True
                        tchange = True
                    data[r][c] = forced[c]
            if tchange:
                print_data(data)
                print('.')
        for c in range(h):
            #print('c =', c)
            if len(h_data[c]) == 0:
                continue
            xdata = []
            for r in range(v):
                xdata.append(data[r][c])
            permutations = get_perms(xdata, h_data[c])
            forced = reduce_to_forced(permutations)
            tchange = False
            for r in range(v):
                if forced[r] == 1 or forced[r] == 2:
                    if data[r][c] != forced[r] and data[r][c] != 0:
                        print('error')
                    if data[r][c] == 0:
                        changed = True
                        tchange = True
                    data[r][c] = forced[r]
            if tchange:
                print_data(data)
                print('.')
        print('')
        if not changed:
            print('Stuck')
            break
        mark_off_solved()
    print('Pass:', n)
    print('Time:', time() - start)
    print_data(data)

def print_data(data, b = True):
    for r in data:
        s = ''
        for c in r:
            if b:
                s += '?' if c == 0 else '█' if c == 1 else ' '
            else:
                s += '?' if c == 0 else 'O' if c == 1 else '-'
        print(s)

#takes too long to solve
solve([[3],
       [8],
       [1, 4, 2],
       [6, 4],
       [2, 4, 1, 1],
       
       [1, 5, 1],
       [7, 3],
       [12],
       [2, 10],
       [1, 3, 7],

       [2, 1, 2, 2],
       [1, 2, 2, 2],
       [1, 1, 1],
       [3, 2],
       [2, 2]],
      


      [[1],
       [1, 3],
       [1, 2, 2],
       [5, 1],
       [2, 2, 2, 3],
       
       [4, 5, 2],
       [10],
       [8],
       [8, 1],
       [7, 2],

       [6, 1],
       [2, 3, 3],
       [2, 5, 1],
       [2, 6, 2],
       [4, 2, 3]])

input('Enter to exit...')
