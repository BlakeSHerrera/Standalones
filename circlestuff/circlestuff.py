#circlestuff

from tkinter import *
from math import *
from random import *
from time import *

WIDTH = 1920 - 25
HEIGHT = 1080 - 100
DEFAULT_THICKNESS = 4

id_num = 0
start = time()

class Polygon:

    def __init__(self, coords,
                 fill = '',
                 outline = '#FF007F',
                 outline_thickness = DEFAULT_THICKNESS):
        self.fill = fill
        self.outline = outline
        self.outline_thickness = outline_thickness
        
        self.op = []
        self.sp = []
        for i in range(0, len(coords) - 1, 2):
            self.op.append(Point(coords[i], coords[i + 1]))
            self.sp.append(Point(coords[i], coords[i + 1]))
        self.id_num = 0

    def reset_sc(self):
        for i in range(len(self.op)):
            self.sp[i] = self.op[i].copy()

    def transform(self, center, dx, dy, dt, ds):
        for i in self.sp:
            i.transform(center, dx, dy, dt, ds)

    def rotate_sc(self, rads, center):
        for i in self.sp:
            i.rotate_about(center, rads)

    def rotate_oc(self, rads, center):
        for i in self.sp:
            i.rot_cos(center, rads)

    def coords(self, info = False):
        points = []
        for i in self.sp:
            if info:
                print('', i)
            points += [i.x, i.y]
        return tuple(points)
    
    def draw_on(self, canvas):
        coords = []
        for i in self.sp:
            print('', i)
            coords += [i.x, i.y]
        self.id_num = canvas.create_polygon(
            coords,
            fill = self.fill,
            outline = self.outline,
            width = self.outline_thickness)
        print(self.id_num, len(self.op))

    def redraw_on(self, canvas):
        coords = []
        for i in self.sp:
            coords += [i.x, i.y]
        canvas.coords(self.id_num, tuple(coords))

