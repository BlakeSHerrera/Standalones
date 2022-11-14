from mouse import *
from time import sleep, time
from subprocess import call
import ctypes

start = time()

class NoteEventSequence:

    def __init__(self, data):
        self.data = data
        self.sequence = []
        data = data.replace('\n', '').replace(' ', '')
        data = data.split('|')
        for c in data:
            x = c.split('*')
            e = NoteEvent(float(x[0]), x[1])
            self.sequence.append(e)

    def play(self):
        for c in self.sequence:
            c.play()

    def __repr__(self):
        return self.data

class NoteEvent:
    
    def __init__(self, delay, data):
        self.delay = delay
        self.events = [KeyEvent(data[i:i+3]) for i in range(0, len(data), 3)]
        self.data = data

    def play(self):
        sleep(self.delay)
        for c in self.events:
            c.run()

class DelayedKeyEvent:

    def __init__(self, ke, dtime):
        self.ke = ke
        self.dtime = dtime

    def run(self):
        if self.dtime:
            sleep(self.dtime)
        self.ke.run()

    def __repr__(self):
        return str(self.ke) + ' ' + str(self.dtime)
    
class KeyEvent:

    shiftCode = keyCodes['SHIFT']
    
    def __init__(self, data):
        self.data = data
        self.prt = data[0]
        self.hexKeyCode = keyCodes[data[1]]
        self.isShifted = data[2] == '+'

    def run(self):
        if self.isShifted:
            pressKey(KeyEvent.shiftCode)
        if self.prt == '+':
            pressKey(self.hexKeyCode)
        elif self.prt == '-':
            releaseKey(self.hexKeyCode)
        else:
            pressKey(self.hexKeyCode)
            releaseKey(self.hexKeyCode)
        if self.isShifted:
            releaseKey(KeyEvent.shiftCode)

    def __repr__(self):
        return self.data

def bpm(x):
    return 60 / x

s = '''
112234455667
88990QQWWEER
TTYYUIIOOPPA
SSDDFGGHHJJK
LLZZXCCVVBBN
M'''.replace('\n', '')
#64 = C4 = T-
vp_key_codes = {}
last = ''
for c in range(36, 97):
    code = s[c - 36]
    code += '+' if code == last else '-'
    last = code[0]
    vp_key_codes[c] = code

path = 'Since We Met.txt'
if path.endswith('mid'):
    midicsv = 'midicsv-1.1/Midicsv.exe'
    cmd = midicsv + ' -v ' + path + ' ' + path[:-3] + 'txt'
    print(cmd)
    call(cmd)
    path = path[:-3] + 'txt'
    
f = open(path)
s = f.read().split('\n')
data = []
key_transpose = 0 #user set #notes up/down (12 = +octave)
for line in s:
    line = line.split(', ')
    try:
        cmd = line[2].lower()
    except IndexError:
        continue
    if cmd in ('note_on_c', 'note_off_c'):
        track = int(line[0])
        dtime = int(line[1])
        channel = int(line[3])
        note = int(line[4]) + key_transpose
        note = note + 12 if note < 36 else note
        velocity = int(line[5])
        if velocity and not cmd == 'note_off_c':
            if not (36 <= note <= 96):
                note = -1
                continue
            data.append([track, dtime, channel, note, velocity])
        else:
            pass

def mergesort_data(data):
    def mg_helper(data, left, right):
        mid = (right + left) // 2
        if right - left > 1:
            mg_helper(data, left, mid)
            mg_helper(data, mid, right)
        i = left
        j = mid
        tmp = []
        while i < mid and j < right:
            if data[i][1] <= data[j][1]:
                tmp.append(data[i])
                i += 1
            else:
                tmp.append(data[j])
                j += 1
        while i < mid:
            tmp.append(data[i])
            i += 1
        while j < right:
            tmp.append(data[j])
            j += 1
        for c in range(left, right):
            data[c] = tmp[c - left]
        del tmp
    mg_helper(data, 0, len(data))

#merge sort data by dtime
mergesort_data(data)
    
headerBPM = int(s[0].split(', ')[5])
print(headerBPM)
bpm = bpm(100) #user set
events = []
for c in range(1, len(data))[::-1]:
    #change to delta time, convert to real time delay
    data[c][1] = (data[c][1] - data[c - 1][1]) * bpm / headerBPM
for c in data:
    if c[3] != -1:
        ke = KeyEvent('=' + vp_key_codes[c[3]])
        events.append(DelayedKeyEvent(ke, c[1]))
f.close()
print('\nDone parsing in', time() - start, 'seconds.')

sleep(5)
for c in events:
    c.run()

print('\nDone playing.')
#http://www.fourmilab.ch/webtools/midicsv/
