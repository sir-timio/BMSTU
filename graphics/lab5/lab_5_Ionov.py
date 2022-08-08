from OpenGL.GL import *
import pyglet
from pyglet.window import key
import numpy as np

eps = 1e-09

# 11 вариант

clipped = False
pixel_size = 1
clipped_lines = []
center_pos_x = 0
center_pos_y = 0
center_pos_z = 0
half_side_length = 1
edge_len = 1


def ar(l):
    return np.array(l)


class Line:
    def __init__(self, p1, p2, f1=None, f2=None, i1=None, i2=None):
        self.p1 = p1
        self.p2 = p2
        self.v = p1 - p2
        self.show = True
        self.f1, self.f2, self.i1, self.i2 = f1, f2, i1, i2

    def len(self):
        return np.sqrt(np.dot(self.v, self.v))

    def display(self):
        if self.show:
            glVertex3f(self.p1[0], self.p1[1], self.p1[2])
            glVertex3f(self.p2[0], self.p2[1], self.p2[2])
        else:
            pass

    def in_cube(self):
        return all(abs(self.p1) <= edge_len) and all(abs(self.p2) <= edge_len)

    def is_intersect(self):
        return any([is_segment_int_plane(self, p) for p in planes])


class Plane:
    def __init__(self, v, n):
        self.v = v
        self.n = n


main_cube_vertecies = [
    # front face
    [center_pos_x - half_side_length, center_pos_y + half_side_length,
     center_pos_z - half_side_length],
    [center_pos_x + half_side_length, center_pos_y + half_side_length,
     center_pos_z - half_side_length],
    [center_pos_x + half_side_length, center_pos_y - half_side_length,
     center_pos_z - half_side_length],
    [center_pos_x - half_side_length, center_pos_y - half_side_length,
     center_pos_z - half_side_length],

    # back face
    [center_pos_x - half_side_length, center_pos_y + half_side_length,
     center_pos_z + half_side_length],
    [center_pos_x + half_side_length, center_pos_y + half_side_length,
     center_pos_z + half_side_length],
    [center_pos_x + half_side_length, center_pos_y - half_side_length,
     center_pos_z + half_side_length],
    [center_pos_x - half_side_length, center_pos_y - half_side_length,
     center_pos_z + half_side_length],

    # left face
    [center_pos_x + half_side_length, center_pos_y + half_side_length,
     center_pos_z + half_side_length],
    [center_pos_x + half_side_length, center_pos_y + half_side_length,
     center_pos_z - half_side_length],
    [center_pos_x + half_side_length, center_pos_y - half_side_length,
     center_pos_z - half_side_length],
    [center_pos_x + half_side_length, center_pos_y - half_side_length,
     center_pos_z + half_side_length],

    # right face
    [center_pos_x - half_side_length, center_pos_y + half_side_length,
     center_pos_z + half_side_length],
    [center_pos_x - half_side_length, center_pos_y + half_side_length,
     center_pos_z - half_side_length],
    [center_pos_x - half_side_length, center_pos_y - half_side_length,
     center_pos_z - half_side_length],
    [center_pos_x - half_side_length, center_pos_y - half_side_length,
     center_pos_z + half_side_length],

    # top face
    [center_pos_x - half_side_length, center_pos_y - half_side_length,
     center_pos_z + half_side_length],
    [center_pos_x - half_side_length, center_pos_y - half_side_length,
     center_pos_z - half_side_length],
    [center_pos_x + half_side_length, center_pos_y - half_side_length,
     center_pos_z - half_side_length],
    [center_pos_x + half_side_length, center_pos_y - half_side_length,
     center_pos_z + half_side_length],

    # bottom face
    [center_pos_x - half_side_length, center_pos_y + half_side_length,
     center_pos_z + half_side_length],
    [center_pos_x - half_side_length, center_pos_y + half_side_length,
     center_pos_z - half_side_length],
    [center_pos_x + half_side_length, center_pos_y + half_side_length,
     center_pos_z - half_side_length],
    [center_pos_x + half_side_length, center_pos_y + half_side_length,
     center_pos_z + half_side_length]
]

lines = [
    Line(ar([0, 0, 0]), ar([1, 2, 3])),
    Line(ar([-2, 0, 0]), ar([2, 0, 0])),
    Line(ar([0, -2, 0]), ar([0, 2, 0])),
    Line(ar([0.5, 0.5, 0]), ar([-0.5, 0.5, 0])),
    Line(ar([1.5, 2, 0]), ar([2, -2, 0])),
    Line(ar([-2.8, -2.2, 0]), ar([2.3, 2.9, 0])),
    Line(ar([0.5, 1.5, 0]), ar([-0.5, 1.5, 0])),
]

v_lines = []

planes = [
    Plane(ar([1, 1, -1]), ar([0, 0, -1])),
    Plane(ar([1, 1, 1]), ar([0, 0, 1])),

    Plane(ar([1, 1, 1]), ar([0, 1, 0])),
    Plane(ar([1, -1, -1]), ar([0, -1, 0])),

    Plane(ar([1, 1, 1]), ar([1, 0, 0])),
    Plane(ar([-1, 1, -1]), ar([-1, 0, 0])),
]


