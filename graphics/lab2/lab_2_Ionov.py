from OpenGL.GL import *
import pyglet
from pyglet.gl import gluPerspective
from pyglet.window import key
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

center_pos_x = 0
center_pos_y = 0
center_pos_z = 0
half_side_length = 2

main_cube_vertecies =  [
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


center_pos_x = 0
center_pos_y = 0
center_pos_z = 0
half_side_length = 0.3 * 0.5


small_cube_vertecies = [
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



def draw_cube(is_fill):
    color_p = 0
    if is_fill:
        mode = GL_FILL
    else:
        mode = GL_LINE
    for ind in indexes:
        vs = []
        for v in ind:
            vs.append(main_cube_vertecies[v])
        glPolygonMode(GL_FRONT_AND_BACK, mode)
        glBegin(GL_QUADS)
        for v in vs:
            glVertex3f(*v)
            glColor3ub(colors[color_p][0], colors[color_p][1], colors[color_p][2])
        glEnd()
        color_p += 1

def draw_static_cube():
    color_p = 0
    for ind in indexes:
        vs = []
        for v in ind:
            vs.append(small_cube_vertecies[v])
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glBegin(GL_QUADS)
        for v in vs:
            glVertex3f(*v)
            glColor3ub(colors[color_p][0], colors[color_p][1], colors[color_p][2])
        glEnd()
        color_p += 1


class MyWindow(pyglet.window.Window):

    rotation = {
        'x': 0,
        'y': 0,
        'z': 0,
    }
    translation = {
        'x': 0,
        'y': 0,
        'z': -4,
    }
    edge_len = 2
    speed = 1.5
    scale = 1
    is_fill = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        glClearColor(-6, -2, 0, 1)
        glEnable(GL_DEPTH_TEST)

    def on_draw(self):
        self.clear()
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-10, 10, -10, 10, 0, 20)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        glTranslatef(self.translation['x'], self.translation['y'], self.translation['z'])
        glRotatef(self.rotation['x'], 1, 0, 0)
        glRotatef(self.rotation['y'], 0, 1, 0)
        glRotatef(self.rotation['z'], 0, 0, 1)
        glScalef(self.scale, self.scale, self.scale)
        draw_cube(self.is_fill)
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
            self.is_fill = not self.is_fill
        elif s == key.W:
            self.translation['y'] += self.speed/3
        elif s == key.S:
            self.translation['y'] -= self.speed/3
        elif s == key.A:
            self.translation['x'] -= self.speed/3
        elif s == key.D:
            self.translation['x'] += self.speed/3
        elif s == key.F:
            self.translation['z'] -= self.speed/3
        elif s == key.N:
            self.translation['z'] += self.speed/3
        elif s == key.U:
            self.rotation['z'] -= self.speed
        elif s == key.J:
            self.rotation['z'] += self.speed
        elif s == key.X:
            self.scale *= 1.1
        elif s == key.C:
            self.scale /= 1.1


if __name__ == '__main__':
    MyWindow(720, 720, 'lab2', resizable=True)
    pyglet.app.run()
