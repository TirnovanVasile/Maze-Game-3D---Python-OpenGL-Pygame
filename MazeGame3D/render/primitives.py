import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


def load_texture(path, repeat=True):
    surf = pygame.image.load(path).convert_alpha()
    surf = pygame.transform.flip(surf, False, True)
    img_data = pygame.image.tostring(surf, "RGBA", True)
    w, h = surf.get_size()

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    wrap = GL_REPEAT if repeat else GL_CLAMP_TO_EDGE
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glGenerateMipmap(GL_TEXTURE_2D)

    glBindTexture(GL_TEXTURE_2D, 0)
    return tex_id


def draw_textured_cube(sx, sy, sz, tex_id, rep_u=1.0, rep_v=1.0):
    x, y, z = sx / 2, sy / 2, sz / 2
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glColor3f(1, 1, 1)

    glBegin(GL_QUADS)

    glNormal3f(0, 0, 1)
    glTexCoord2f(0, 0);         glVertex3f(-x, -y,  z)
    glTexCoord2f(rep_u, 0);     glVertex3f( x, -y,  z)
    glTexCoord2f(rep_u, rep_v); glVertex3f( x,  y,  z)
    glTexCoord2f(0, rep_v);     glVertex3f(-x,  y,  z)

    glNormal3f(0, 0, -1)
    glTexCoord2f(0, 0);         glVertex3f( x, -y, -z)
    glTexCoord2f(rep_u, 0);     glVertex3f(-x, -y, -z)
    glTexCoord2f(rep_u, rep_v); glVertex3f(-x,  y, -z)
    glTexCoord2f(0, rep_v);     glVertex3f( x,  y, -z)

    glNormal3f(-1, 0, 0)
    glTexCoord2f(0, 0);         glVertex3f(-x, -y, -z)
    glTexCoord2f(rep_u, 0);     glVertex3f(-x, -y,  z)
    glTexCoord2f(rep_u, rep_v); glVertex3f(-x,  y,  z)
    glTexCoord2f(0, rep_v);     glVertex3f(-x,  y, -z)

    glNormal3f(1, 0, 0)
    glTexCoord2f(0, 0);         glVertex3f( x, -y,  z)
    glTexCoord2f(rep_u, 0);     glVertex3f( x, -y, -z)
    glTexCoord2f(rep_u, rep_v); glVertex3f( x,  y, -z)
    glTexCoord2f(0, rep_v);     glVertex3f( x,  y,  z)

    glNormal3f(0, 1, 0)
    glTexCoord2f(0, 0);         glVertex3f(-x,  y,  z)
    glTexCoord2f(rep_u, 0);     glVertex3f( x,  y,  z)
    glTexCoord2f(rep_u, rep_v); glVertex3f( x,  y, -z)
    glTexCoord2f(0, rep_v);     glVertex3f(-x,  y, -z)

    glNormal3f(0, -1, 0)
    glTexCoord2f(0, 0);         glVertex3f(-x, -y, -z)
    glTexCoord2f(rep_u, 0);     glVertex3f( x, -y, -z)
    glTexCoord2f(rep_u, rep_v); glVertex3f( x, -y,  z)
    glTexCoord2f(0, rep_v);     glVertex3f(-x, -y,  z)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)


def draw_sphere(radius, slices=16, stacks=16):
    q = gluNewQuadric()
    gluQuadricNormals(q, GLU_SMOOTH)
    gluSphere(q, radius, slices, stacks)
    gluDeleteQuadric(q)