class Circle:
    
    def __init__(self, x, y, r,
                 fill = '',
                 outline = '#FF007F',
                 outline_thickness = DEFAULT_THICKNESS,
                 should_fill = True):
        if r < 2:
            should_fill = False
        self.oc = Point(x, y)
        self.sc = Point(x, y)
        self.ro = r
        self.rs = r
        self.fill = fill
        self.outline = outline
        self.outline_thickness = outline_thickness

        self.id_num = 0
        self.rotation = 0
        self.inner_circles = []
        self.inner_polygons = []
        if(should_fill):
            self.fill_space(True)

    def __repr__(self):
        return '%d, (%.2f, %.2f), r=%.2f' % (
            self.id_num, self.sc.x, self.sc.y, self.rs)

    def get_x(self, theta):
        return self.sc.x + self.rs * cos(theta)

    def get_y(self, theta):
        return self.sc.y + self.rs * sin(theta)

    def get_xy(self, theta):
        return Point(self.get_x(theta), self.get_y(theta))

    def bbox(self):
        return (self.sc.x - self.rs,
                self.sc.y - self.rs,
                self.sc.x + self.rs,
                self.sc.y + self.rs)

    def reset_sc(self):
        self.sc = self.oc.copy()
        self.rs = self.ro
        for i in self.inner_circles + self.inner_polygons:
            i.reset_sc()

    def rotate_sc(self, rads, center = None):
        if center is None:
            center = self.sc
        self.sc.rotate_about(center, rads)
        for i in self.inner_circles:
            i.rotate_sc(rads, center)
            i.rotate_sc(rads)
        for i in self.inner_polygons:
            i.rotate_sc(rads, center)

    def rotate_oc(self, rads, center = None):
        if center is None:
            center = self.sc
        self.sc.rot_cos(center, rads)
        for i in self.inner_circles:
            i.rotate_oc(rads, center)
            i.rotate_oc(rads)
        for i in self.inner_polygons:
            i.rotate_oc(rads, center)
        
    def area(self):
        return pi * rs ** 2

    def transform(self, center, dx, dy, dt, ds):
        self.sc.transform(center, dx, dy, dt, ds)
        self.rs *= ds
        for i in inner_circles + inner_polygons:
            i.transform(center, dx, dy, dt, ds)

    def draw_on(self, canvas):
        self.id_num = canvas.create_oval(
            self.bbox(),
            fill = self.fill,
            outline = self.outline,
            width = self.outline_thickness)
        print(self)
        for i in self.inner_circles + self.inner_polygons:
            i.draw_on(canvas)

    def redraw_on(self, canvas):
        #swap sc for oc = fun
        canvas.coords(
            self.id_num,
            self.bbox())
        for i in self.inner_circles + self.inner_polygons:
            i.redraw_on(canvas)

    def circle_inversion(self, c, use_oc = False):
        center = self.oc if use_oc else self.sc
        l = Line(center, c.sc)
        p1 = self.get_xy(l.t1())
        p2 = self.get_xy(l.t2())
        p1.circle_inversion(c)
        p2.circle_inversion(c)
        x = avg(p1.x, p2.x)
        y = avg(p1.y, p2.y)
        self.sc = Point(x, y)
        self.rs = p1.dist_from(p2) / 2
        if use_oc:
            self.oc = self.sc.copy()
            self.ro = self.rs

    def tan_line(self, dt):
        p1 = self.get_xy(dt)
        p2 = self.get_xy(dt - pi / 4)
        p2.zoom_about(self.sc, sqrt(2))
        return Line(p1, p2)

    def norm_line(self, dt):
        return Line(self.sc, self.get_xy(dt))

    def fill_space(self,
                   should_fill = True,
                   limit_r = None):
        if self.rs < 10:
            return
        r = randint(1, 12)
        #if not Circle.limit_r is None:
            #r = choice(Circle.limit_r)
        print('rand =', r)
        if r == 0:
            #empty
            pass
        elif r == 1:
            self.c_fill_1(should_fill)
        elif r == 2:
            self.c_fill_2(should_fill)
        elif r == 3:
            self.c_fill_3(should_fill)
        elif r == 4:
            self.c_fill_4()
        elif r == 5:
            self.c_fill_5(should_fill)
        elif r == 6:
            self.c_fill_6()
        elif r == 7:
            self.c_fill_7(should_fill)
        elif r == 8:
            self.c_fill_8(should_fill) #TODO
        elif r == 9:
            self.c_fill_9(should_fill) #TODO
        elif r == 10:
            #smaller circle, edge touching
            pass
        elif r == 12:
            self.c_fill_12(should_fill)

        #smaller circle, edge touching, ring of circles around edge
        #smaller circle, edge not touching, + ring of circles
        #yin yang
        #n-yang
        #Fibonacci spiral
        #Fibonacci spiral of circles

    def c_fill_1(self,
                 should_fill = False,
                 r_lower = .50,
                 r_higher = .95):
        #smaller circle, concentric
        #radius between 50% and 95%
        r = random() * self.rs * r_lower + self.rs * (r_higher - r_lower)
        #r = r if force_r is None else force_r
        self.inner_circles.append(Circle(
            self.sc.x,
            self.sc.y,
            r,
            self.fill,
            self.outline,
            self.outline_thickness,
            should_fill = should_fill))

    def c_fill_2(self,
                 should_fill = False,
                 force_n = None):
        #n circle border, same size, r > 50%
        n = randint(3, 12) if force_n is None else force_n
        dt = 2 * pi / n
        r = avg(self.rs * hypot(1 - cos(dt), sin(dt)) / 2,
                self.rs)
        for i in range(n):
            self.inner_circles.append(Circle(
                self.get_x(dt * i) - r * cos(dt * i),
                self.get_y(dt * i) - r * sin(dt * i),
                r,
                should_fill = False))
        self.inner_circles.append(Circle(
            self.sc.x,
            self.sc.y,
            2 * r - self.rs,
            should_fill = should_fill))

    def c_fill_3(self,
                 should_fill = False,
                 force_n = None):
        #n circle border inverse, same size, r > 50%
        n = randint(3, 12) if force_n is None else force_n
        dt = 2 * pi / n
        r = avg(self.rs - self.rs * hypot(1 - cos(dt), sin(dt)) / 2,
                self.rs)
        for i in range(n):
            self.inner_circles.append(Circle(
                self.get_x(dt * i) - r * cos(dt * i),
                self.get_y(dt * i) - r * sin(dt * i),
                r,
                should_fill = False))
        self.inner_circles.append(Circle(
            self.sc.x,
            self.sc.y,
            2 * r - self.rs,
            should_fill = should_fill))

    def c_fill_4(self,
                 force_n = None):
        #n circle border, same size, r = 50%
        n = randint(2, 8) if force_n is None else force_n
        dt = 2 * pi / n
        r = self.rs / 2
        for i in range(n):
            self.inner_circles.append(Circle(
                self.get_x(dt * i) - r * cos(dt * i),
                self.get_y(dt * i) - r * sin(dt * i),
                r,
                should_fill = False))

    def c_fill_5(self,
                 should_fill_inner = False,
                 should_fill_outer = False, #warning on True
                 force_n = None):
        #n circle border, same size, r < 50%
        n = randint(2, 8) if force_n is None else force_n
        r = self.rs * sin(pi / n) / (sin(pi / n) + 1)
        dt = 2 * pi / n
        for i in range(n):
            self.inner_circles.append(Circle(
                self.get_x(dt * i) - r * cos(dt * i),
                self.get_y(dt * i) - r * sin(dt * i),
                r,
                should_fill = should_fill_outer)) #warning on True
        self.inner_circles.append(Circle(
            self.sc.x,
            self.sc.y,
            self.rs - 2 * r,
            should_fill = should_fill_inner))

    def c_fill_6(self,
                 should_fill = False,
                 force_n = None):
        #n circles, random proportions
        n = randint(2, 8) if force_n is None else force_n
        pass

    def c_fill_7(self,
                 should_fill = False,
                 force_n = None):
        #inscribed regular polygon with inscribed circle
        n = randint(3, 5) if force_n is None else force_n
        dt = 2 * pi / n
        coords = []
        for i in range(n):
            p = self.get_xy(dt * i)
            coords.append(p.x)
            coords.append(p.y)
        self.inner_polygons.append(Polygon(coords))
        self.inner_circles.append(Circle(
            self.sc.x,
            self.sc.y,
            self.rs * sin(rad((n - 2) * 90 / n)),
            should_fill = should_fill))

    def c_fill_8(self,
                 should_fill = False,
                 force_n = None):
        #inscribed regular star
        n = randint(4, 10) if force_n is None else force_n
        dt = 2 * pi / n
        coords = []
        if n % 2 == 1:
            for i in range(n):
                p = self.get_xy(2 * dt * i)
                coords.append(p.x)
                coords.append(p.y)
        else:
            for i in range(0, n, 2):
                p = self.get_xy(dt * i)
                coords.append(p.x)
                coords.append(p.y)
            self.inner_polygons.append(Polygon(coords))
            coords = []
            for i in range(1, n, 2):
                coords += [
                    self.sc.x + self.rs * cos(dt * i),
                    self.sc.y + self.rs * sin(dt * i)]
        self.inner_polygons.append(Polygon(coords))
        #TODO find inscribed circle

    def c_fill_9(self,
                 should_fill = False,
                 force_n = None):
        #inscribed regular polygon and star
        n = randint(4, 10) if force_n is None else force_n
        dt = 2 * pi / n
        coords = []
        for i in range(n):
            coords += [
                self.get_x(i * dt),
                self.get_y(i * dt),
                self.get_x((i + 2) * dt),
                self.get_y((i + 2) * dt)]
        self.inner_polygons.append(Polygon(coords))
        #TODO find inscribed circle

    def c_fill_10(self,
                  should_fill = False,
                  force_n = None):
        #inscribed n-tagram
        lis = [7, 8, 9, 11, 12]
        n = choice(lis) if force_n is None else force_n
        dt = 2 * pi / n
        coords = []
        for i in range(n):
            coords += [
                self.get_x((n - 1) // 2 * i * dt),
                self.get_y((n - 1) // 2 * i * dt)]
        self.inner_polygons.append(Polygon(coords))

    def c_fill_11(self,
                  should_fill = False,
                  force_n = None):
        #cluster of lines
        n = randint(4, 8) if force_n is None else force_n
        dt = 2 * pi / n
        coords = []
        for i in range(n):
            for j in range(i + 1, n)[::-1]:
                coords += [
                    self.get_x(i * dt),
                    self.get_y(i * dt),
                    self.get_x(j * dt),
                    self.get_y(j * dt)]
        self.inner_polygons.append(Polygon(coords))

    def c_fill_12(self,
                  force_n = None,
                  should_fill = False):
        #n-yang
        n = randint(2, 4) if force_n is None else force_n
        dt = 2 * pi / n
        r = self.rs * sin(pi / n) / (sin(pi / n) + 1)
        for i in range(n):
            c = Circle(
                self.get_x(dt * i) - r * cos(dt * i),
                self.get_y(dt * i) - r * sin(dt * i),
                r,
                should_fill = False)
            c_next = Circle(
                self.get_x(dt * (i + 1)) - r * cos(dt * (i + 1)),
                self.get_y(dt * (i + 1)) - r * sin(dt * (i + 1)),
                r,
                should_fill = False)
            c_of_i = Circle(
                c.get_x(dt * i),
                c.get_y(dt * i),
                c.rs * 2,
                should_fill = False)
            c_next.circle_inversion(c_of_i, True)
            theta = dt * i + pi / 2
            for j in range(10):
                p = Point(
                    c_next.sc.x,
                    c_next.sc.y)
                p.translate(
                    j * 2 * c_next.rs * cos(theta),
                    j * 2 * c_next.rs * sin(theta))
                circ = Circle(
                    p.x, p.y, c_next.rs,
                    should_fill = False)
                circ.circle_inversion(c_of_i, True)
                if circ.ro < 10:
                    break
                self.inner_circles.append(Circle(
                    circ.oc.x, circ.oc.y, circ.ro,
                    should_fill = should_fill))

    def c_fill_13(self):
        pass

class Line:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def x(self, y):
        m = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
        b = self.p1.y - m * p1.x
        return (y - b) / m

    def y(self, x):
        m = (self.p2.y - self.p1.y) / (self.p2.x - self.p1.x)
        b = self.p1.y - m * p1.x
        return self.m * x + self.b

    def transform(self, center, dx, dy, dt, ds):
        self.p1.transform(center, dx, dy, dt, ds)
        self.p2.transform(center, dx, dy, dt, ds)

    def translate(self, dx, dy):
        self.p1.translate(dx, dy)
        self.p2.translate(dx, dy)

    def rotate_about(self, center, dt):
        self.p1.rotate(center, dt)
        self.p2.rotate(center, dt)

    def zoom_about(self, center, ds):
        self.p1.zoom_about(center, ds)
        self.p2.zoom_about(center, ds)

    def t1(self):
        return atan2(self.p2.y - self.p1.y,
                     self.p2.x - self.p1.x)

    def t2(self):
        return atan2(self.p1.y - self.p2.y,
                     self.p1.x - self.p2.x)

    def midpoint(self):
        return Point((self.p1.x + self.p2.x) / 2,
                     (self.p1.y + self.p2.y) / 2)

    def length(self):
        return self.p1.dist_from(self.p2)

class Point:

    def __init__(self, x, y):
        if type(x) == Point or type(y) == Point:
            raise Exception()
        self.x = x
        self.y = y

    def __repr__(self):
        print(self.x, self.y, type(self.x), type(self.y))
        return '(%.2f, %.2f)' % (self.x, self.y)

    def copy(self):
        return Point(self.x, self.y)

    def circle_inversion(self, c):
        oa = Line(self, c.sc)
        d = oa.length()
        if d < 1:
            message = 'Cannot invert point at circle center'
            raise Exception(message)
        d_pr = c.rs ** 2 / d
        zm = d_pr / d
        self.zoom_about(c.sc, zm)

    def dist_from(self, other_point):
        x = self.x - other_point.x
        y = self.y - other_point.y
        return sqrt(x ** 2 + y ** 2)
    
    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate_about(self, center, dt):
        if self.x == center.x and self.y == center.y:
            return
        hypot = self.dist_from(center)
        theta = atan2(self.y - center.y, self.x - center.x) + dt
        self.x = center.x + hypot * cos(theta)
        self.y = center.y + hypot * sin(theta)

    def rot_cos(self, center, dt):
        if self.x == center.x and self.y == center.y:
            return
        hypot = self.dist_from(center) * cos(dt)
        theta = atan2(self.y - center.y, self.x - center.x) + dt
        self.x = center.x + hypot * cos(theta)
        self.y = center.y + hypot * sin(theta)

    def zoom_about(self, center, scale):
        self.x = (self.x - center.x) * scale + center.x
        self.y = (self.y - center.y) * scale + center.y

    def transform(self, center, dx, dy, dt, ds):
        self.translate(dx, dy)
        self.rotate_about(center, dt)
        self.zoom_about(center, ds)

    def mid(x0, y0, x1, y1):
        return Point((x0 + x1) / 2, (y0 + y1) / 2)

def rad(deg):
    return deg * pi / 180

def deg(rad):
    return rad * 180 / pi

def avg(*nums):
    return sum(nums)/len(nums)

def get_rot():
    global start
    return (time() - start) * pi / 15

divisors = [c for c in range(1, 360) if 360 % c == 0]

root = Tk()

w = Canvas(root, width=WIDTH, height=HEIGHT, bg='black')
w.pack()

Circle.limit_r = [12]
m = []
m.append(Circle(WIDTH // 2, HEIGHT // 2, min(WIDTH, HEIGHT) // 2,
                should_fill = True))
#m[-1].c_fill_10(force_n = 5)


for i in m:
    i.draw_on(w)

def redo_stuff():
    root.after(34, redo_stuff)
    r = get_rot()
    for i in m:
        i.reset_sc()
        i.rotate_sc(r)
        i.redraw_on(w)

root.after(-1, redo_stuff)
root.mainloop()
