from pyglet.gl import *
from pyglet.window import key
from math import *
import numpy as np
import time
import json
from ctypes import pointer, sizeof
import itertools
flatten = itertools.chain.from_iterable

import time
from pyglet import clock
fps_display = pyglet.clock.Clock()

'''
1) загрузка текстуры только 1 раз
2) очищаем массив точек только если он не пустой
3) отлючение встроенной нормализации
4) отсечение обратных граней glEnable(GL_CULL_FACE)
5) дисплейные списки
6) буффер вершин, нормалей,текстурных координат
'''

buff_names = ['inner_vs', 'side_vs', 'color', 'inner_norms',
              'side_norms', 'side_text', 'inner_text',
              'cube_vs', 'cube_clr', 'cube_norms']
id_map = {}
for n in buff_names:
    id_map[n] = GLuint(0)



class Cube():

    def __init__(self):
        self.d_list = None
        center_pos_x = 0
        center_pos_y = 0
        center_pos_z = 0
        half_side_length = 0.3 * 0.5
        self.tex_vs = [
            [0, 0],
            [0, 1],
            [1, 1],
            [1, 0]
        ]

        self.colors = [[255, 128, 0],
                  [200, 40, 10],
                  [70, 200, 10],
                  [20, 150, 20],
                  [20, 20, 230],
                  [200, 20, 200],
                  [222, 188, 188],
                  [20, 230, 160]]

        self.indexes = [(0, 3, 2, 1),
                   (2, 3, 7, 6),
                   (0, 4, 7, 3),
                   (1, 2, 6, 5),
                   (4, 5, 6, 7),
                   (0, 1, 5, 4)]

        self.vertecies = [
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

        self.gen_display_list()

    def gen_display_list(self):
        id = glGenLists(1)
        self.d_list = id
        glNewList(id, GL_COMPILE)
        self.draw()
        glEndList()

    def make_vbo(self):
        vs = list(flatten(list(flatten(self.vertecies))))
        vs = (GLfloat * len(vs))(*vs)

        glGenBuffers(1, pointer(id_map['cube_vs']))
        glBindBuffer(GL_ARRAY_BUFFER, id_map['cube_vs'])
        glBufferData(GL_ARRAY_BUFFER, sizeof(vs), vs, GL_STATIC_DRAW)

    def draw_vbo(self):
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, id_map['cube_vs'])
        glVertexPointer(3, GL_FLOAT, 0, 0)



    def draw(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        color_p = 0
        glColor3f(1, 1, 1)
        for ind in self.indexes:
            vs = []
            for v in ind:
                vs.append(self.vertecies[v])
            glBegin(GL_QUADS)
            t_p = 0
            for v in vs[::-1]:
                glTexCoord2f(*self.tex_vs[t_p])
                t_p += 1
                glNormal3f(*v)
                glVertex3f(*v)
                glColor3ub(self.colors[color_p][0], self.colors[color_p][1], self.colors[color_p][2])
            glEnd()
            color_p += 1

    def display(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, 1, 0.1, 10)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(-0.7, -0.7, -3)
        glCallList(self.d_list)


class Cylinder():
    def __init__(self):
        self.speed = 2
        self.scale = 1.2
        self.slices = 10
        self.h_slices = 2
        self.h = 3
        self.a = 1
        self.b = 1
        self.dx = 0.3

        self.side_vertecies = []
        self.inner_vertecies = []
        self.color = []
        self.color_vbo = []

        self.norms = []
        self.side_text = []

        self.rotation = {
            'x': 0,
            'y': 0,
            'z': 0,
        }

        self.translation = {
            'x': 1,
            'y': -1,
            'z': -4,
        }

        self.re_draw = True
        self.mode = GL_FILL
        self.texture_on = 0
        self.light_on = 0


        self.display_list = 0
        self.gen_display_list()
        self.make_vbo()

    def gen_display_list(self):
        id = glGenLists(1)
        self.display_list = id
        glNewList(id, GL_COMPILE)
        self.make()
        self.make_vbo()
        self.draw_vbo()
        glEndList()

    def make_vbo(self):
        self.make()
        # inner points formula (self.h_slices+1) * (2 * (self.slices + 1) + 1)
        # side points formula (4 * (self.slices + 1))

        # side vertexes buff
        vs = list(flatten(list(flatten(self.side_vertecies))))
        vs = (GLfloat * len(vs))(*vs)

        glGenBuffers(1, pointer(id_map['side_vs']))
        glBindBuffer(GL_ARRAY_BUFFER, id_map['side_vs'])
        glBufferData(GL_ARRAY_BUFFER, sizeof(vs), vs, GL_STATIC_DRAW)

        # side norms
        norms = (GLfloat * len(vs))(*vs)

        glGenBuffers(1, pointer(id_map['side_norms']))
        glBindBuffer(GL_ARRAY_BUFFER, id_map['side_norms'])
        glBufferData(GL_ARRAY_BUFFER, sizeof(norms), norms, GL_STATIC_DRAW)

        # side color
        color = self.color_vbo
        color = (GLfloat * len(color))(*color)

        glGenBuffers(1, pointer(id_map['color']))
        glBindBuffer(GL_ARRAY_BUFFER, id_map['color'])
        glBufferData(GL_ARRAY_BUFFER, sizeof(color), color, GL_STATIC_DRAW)

        # side texture
        texture = list(flatten(list(flatten(self.side_text))))
        texture = (GLfloat * len(texture))(*texture)

        glGenBuffers(1, pointer(id_map['side_text']))
        glBindBuffer(GL_ARRAY_BUFFER, id_map['side_text'])
        glBufferData(GL_ARRAY_BUFFER, sizeof(texture), texture, GL_STATIC_DRAW)

        ############################

        # inner vertexes buff
        vs = list(flatten(list(flatten(self.inner_vertecies))))
        vs = (GLfloat * len(vs))(*vs)

        glGenBuffers(1, pointer(id_map['inner_vs']))
        glBindBuffer(GL_ARRAY_BUFFER, id_map['inner_vs'])
        glBufferData(GL_ARRAY_BUFFER, sizeof(vs), vs, GL_STATIC_DRAW)

        # inner norms
        norms = (GLfloat * len(vs))(*vs)

        glGenBuffers(1, pointer(id_map['inner_norms']))
        glBindBuffer(GL_ARRAY_BUFFER, id_map['inner_norms'])
        glBufferData(GL_ARRAY_BUFFER, sizeof(norms), norms, GL_STATIC_DRAW)

        # inner texture
        texture = list(flatten(list(flatten(self.side_text))))
        texture = (GLfloat * len(texture))(*texture)

        glGenBuffers(1, pointer(id_map['inner_text']))
        glBindBuffer(GL_ARRAY_BUFFER, id_map['inner_text'])
        glBufferData(GL_ARRAY_BUFFER, sizeof(texture), texture, GL_STATIC_DRAW)


    def draw_vbo(self):
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)
        global id0, id1, id2
        if self.re_draw:
            self.make_vbo()
            self.re_draw = 0

        # draw side
        # color
        glEnableClientState(GL_COLOR_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, id_map['color'])
        glColorPointer(3, GL_FLOAT, 0, 0)

        # norms
        glEnableClientState(GL_NORMAL_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, id_map['side_norms'])
        glNormalPointer(GL_FLOAT, 0, 0)

        # texture
        glEnableClientState(GL_TEXTURE_COORD_ARRAY_EXT)
        glBindBuffer(GL_ARRAY_BUFFER, id_map['side_text'])
        glTexCoordPointer(2, GL_FLOAT, 0, 0)
        # vs
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, id_map['side_vs'])
        glVertexPointer(3, GL_FLOAT, 0, 0)
        glDrawArrays(GL_QUAD_STRIP, 0, 4 * (self.slices + 1))
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY_EXT)

        # draw inner

        # norms
        glEnableClientState(GL_NORMAL_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, id_map['inner_norms'])
        glNormalPointer(GL_FLOAT, 0, 0)

        # texture
        glEnableClientState(GL_TEXTURE_COORD_ARRAY_EXT)
        glBindBuffer(GL_ARRAY_BUFFER, id_map['inner_text'])
        glTexCoordPointer(2, GL_FLOAT, 0, 0)

        # vs
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, id_map['inner_vs'])
        glVertexPointer(3, GL_FLOAT, 0, 0)
        for i in range(self.h_slices + 1):
            glDrawArrays(GL_TRIANGLE_FAN, i * (self.slices + 2), self.slices + 2)

        glBindBuffer(GL_ARRAY_BUFFER, 0)


        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY_EXT)


    def display(self):

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(-2, 2, -2, 2, 1, 20.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glPushMatrix()
        glTranslatef(self.translation['x'], self.translation['y'], self.translation['z'])
        glRotatef(self.rotation['x'], 1, 0, 0)
        glRotatef(self.rotation['y'], 0, 1, 0)
        glRotatef(self.rotation['z'], 0, 0, 1)
        glScalef(self.scale, self.scale, self.scale)
        glColor3f(141/255, 50/255, 168/255)
        if self.re_draw:
            glDeleteLists(self.display_list, 1)
            self.gen_display_list()
        glCallList(self.display_list)
        glPopMatrix()

    def draw(self):
        # x = a*cos(t), y = b*sin(t)
        glPolygonMode(GL_FRONT_AND_BACK, self.mode)
        if self.re_draw:
            self.make()


        # draw inner
        for j in range(self.h_slices+1):
            c = self.inner_vertecies[j][0]
            glBegin(GL_TRIANGLE_FAN)
            if self.light_on:
                glNormal3f(*c)
            glVertex3f(*c)
            for i in range(1, 2 * self.slices + 3):
                v = self.inner_vertecies[j][i]
                if self.light_on:
                    glNormal3f(*v)
                glVertex3f(*v)
                if self.light_on:
                    glNormal3f(*v)
            glEnd()

        # draw side
        glBegin(GL_QUAD_STRIP)
        for i in range(self.slices + 1):
            clr = self.color[i]
            side = self.side_vertecies[i]
            text = self.side_text[i]
            glColor3f(*clr)
            for j in range(4):
                glNormal3f(*side[j])
                glTexCoord2f(*text[j])
                glVertex3f(*side[j])
        glEnd()


    def make(self):

        hl = self.h / 2
        if len(self.side_vertecies):
            self.side_vertecies.clear()
            self.inner_vertecies.clear()
            self.color.clear()
            self.color_vbo.clear()
            self.side_text.clear()
            self.inner_text.clear()

        # make side
        self.side_vertecies = [[] for _ in range(self.slices + 1)]
        self.side_text = [[] for _ in range(self.slices + 1)]
        step = 1 / self.slices
        prev = 0
        for i in range(self.slices + 1):
            theta = i * 2. * pi / self.slices
            next_theta = (i + 1) * 2. * pi / self.slices
            v1 = [self.a * cos(theta), -hl, self.b * sin(theta)]
            v2 = [self.a * cos(theta), hl, self.b * sin(theta)]
            v3 = [self.a * cos(next_theta), -hl, self.b * sin(next_theta)]
            v4 = [self.a * cos(next_theta), hl, self.b * sin(next_theta)]
            clr = [(cos(theta) + 1) / 2., (sin(theta) + 0.7) / 2., cos(theta) * sin(theta)]
            self.color.append(clr)
            self.color_vbo.extend(4 * clr)
            self.side_vertecies[i].extend([v1, v2, v3, v4])
            self.side_text[i].extend([[prev, 0], [prev, 1], [prev + step, 0], [prev + step, 1]])
            prev += step

        # make inner
        dh = 0
        self.inner_vertecies = [[] for _ in range(self.h_slices + 1)]
        self.inner_text = [[] for _ in range(self.h_slices + 1)]
        for j in range(self.h_slices + 1):
            v = [0.0, dh - hl, 0.0]
            self.inner_vertecies[j].append(v)
            self.inner_text[j].append([0.5, 0.5])
            for i in range(self.slices + 1):
                theta = i * 2. * pi / self.slices
                v1 = [self.a * cos(theta), dh - hl, self.b * sin(theta)]
                x = (cos(theta) + 1)/2
                y = (sin(theta) + 1)/2
                self.inner_text[j].append([y, x])
                self.inner_vertecies[j].append(v1)
            dh += self.h / self.h_slices
        # change clockwise of top
        self.inner_vertecies[self.h_slices][1:] = self.inner_vertecies[self.h_slices][:0:-1]
        self.inner_text[self.h_slices][1:] = self.inner_text[self.h_slices][:0:-1]

    def move(self):
        if self.translation['x'] > 3 or self.translation['x'] < -2:
            self.dx *= -1

        self.translation['x'] += self.dx
        glTranslatef(self.translation['x'], 0, 0)


class Window(pyglet.window.Window):
    cyc = Cylinder()
    cube = Cube()
    start_time = time.time()
    counter = 0
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        glClearColor(-6, -2, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glDisable(GL_NORMALIZE)
        self.cyc.make()
        load_texture()
        self.scene = {
            'l_pos_0': '(GLfloat * 4)(0, 0, 6, 1)',
            'l_dif_0': '(GLfloat * 3)(1, 1, 0)',

            'l_pos_1': '(GLfloat * 4)(1, 1, 6, 1)',
            'l_dif_1': '(GLfloat * 3)(0, 1, 1)',

            'l_pos_2': '(GLfloat * 4)(-1, -1, 6, 1)',
            'l_dif_2': '(GLfloat * 3)(1, 1, 1)',
            'texture_on': 0,
            'light_on': 0
        }

    def on_draw(self):
        self.clear()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        if self.scene['light_on']:
            self.turn_on_light()
        if self.scene['texture_on']:
            self.turn_on_texture()

        self.cube.display()
        self.cyc.display()

        # pyglet.clock.tick()
        # self.cyc.speed = 20
        # self.cyc.re_draw = 1
        # print(pyglet.clock.get_fps())


    def on_resize(self, width, height):
        glViewport(0, 0, min(width, height), min(width, height))

    def on_text_motion(self, s):
        if s == key.UP:
            self.cyc.rotation['x'] -= self.cyc.speed
        elif s == key.DOWN:
            self.cyc.rotation['x'] += self.cyc.speed
        elif s == key.LEFT:
            self.cyc.rotation['y'] -= self.cyc.speed
        elif s == key.RIGHT:
            self.cyc.rotation['y'] += self.cyc.speed

    def on_key_press(self, s, modifiers):
        global mode
        if s == key.SPACE:
            if self.cyc.mode == GL_LINE:
                self.cyc.mode = GL_FILL
            else:
                self.cyc.mode = GL_LINE
            self.cyc.re_draw = 1
        elif s == key.W:
            self.cyc.translation['y'] += self.cyc.speed
        elif s == key.S:
            self.cyc.translation['y'] -= self.cyc.speed
        elif s == key.A:
            self.cyc.translation['x'] -= self.cyc.speed
        elif s == key.D:
            self.cyc.translation['x'] += self.cyc.speed
        elif s == key.F:
            self.cyc.translation['z'] -= self.cyc.speed/2
        elif s == key.N:
            self.cyc.translation['z'] += self.cyc.speed/2
        elif s == key.U:
            self.cyc.rotation['z'] -= self.cyc.speed
        elif s == key.J:
            self.cyc.rotation['z'] += self.cyc.speed

        elif s == key.X:
            self.cyc.scale *= 1.1
            self.cyc.re_draw = 1
        elif s == key.C:
            self.cyc.scale /= 1.1
            self.cyc.re_draw = 1
        elif s == key.L and self.cyc.slices > 5:
            self.cyc.slices -= 5
            self.cyc.re_draw = 1
        elif s == key.K and self.cyc.slices < 1000:
            self.cyc.slices += 5
            self.cyc.re_draw = 1
        elif s == key._1:
            self.cyc.a += 0.1
            self.cyc.re_draw = 1
        elif s == key._2 and self.cyc.a > 0.3:
            self.cyc.a -= 0.1
            self.cyc.re_draw = 1
        elif s == key._3:
            self.cyc.b += 0.1
            self.cyc.re_draw = 1
        elif s == key._4 and self.cyc.b > 0.3:
            self.cyc.b -= 0.1
            self.cyc.re_draw = 1
        elif s == key.I and self.cyc.h_slices < 100:
            self.cyc.h_slices += 1
            self.cyc.re_draw = 1
        elif s == key.O and self.cyc.h_slices > 2:
            self.cyc.h_slices -= 1
            self.cyc.re_draw = 1
        elif s == key._5:
            if self.scene['light_on']:
                self.turn_off_light()
            else:
                self.turn_on_light()
        elif s == key._6:
            if self.scene['texture_on']:
                self.turn_off_texture()
            else:
                self.turn_on_texture()
        elif s == key.T:
            self.animate()
        elif s == key._7:
            self.save_config()
        elif s == key._8:
            self.load_config()

    def turn_on_light(self):
        self.scene['light_on'] = 1
        self.cyc.light_on = 1
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_LIGHTING)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_COLOR_MATERIAL)
        glTranslatef(1, -1, 4)


        light_diffuse_0 = eval(self.scene['l_dif_0'])
        light_position_0 = eval(self.scene['l_pos_0'])

        glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)

        glEnable(GL_LIGHT0)
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 10)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse_0)
        glLightfv(GL_LIGHT0, GL_POSITION, light_position_0)

        light_diffuse_1 = eval(self.scene['l_dif_1'])
        light_position_1 = eval(self.scene['l_pos_1'])

        glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)

        glEnable(GL_LIGHT1)
        glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 10)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse_1)
        glLightfv(GL_LIGHT1, GL_POSITION, light_position_1)

        light_diffuse_2 = eval(self.scene['l_dif_2'])
        light_position_2 = eval(self.scene['l_pos_2'])

        glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)

        glEnable(GL_LIGHT2)
        glLightf(GL_LIGHT2, GL_SPOT_CUTOFF, 10)
        glLightfv(GL_LIGHT2, GL_DIFFUSE, light_diffuse_2)
        glLightfv(GL_LIGHT2, GL_POSITION, light_position_2)

    def turn_off_light(self):
        self.scene['light_on'] = 0
        self.cyc.light_on = 0
        glDisable(GL_LIGHTING)
        glDisable(GL_NORMALIZE)
        glDisable(GL_COLOR_MATERIAL)

    def turn_off_texture(self):
        self.scene['texture_on'] = 0
        self.cyc.texture_on = 0
        glDisable(GL_TEXTURE_2D)

    def turn_on_texture(self):
        self.scene['texture_on'] = 1
        self.cyc.texture_on = 1
        glEnable(GL_TEXTURE_2D)

    def animate(self):
        for _ in range(110):
            time.sleep(0.03)
            self.cyc.move()
            self.on_draw()
            self.flip()

    def save_config(self):
        names = ['speed', 'scale', 'slices', 'h_slices', 'h', 'a', 'b', 'dx', 'mode']
        with open('cyc_config.json', 'w') as f:
            f.write(json.dumps(dict(zip(names, [self.cyc.__dict__[name] for name in names]))))
        with open('scene_config.json', 'w') as f:
            f.write(json.dumps(self.scene.copy()))

    def load_config(self):
        names = ['speed', 'scale', 'slices', 'h_slices', 'h', 'a', 'b', 'dx', 'mode']
        with open('cyc_config.json', 'r') as f:
            data = json.load(f)
            for n in names:
                self.cyc.__setattr__(n, data[n])
        with open('scene_config.json', 'r', encoding='utf-8') as f:
            self.scene = json.load(f).copy()
        self.on_draw()
        self.cyc.re_draw = 1

def load_texture():
    data = pyglet.image.load("texture.png").get_data()
    texture_ids = (pyglet.gl.GLuint * 1)()
    glGenTextures(1, texture_ids)
    texture_id = texture_ids[0]
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1024, 1024, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)


if __name__ == '__main__':
    window = Window(720, 720, 'lab7', resizable=True)
    pyglet.app.run()
