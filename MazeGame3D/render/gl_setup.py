from OpenGL.GL import *
from config import MAZE_SIZE


def setup_gl():
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_FOG)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glFogfv(GL_FOG_COLOR, (0.05, 0.05, 0.1, 1))
    glFogi(GL_FOG_MODE, GL_EXP2)
    glFogf(GL_FOG_DENSITY, 0.03)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.2, 0.2, 0.25, 1.0))

    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 0.9, 0.7, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))

    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.1, 0.1, 0.15, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.3, 0.3, 0.4, 1.0))
    glLightfv(GL_LIGHT1, GL_POSITION, (MAZE_SIZE * 2, 10, MAZE_SIZE * 2, 1.0))
