from pyglet.gl import *
from pyglet.window import key
from math import *
import numpy as np
import time
import json

import time
from pyglet import clock

# 23 вариант

fps_display = pyglet.clock.Clock()


class Cube():
    center_pos_x = 0
    center_pos_y = 0
    center_pos_z = 0
    half_side_length = 0.3 * 0.5

    tex_vs = [
        [0, 0],
        [0, 1],
        [1, 1],
        [1, 0]
    ]

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

    vertecies = [
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
        self.draw()


class Cylinder():
    side_vertecies = []
    inner_vertecies = []
    text_coords = []
    inner_text = []
    color = []
    rotation = {
        'x': 0,
        'y': 0,
        'z': 0,
    }
    translation = {
        'x': 1,
        'y': -1,
        'z': -4,
    }

    re_draw = True

    def __init__(self):
        self.speed = 2
        self.scale = 1.2
        self.slices = 10
        self.h_slices = 2
        self.h = 3
        self.a = 1
        self.b = 1
        self.dx = 0.3
        self.mode = GL_FILL
        self.make()

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
        self.draw()
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
            glNormal3f(*c)
            glVertex3f(*c)
            glTexCoord2f(*self.inner_tex[j][0])
            for i in range(1, len(self.inner_vertecies[j])):
                v = self.inner_vertecies[j][i]
                tex = self.inner_tex[j][i]
                glNormal3f(*v)
                glVertex3f(*v)
                glTexCoord2f(*tex)
            glEnd()

        self.inner_tex[self.h_slices][1:] = self.inner_tex[self.h_slices][:0:-1]
        self.inner_vertecies[self.h_slices][1:] = self.inner_vertecies[self.h_slices][:0:-1]


        # draw side
        glBegin(GL_QUAD_STRIP)
        for i in range(self.slices + 1):
            clr = self.color[i]
            side = self.side_vertecies[i]
            text = self.text_coords[i]
            glColor3f(*clr)
            for j in range(4):
                glNormal3f(*side[j])
                glTexCoord2f(*text[j])
                glVertex3f(*side[j])
        glEnd()


    def make(self):
        hl = self.h / 2
        self.side_vertecies.clear()
        self.inner_vertecies.clear()
        self.color.clear()

        # make inner
        dh = 0
        self.inner_vertecies = [[] for _ in range(self.h_slices + 1)]
        self.inner_tex = [[] for _ in range(self.h_slices + 1)]
        for j in range(self.h_slices + 1):
            c = [0.0, dh - hl, 0.0]
            self.inner_vertecies[j].append(c)
            self.inner_tex[j].append([0.5, 0.5])
            for i in range(self.slices + 1):
                theta = i * 2. * pi / self.slices
                v1 = [self.a * cos(theta), dh - hl, self.b * sin(theta)]
                x = (cos(theta) + 1)/2
                y = (sin(theta) + 1)/2
                self.inner_tex[j].append([x, y])
                self.inner_vertecies[j].append(v1)

            dh += self.h / self.h_slices

        # change clockwise of top
        self.inner_vertecies[self.h_slices][1:] = self.inner_vertecies[self.h_slices][:0:-1]

        # make side
        self.side_vertecies = [[] for i in range(self.slices + 1)]
        self.text_coords = [[] for _ in range(self.slices + 1)]

        self.color = []
        prev = 0
        step = 1 / self.slices
        for i in range(self.slices + 1):
            theta = i * 2. * pi / self.slices
            next_theta = (i + 1) * 2. * pi / self.slices
            self.color.append([(cos(theta) + 1) / 2., (sin(theta) + 0.7) / 2., cos(theta) * sin(theta)])
            self.side_vertecies[i].append([self.a * cos(theta), -hl, self.b * sin(theta)])
            self.side_vertecies[i].append([self.a * cos(theta), hl, self.b * sin(theta)])
            self.side_vertecies[i].append([self.a * cos(next_theta), -hl, self.b * sin(next_theta)])
            self.side_vertecies[i].append([self.a * cos(next_theta), hl, self.b * sin(next_theta)])
            self.text_coords[i].extend([[prev, 0], [prev, 1], [prev + step, 0], [prev + step, 1]])
            prev += step

    def move(self):
        if self.translation['x'] > 3 or self.translation['x'] < -2:
            self.dx *= -1

        self.translation['x'] += self.dx
        glTranslatef(self.translation['x'], 0, 0)


class Window(pyglet.window.Window):
    cyc = Cylinder()
    cube = Cube()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        glClearColor(-6, -2, 0, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        self.cyc.make()
        self.load_texture()
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

    def load_texture(self):
        data = pyglet.image.load("texture.png").get_data()
        texture_ids = (pyglet.gl.GLuint * 1)()
        glGenTextures(1, texture_ids)
        texture_id = texture_ids[0]
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1024, 1024, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)





def make_texture():
    glEnable(GL_TEXTURE_2D)
    data = pyglet.image.load("../lab7/texture.png").get_data()
    texture_ids = (pyglet.gl.GLuint * 1)()
    glGenTextures(1, texture_ids)
    texture_id = texture_ids[0]
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1024, 1024, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)


if __name__ == '__main__':
    window = Window(720, 720, 'lab6', resizable=True)
    pyglet.app.run()
