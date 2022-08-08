from pyglet.gl import *
from pyglet.window import key
from math import *
import numpy as np

mode = GL_FILL

colors = [[255, 128, 0],
          [200, 40, 10],
          [70, 200, 10],
          [20, 150, 20],
          [20, 20, 230],
          [200, 20, 200],
          [222, 188, 188],
          [20, 230, 160]]

indexes = [(0, 3, 2, 1),
           (2, 3, 7, 6),
           (0, 4, 7, 3),
           (1, 2, 6, 5),
           (4, 5, 6, 7),
           (0, 1, 5, 4)]

re_draw = True


def set_re_draw(state):
    global re_draw
    re_draw = state


side_vertecies = []
inner_vertecies = []
center = []
color = []

center_pos_x = 0
center_pos_y = 0
center_pos_z = 0
half_side_length = 0.3 * 0.5

cube_vertecies = [
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


def draw_cube():
    color_p = 0
    for ind in indexes:
        vs = []
        for v in ind:
            vs.append(cube_vertecies[v])
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBegin(GL_QUADS)
        for v in vs:
            glVertex3f(*v)
            glColor3ub(colors[color_p][0], colors[color_p][1], colors[color_p][2])
        glEnd()
        color_p += 1


def make_elliptical_cyclinder(a, b, h, slices, h_slices):
    global inner_vertecies, center, side_vertecies, color
    hl = h / 2
    side_vertecies.clear()
    inner_vertecies.clear()
    center.clear()
    color.clear()

    # make inner

    dh = 0
    center = []
    inner_vertecies = [[[] for i in range(slices + 1)] for j in range(h_slices + 1)]

    for j in range(h_slices + 1):
        center.append([0.0, dh - hl, 0.0])
        for i in range(slices + 1):
            theta = i * 2. * pi / slices
            next_theta = (i + 1) * 2. * pi / slices
            v1 = [a * cos(theta), dh - hl, b * sin(theta)]
            v2 = [a * cos(next_theta), dh - hl, b * sin(next_theta)]
            inner_vertecies[j][i].append(v1)
            inner_vertecies[j][i].append(v2)
        dh += h / h_slices

    # make side

    side_vertecies = [[] for i in range(slices + 1)]
    color = [[] for i in range(slices + 1)]
    for i in range(slices + 1):
        theta = i * 2. * pi / slices
        next_theta = (i + 1) * 2. * pi / slices
        color[i] = [(cos(theta) + 1) / 2., (sin(theta) + 0.7) / 2., cos(theta) * sin(theta)]
        side_vertecies[i].append([a * cos(theta), -hl, b * sin(theta)])
        side_vertecies[i].append([a * cos(theta), hl, b * sin(theta)])
        side_vertecies[i].append([a * cos(next_theta), -hl, b * sin(next_theta)])
        side_vertecies[i].append([a * cos(next_theta), hl, b * sin(next_theta)])


def draw_elliptical_cyclinder(a, b, h, slices, h_slices):
    # x = a*cos(t), y = b*sin(t)
    global mode, inner_vertecies, center, side_vertecies, re_draw
    hl = h / 2.
    glPolygonMode(GL_FRONT_AND_BACK, mode)
    glShadeModel(GL_SMOOTH)

    if re_draw:
        make_elliptical_cyclinder(a, b, h, slices, h_slices)
        set_re_draw(False)

    # draw inner
    for j in range(h_slices + 1):
        c = center[j]
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(c[0], c[1], c[2])
        for i in range(slices + 1):
            v1 = inner_vertecies[j][i][0]
            v2 = inner_vertecies[j][i][1]
            glVertex3f(v1[0], v1[1], v1[2])
            glVertex3f(v2[0], v2[1], v2[2])
        glEnd()
    # draw side

    glBegin(GL_QUAD_STRIP)
    for i in range(slices + 1):
        theta = i * 2. * pi / slices
        next_theta = (i + 1) * 2. * pi / slices
        clr = color[i]
        glColor3f(clr[0], clr[1], clr[2])
        side = side_vertecies[i]
        for p in side:
            glVertex3f(p[0], p[1], p[2])
    glEnd()


class MyWindow(pyglet.window.Window):
    rotation = {
        'x': 0,
        'y': 0,
        'z': 0,
    }
    translation = {
        'x': 2,
        'y': -1,
        'z': -3,
    }
    speed = 2
    scale = 1.2
    slices = 20
    h_slices = 10
    h = 3
    a = 1.5
    b = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        glClearColor(-6, -2, 0, 1)
        glEnable(GL_DEPTH_TEST)
        make_elliptical_cyclinder(self.a, self.b, self.h, self.slices, self.h_slices)

    def on_draw(self):
        self.clear()
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1, 0.1, 10)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(-0.5, -0.5, -3)
        draw_cube()

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-2, 2, -2, 2, 1, 20.0)
        glRotatef(15, 1, 0, 0)
        glRotatef(15, 0, 1, 0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        glTranslatef(self.translation['x'], self.translation['y'], self.translation['z'])
        glRotatef(self.rotation['x'], 1, 0, 0)
        glRotatef(self.rotation['y'], 0, 1, 0)
        glRotatef(self.rotation['z'], 0, 0, 1)
        glScalef(self.scale, self.scale, self.scale)
        draw_elliptical_cyclinder(self.a, self.b, self.h, self.slices, self.h_slices)
        glPopMatrix()

    def on_resize(self, width, height):
        glViewport(0, 0, min(width, height), min(width, height))

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
        global mode
        if s == key.SPACE:
            if mode == GL_LINE:
                mode = GL_FILL
            else:
                mode = GL_LINE
        elif s == key.W:
            self.translation['y'] += self.speed
        elif s == key.S:
            self.translation['y'] -= self.speed
        elif s == key.A:
            self.translation['x'] -= self.speed
        elif s == key.D:
            self.translation['x'] += self.speed
        elif s == key.F:
            self.translation['z'] -= self.speed
        elif s == key.N:
            self.translation['z'] += self.speed
        elif s == key.U:
            self.rotation['z'] -= self.speed
        elif s == key.J:
            self.rotation['z'] += self.speed
        elif s == key.X:
            self.scale *= 1.1
            set_re_draw(True)
        elif s == key.C:
            self.scale /= 1.1
            set_re_draw(True)
        elif s == key.L and self.slices > 5:
            self.slices -= 5
            set_re_draw(True)
        elif s == key.K and self.slices < 1000:
            self.slices += 5
            set_re_draw(True)
        elif s == key._1:
            self.a += 0.1
            set_re_draw(True)
        elif s == key._2 and self.a > 0.3:
            self.a -= 0.1
            set_re_draw(True)
        elif s == key._3:
            self.b += 0.1
            set_re_draw(True)
        elif s == key._4 and self.b > 0.3:
            self.b -= 0.1
            set_re_draw(True)
        elif s == key.I and self.h_slices < 100:
            self.h_slices += 1
            set_re_draw(True)
        elif s == key.O and self.h_slices > 2:
            self.h_slices -= 1
            set_re_draw(True)


if __name__ == '__main__':
    window = MyWindow(720, 720, 'lab3', resizable=True)
    pyglet.app.run()
