#hanoi.py
#Python 3.4.4

from tkinter import *
from time import sleep, time
from functools import partial
from threading import Thread

#implemented as a stack
class Peg:

    #superclass for the other defined exceptions
    class PegException(Exception):
        pass

    #raised when user tries to move a disk
    #from an empty peg. Note it is not handled
    #in push or pop methods
    class EmptyPegMoveException(PegException):

        def __init__(
                self,
                arg):   #the empty peg
            msg = 'Cannot move from %s' % (arg)
            super().__init__(msg)

    #raised when user tries to move a larger disk
    #onto a smaller disk
    class BackwardsDiskException(PegException):

        def __init__(
                self,
                arg1,   #the larger disk
                arg2):  #the smaller disk
            msg = 'Cannot push %s onto %s' % (arg1, arg2)
            super().__init__(msg)

    #constants for graphics usage
    SEPARATION = 100
    BOTTOM = 50
        
    def __init__(
            self,
            id_num):    #the number of the peg, for graphics
        self.id_num = id_num
        self.disks = []

    def __repr__(self):
        return 'Peg %d: %s' % (self.id_num,
                               str([i.size for i in self.disks]))

    def pop(
            self):
        if self.is_empty():
            raise Peg.EmptyPegMoveException(self)
        return self.disks.pop()

    def peek(
            self):
        if self.is_empty():
            raise Peg.EmptyPegMoveException(self)
        return self.disks[-1]

    #Push the disk onto the stack and redraw it
    def push(
            self,
            disk):
        if not len(self.disks) < 1 and self.disks[-1].size < disk.size:
            raise Peg.BackwardsDiskException(disk.size, self)
        disk.height = len(self.disks)
        disk.peg_num = self.id_num
        self.disks.append(disk)
        disk.redraw()

    def size(
            self):
        return len(self.disks)

    def is_empty(
            self):
        return self.size() < 1

    #removes all disks from the peg and the canvas
    def destroy_disks(
            self):
        while not self.is_empty():
            self.pop().delete()

class Disk:

    #constants for graphics
    DWIDTH = 10
    DHEIGHT = 10
    COLORS = ['#FF0000',
              '#FFFF00',
              '#00FF00',
              '#00FFFF',
              '#0000FF',
              '#FF00FF']
    
    def __init__(
            self,
            size):
        self.size = size
        self.color = Disk.COLORS[size % len(Disk.COLORS)]
        self.height = -1    #must set these in order to
        self.peg_num = -1   #draw on canvas initially
        self.draw()

    def __repr__(
            self):
        return 'Disk %d' % (self.size)

    #Calculates bounding box for drawing
    def bbox(
            self):
        cx = (self.peg_num + 1) * Peg.SEPARATION
        by = Peg.BOTTOM + Disk.DHEIGHT * self.height
        return (cx - self.size * Disk.DWIDTH // 2,
                by + Disk.DHEIGHT,
                cx + self.size * Disk.DWIDTH // 2,
                by)

    def draw(
            self):
        self.id_num = canvas.create_rectangle(
            self.bbox(),
            fill = self.color,
            outline = '#000000')

    def redraw(
            self):
        canvas.coords(self.id_num,
                      self.bbox())

    #removes self from canvas
    def delete(
            self):
        canvas.delete(self.id_num)

#raised when there are < 3 pegs
class PegCountError(Exception):

    def __init__(
            self,
            arg):   #number of pegs
        msg = 'Not enough pegs: %d' % (arg)
        super().__init__(msg)

#raised when there are < 1 disks
class DiskCountError(Exception):

    def __init__(
            self,
            arg):   #number of disks
        msg = 'Not enough disks: %d' % (arg)
        super().__init__(msg)
    
def move_disk(
        from_peg,
        to_peg):
    disk = from_peg.pop()
    try:
        to_peg.push(disk)
    except Peg.BackwardsDiskException:
        from_peg.push(disk)
        raise
    disk.redraw()
    global num_moves
    num_moves += 1
    sleep(TIMER)

#Handles pressing numbered buttons
def button_press(
        peg_number):
    global is_solving, selected_peg
    if is_solving:
        print("Don't press this while solving")
    elif selected_peg is None:
        selected_peg = pegs[peg_number]
    else:
        try:
            move_disk(selected_peg, pegs[peg_number])
        except Peg.PegException as ex:
            print(ex)
        selected_peg = None

def print_pegs(
        ):
    global is_solving
    if is_solving:
        print('May have errors whilst solving')
    for p in pegs:
        print(p)
    print('')