def draw_cube():
    indexes = [(0, 3, 2, 1),
               (2, 3, 7, 6),
               (0, 4, 7, 3),
               (1, 2, 6, 5),
               (4, 5, 6, 7),
               (0, 1, 5, 4)]
    color_p = 0
    for ind in indexes:
        vs = []
        for v in ind:
            vs.append(main_cube_vertecies[v])
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glBegin(GL_QUADS)
        glColor3f(1, 1, 1)
        color_p += 1
        for v in vs:
            glVertex3f(*v)
        glEnd()


def draw_lines():
    global lines
    glBegin(GL_LINES)
    glColor3f(1, 1, 0)
    for l in lines:
        l.display()
    glEnd()


def draw_clipped_lines():
    global lines
    glBegin(GL_LINES)
    glColor3f(0, 1, 1)
    for l in v_lines:
        if not l.i1 is None:
            Line(l.f1, l.i1).display()
        if not l.i2 is None:
            Line(l.f2, l.i2).display()
        else:
            Line(l.f1, l.f2).display()
    glEnd()


def point_inside(p):
    return all(abs(p) <= edge_len)


# Находим компоненты вектора CA (как разность координат точки С, они известны, и точки А, они тоже известны, т.к. это может быть любая точка из определяющих плоскость);
# Находим величину CN, скалярно умножив CA на n;
# Находим величину CM, скалярно умножив CV на n;
# Рассчитываем коэффициент К, как частное от деления CN на CM;

def is_segment_int_plane(l: Line, plane: Plane):
    n = plane.n
    a = plane.v
    c = l.p1
    v = l.p2

    cv = v - c
    ca = a - c
    cn = np.dot(ca, n)
    cm = np.dot(cv, n)

    if abs(cm) < eps:  # lies in plane or parallel
        return cn == 0

    k = cn / cm

    return 0 <= k <= 1


def is_point_near_cube(p):
    return all(abs(p) < 1 + 0.01)


def clipping(line: Line, id):
    global lines
    p1 = line.p1
    p2 = line.p2
    # print('#####################')
    # print(f'f1: {lines[id].f1}, f2: {lines[id].f2}, i1: {lines[id].i1}, i2: {lines[id].i2}, ints: {lines[id].ints}')

    if line.in_cube():
        return

    if lines[id].f1 is None and not point_inside(p1):  # нет видимой точки f1 и p1 вне куба
        lines[id].f1 = p1

    if lines[id].f2 is None and not point_inside(p2):  # нет видимой точки f2 и p2 вне куба
        lines[id].f2 = p2

    if not line.is_intersect():
        if lines[id] not in v_lines:
            v_lines.append(lines[id])
        return

    if line.len() < 0.01:  # незначителен
        if lines[id].f1 is None and lines[id].f2 is None:  # нет видимых точек
            return

        if not is_point_near_cube(p1):
            return

        if lines[id].i1 is None and not lines[id].f1 is None:
            lines[id].i1 = p1
            if lines[id] not in v_lines:
                v_lines.append(lines[id])
            return
        if lines[id].i2 is None and not lines[id].f2 is None:
            lines[id].i2 = p2
            if lines[id] not in v_lines:
                v_lines.append(lines[id])
            return
        return

    l = line.p1
    r = line.p2
    m = (p1 + p2) / 2

    if lines[id].is_intersect():
        clipping(Line(l, m), id)
        clipping(Line(m, r), id)


class MyWindow(pyglet.window.Window):
    rotation = {
        'x': -15,
        'y': 25,
        'z': 0,
    }
    translation = {
        'x': 0,
        'y': 0,
        'z': -2,
    }
    edge_len = 1
    speed = 1.5
    scale = 1
    is_fill = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        glClearColor(-6, -2, 0, 1)
        glEnable(GL_DEPTH_TEST)

    def on_draw(self):
        global lines, clipped
        self.clear()
        glClear(GL_COLOR_BUFFER_BIT)
        glViewport(0, 0, self.width, self.height)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-4, 4, -4, 4, 0, 4)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        glTranslatef(self.translation['x'], self.translation['y'], self.translation['z'])
        glRotatef(self.rotation['x'], 1, 0, 0)
        glRotatef(self.rotation['y'], 0, 1, 0)
        glRotatef(self.rotation['z'], 0, 0, 1)
        draw_cube()

        if not clipped:
            draw_lines()
        else:
            for i in range(len(lines)):
                clipping(lines[i], i)
            draw_clipped_lines()
        glPopMatrix()


    def on_text_motion(self, s):
        if s == key.UP:
            self.rotation['x'] -= self.speed
        elif s == key.DOWN:
            self.rotation['x'] += self.speed
        elif s == key.LEFT:
            self.rotation['y'] -= self.speed
        elif s == key.RIGHT:
            self.rotation['y'] += self.speed

    def on_key_press(self, s, modifiers):
        global mode, clipped
        if s == key.C:
            clipped = not clipped
            self.on_draw()


if __name__ == '__main__':
    MyWindow(720, 720, 'lab5', resizable=True, screen=0)
    pyglet.app.run()
