from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse
from math import *
import numpy as np


N = 3
width = 500
height = 500
delete_last_point = False
points = []
filt = False

purple = np.array([120 / 255, 66 / 255, 245 / 255])
buff = np.zeros(shape=(width, height, 3), dtype=np.float32)


class Edge:
    def __init__(self, p1, p2):
        if p1.y > p2.y:
            p1, p2 = p2, p1
        self.p1 = p1
        self.p2 = p2
        if p2.y != p1.y:
            self.delta = (p2.x - p1.x) / (p2.y - p1.y)


class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)


def postfiltration():
    global buff, filt
    intensity_mask = [
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1],
    ]
    w_sum = 0
    for row in intensity_mask:
        w_sum += sum(row)
    b_shape = buff.shape
    for i in range(1, b_shape[0] - 1):
        for j in range(1, b_shape[1] - 1):
            for k in range(3):
                buff[i][j][k] = (intensity_mask * buff[i - 1:i + 2, j - 1:j + 2, k]).sum() / w_sum

    filt = True


def rasterize():
    global points, buff,height, purple
    if len(points) < 3:
        return
    cap = []  # список активных ребер
    edges = []
    for i in range(len(points) - 1):
        edges.append(Edge(points[i], points[i + 1]))
    edges.append(Edge(points[0], points[-1]))
    for e in edges:
        if e.p1.y == e.p2.y:
            edges.remove(e)

    edges.sort(key=lambda e: e.p1.y)
    ys = [e.p1.y for e in edges]
    couples = []
    for line in range(round(ys[0]) - 1, height - 1):
        if line in ys:
            cap.extend(e for e in edges if e.p1.y == line)
            couples.extend([e.p1.x - e.delta, e.delta] for e in edges if e.p1.y == line)
        for e in cap:
            if e.p2.y < line:
                cap.remove(e)
                for c in couples:
                    if c[1] == e.delta:
                        couples.remove(c)

        for c in couples:
            c[0] += c[1]
        if len(couples) < 2:
            continue
        ints = [c[0] for c in couples]
        l_x = int(floor(min(ints)))
        r_x = int(ceil(max(ints)))
        for i in range(l_x, r_x):
            buff[i][line] = purple



class MyWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == mouse.LEFT:
            points.append(Point(x, y))

    def on_key_press(self, s, modifiers):
        global points, buff, filt
        if s == key.F:
            rasterize()
        elif s == key.C:
            buff = np.zeros(shape=(self.width, self.height, 3), dtype=np.float32)
            points.clear()
            window.clear()
            window.flip()
            filt = False
        elif s == key.SPACE:
            postfiltration()

    def on_draw(self):
        global buff, filt, purple
        self.clear()
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.width, 0, self.height, 0, 1)

        glMatrixMode(GL_MODELVIEW)
        glDrawPixels(self.width, self.height, GL_RGB, GL_FLOAT,
                     buff.swapaxes(0, 2).swapaxes(1, 2).flatten('F').ctypes)

        # shape 3 width height
        if not filt:
            if len(points) == 1:
                glBegin(GL_POINTS)
                glVertex2f(float(points[0].x), float(points[0].y))
                glEnd()
            elif len(points) > 1:
                glBegin(GL_LINE_STRIP)
                glColor3f(purple[0], purple[1], purple[2])
                for p in points:
                    glVertex2f(p.x, p.y)
                glVertex2f(points[0].x, points[0].y)
                glEnd()


    def on_resize(self, w, h):
        global buff, width, height, points
        w_c = w / width
        h_c = h / height
        for i in range(len(points)):
            points[i] = Point(points[i].x * w_c, points[i].y * h_c)

        width, height = w, h
        buff = np.zeros(shape=(width, height, 3), dtype=np.float32)
        rasterize()
        glViewport(0, 0, width, height)


if __name__ == '__main__':
    window = MyWindow(width, height, 'lab3', resizable=True)
    window.set_minimum_size(300, 300)
    pyglet.app.run()