#prints True if puzzle is solved else False
def check(
        ):
    global is_solving, start, num_moves
    t = time() - start
    if pegs[-1].size() == NUM_DISKS:
        n = NUM_DISKS
        p = NUM_PEGS
        print('Solved!')
        print('Expected number of moves: %f' % (
            (2 ** (n / (p - 2)) - 1) * (2 * p - 5)))
        is_solving = False
    else:
        print('Unsolved.')
        if is_solving:
            print('May be innacurate whilst solving')
    print('Time:  %dm %.2fs' % (t // 60, t % 60))
    print('Moves: %d' % (num_moves))
    print('')

#destroys the disks on all pegs and
#adds new disks onto the first peg
def reset(
        ):
    global is_solving, start, num_moves
    if is_solving:
        print("Don't reset whilst solving")
        return
    num_moves = 0
    for p in pegs:
        p.destroy_disks()
    for i in range(NUM_DISKS, 0, -1):
        pegs[0].push(Disk(i))
    start = time()

#recursive solution for 3 pegs
def recursive_solve_n3(
        ):

    #method which does the solving
    def helper(n, from_peg, aux_peg, to_peg):
        if n < 1:
            return
        if n == 1:
            move_peg(from_peg, to_peg)
            return
        #move (recursively) the top n-1 pegs to aux peg
        helper(n - 1, from_peg, to_peg, aux_peg)
        #move the only disk left to target peg
        move_peg(from_peg, to_peg)
        #move everything from aux peg to target peg
        helper(n - 1, aux_peg, from_peg, to_peg)

    if NUM_PEGS != 3:
        print('recursive_solve_n3 cannot solve with %d pegs' % NUM_PEGS)
    reset()
    global is_solving
    is_solving = True
    helper(num_disks, pegs[0], pegs[1], pegs[2])
    check()

''' recursive_solve()

    Given p number of pegs and n number of disks,
    this recursive algorithm works in blocks, which are
    composed of p - 2 disks.
    The top blocks are moved to any auxiliary peg recursively,
    Then remaining block is moved to the target peg.
    Finally, the other blocks are moved to the target peg
    recursively.

    In order to move a block, spread out the disks over
    all of the possible pegs. Reserve the target peg for
    the last block. Then, stack them back on the target
    peg, in the order opposite which you spread them out.

    Knowing that this just a more complex verion of the
    original tower of hanoi problem, I believe one could
    easily set up a loop to determine where the blocks
    should go, and then use an inner loop to move the
    block itself. This would be very much similar to what
    I have done for my while loop to solve the initial
    problem.

    The number of moves required to move a block of size
    a is 2 * a - 1. Remember, a = p - 2. Thus, this
    simplifies to 2 * p - 5 moves per block.
    
    The number of blocks that must be moved is similar
    to the initial tower of hanoi problem. For b blocks,
    the number of blocks that must be moved is 2 ^ b - 1.
    b = n / a = n = n / (p - 2)
    So, the number of blocks that must be moved is
    2 ^ (n / p - 2) - 1

    Given this information, the expected number of moves
    is approximately
      (2 ^ b - 1) * (2 * a - 1)
    = (2 ^ (n / (p - 2)) - 1) * (2 * p - 5)
    This formula is only 100% accurate if all blocks are
    full, meaning that n % a == 0

    This code has been optimized by making the the block
    with the fewest disks the one on top, as it ends up
    being moved 50% of the time. It may be just as easy
    to optimize this using a loop because you will be able
    to set the top block as being the smallest outside of
    the loop and move it every other move.
'''
#Recursively solves given any number of pegs
def recursive_solve(
        ):

    def helper(
            n,  #number of disks to move
            p): #list of pegs: p[0] is from, p[-1] is to
        if n < 1:
            return
        a = NUM_PEGS - 2
        #move top blocks to the second peg
        helper(n - a, p[:1] + p[2:] + p[1:2])
        #spread the last disks from p[0] across p[2:]
        b = min(n, a)
        for i in range(2, b + 2):
            move_disk(p[0], p[i + a - b])
        #go in reverse order, put disks on target peg p[-1]
        for i in range(2, b + 1)[::-1]:
            move_disk(p[i + a - b], p[-1])
        #move the blocks from second peg to the target peg
        helper(n - a, p[1:2] + p[:1] + p[2:])

    reset()
    global is_solving
    is_solving = True
    sleep(TIMER)
    helper(NUM_DISKS, pegs)
    check()

#solves for 3 pegs without recursion
def loop_solve_n3(
        ):
    if NUM_PEGS != 3:
        print('loop_solve_n3 cannot solve with %d pegs' % NUM_PEGS)
    reset()
    global is_solving
    is_solving = True
    start = time()
    ''' odd = 0 if the number of disks is even. Otherwise
        odd = 1. If odd, then the red peg should move to the
        left each time. Otherwise, the red peg should move
        to the right each time.

        n is a positive variable that keeps track of where the
        smallest peg is located. I use python negative list
        indexing to easily loop back around instead of using
        modulo. Effectively, n - 1 is the index of the peg left,
        and n - 2 is the index of the right peg. The index of
        the next peg can be expressed as n + odd - 2.

        Note that I could keep a reference to the smallest disk
        (let's call it d) and replace all n with d.peg_num
        However, that seems more difficult to read.
    '''
    odd = pegs[0].size() % 2
    n = 0
    #move smallest peg
    move_peg(pegs[0], pegs[n + odd - 2])
    n = (n + odd - 2) % 3
    #while the last peg does not have all the disks
    while pegs[2].size() != NUM_DISKS:
        ''' One of these is the only possible move that
            is not a wasted moving the smallest peg again.
            If one move raises a PegException, then it
            must be the other move.
        '''
        try:
            move_peg(pegs[n - 1], pegs[n - 2])
        except Peg.PegException:
            move_peg(pegs[n - 2], pegs[n - 1])
        ''' Once again, we have another forced move. Given
            that we cannot make our previous move in reverse,
            we are forced to move the smallest peg again.
            The direction that this peg is moved is always
            the same.
        '''
        move_peg(pegs[n], pegs[n + odd - 2])
        n = (n + odd - 2) % 3
    t = time() - start
    print('Solved in %dm %.2fs' % (t // 60, t % 60))
    is_solving = False

#button for solving calls this
def make_thread(
        ):
    global is_solving
    if not is_solving:
        options = [recursive_solve,
                   recursive_solve_n3,
                   loop_solve_n3]
        ''' User can edit the target, however,
            recursive_solve_n3 and loop_solve_n3
            should only be called if there are
            exactly 3 pegs
        '''
        t1 = Thread(target = options[0])
        t1.start()
    else:
        print('Already solving')

#constants for setting up the game
WIDTH = 800,
HEIGHT = 300
NUM_PEGS = int(input('Pegs: '))    #User can edit
NUM_DISKS = int(input('Disks: '))  #User can edit
TIMER = float(input('Timer: '))    #User can edit, delay after each move in seconds
Peg.SEPARATION = NUM_DISKS * Disk.DWIDTH

is_solving = False
num_moves = 0

if NUM_PEGS < 3:
    raise PegCountError(NUM_PEGS)
if NUM_DISKS < 1:
    raise DiskCountError(NUM_DISKS)
selected_peg = None

#GUI setup
root = Tk()
canvas = Canvas(root,
                width = WIDTH,
                height = HEIGHT,
                bg = 'white')
canvas.pack()
frame = Frame(root)
button = Button(frame, text = 'print', command = print_pegs)
button.pack(side = LEFT)
button = Button(frame, text = 'check', command = check)
button.pack(side = LEFT)
button = Button(frame, text = 'reset', command = reset)
button.pack(side = LEFT)
button = Button(frame, text = 'solve', command = make_thread)
button.pack(side = LEFT)
pegs = []
for i in range(NUM_PEGS):
    pegs.append(Peg(i))
    #d is a black/white disk that represents the peg
    d = Disk(Peg.SEPARATION // Disk.DWIDTH)
    #must delete b/c initialization method draws it
    d.delete()
    d.color = 'white' if i % 2 == 0 else 'black'
    d.peg_num = i
    d.draw()
    #button for moving the pegs
    button = Button(frame,
                    text = 'Button %d' % (i),
                    command = partial(button_press, i))
    button.pack(side = LEFT)
frame.pack(side = BOTTOM)

#puts the disks on the first peg
reset()
start = time()

#begins the game
root.mainloop()

''' Instruction Manual:
    This game comes with a variety of buttons.
    
    The "print" button will print out the sizes of the disks
    on each peg, from greatest to least.

    The "check" button will check print if the puzzle has been
    solved. It also prints out the estimated number of moves if
    the problem has been solved. Whether the problem has been
    solved or not, it will also print out your current time
    and the current number of moves you have made.

    The "reset" button will put the game back to its starting
    position. It will also reset your timer and number of
    moves.

    The "solve" button will call reset() and solve the puzzle.
    When it is finished, it calls check() to print out
    information. Most other buttons will not function while
    the computer is solving the puzzle.

    Button 0, Button 1... Button n will do one of two things:
    If you have not selected a peg with a disk to move, then
    it will select the peg associated with the button.
    Otherwise, it will move the disk from the selected peg
    over to the peg whose button you pressed, and reset your
    selection.
    If you have made an invalid move (such as selecting an
    empty peg, or moving a disk onto a smaller one), then
    nothing will happen, and your selection will be reset.

    You can exit the game at any time using the X in the
    top right corner.

    The user will find several values they can edit. Most
    notably are the number of disks, the number of pegs,
    and the delay between each moves, given by NUM_DISKS,
    NUM_PEGS, and TIMER, respectively. The user may also edit
    the computer's solving algorithm in the make_thread method.
    It should be noted that the algorithms ending in _n3
    only work if there are exactly 3 pegs.
'''
