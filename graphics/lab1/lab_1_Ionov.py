import pyglet
from pyglet.window import key
from OpenGL.GL import *

window = pyglet.window.Window(720, 720, "lab1", resizable=False)
glColor3f(0.75, 0.14, 0.94)


def drawSquare():
    window.clear()
    glBegin(GL_QUADS)
    glVertex2f(200, 200)
    glVertex2f(400, 200)
    glVertex2f(400, 400)
    glVertex2f(200, 400)
    glEnd()


def drawTriangle():
    window.clear()
    glBegin(GL_TRIANGLES)
    glVertex2f(200, 200)
    glVertex2f(600, 200)
    glVertex2f(400, 400)
    glEnd()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.S:
        drawSquare()
    elif symbol == key.T:
        drawTriangle()
    else:
        window.clear()


pyglet.app.run()
