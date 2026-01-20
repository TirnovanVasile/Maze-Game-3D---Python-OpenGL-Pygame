import random
import math
from OpenGL.GL import *
from OpenGL.GLU import *

from config import MAZE_SIZE, CELL_SIZE, WALL_HEIGHT, LOG_RADIUS, LOG_LENGTH
from render.primitives import draw_textured_cube, draw_sphere


def draw_skybox(game):
    glDisable(GL_LIGHTING)
    glDisable(GL_FOG)

    glPushMatrix()
    glTranslatef(game.pos.x, game.pos.y, game.pos.z)

    size = 100
    glBegin(GL_QUADS)
    glColor3f(0.05, 0.05, 0.15)
    glVertex3f(-size, size, -size)
    glVertex3f(size, size, -size)
    glVertex3f(size, size, size)
    glVertex3f(-size, size, size)
    glEnd()

    glBegin(GL_QUADS)
    for i in range(4):
        a = i * 90
        x1 = size * math.cos(math.radians(a))
        z1 = size * math.sin(math.radians(a))
        x2 = size * math.cos(math.radians(a + 90))
        z2 = size * math.sin(math.radians(a + 90))

        glColor3f(0.02, 0.02, 0.08)
        glVertex3f(x1, -size, z1)
        glVertex3f(x2, -size, z2)

        glColor3f(0.05, 0.05, 0.15)
        glVertex3f(x2, size, z2)
        glVertex3f(x1, size, z1)
    glEnd()

    glPointSize(2)
    glBegin(GL_POINTS)
    random.seed(42)
    for _ in range(100):
        glColor3f(1, 1, random.uniform(0.8, 1))
        glVertex3f(random.uniform(-size, size), random.uniform(0, size), random.uniform(-size, size))
    glEnd()

    glPopMatrix()
    glEnable(GL_FOG)
    glEnable(GL_LIGHTING)


def draw_world(game):
    draw_skybox(game)

    glDisable(GL_LIGHTING)
    glBindTexture(GL_TEXTURE_2D, game.tex_floor)
    glColor3f(1, 1, 1)

    tile = 2.5
    glBegin(GL_QUADS)
    for z in range(MAZE_SIZE):
        for x in range(MAZE_SIZE):
            x1, z1 = x * CELL_SIZE, z * CELL_SIZE
            x2, z2 = (x + 1) * CELL_SIZE, (z + 1) * CELL_SIZE

            glTexCoord2f(x * tile, z * tile);                 glVertex3f(x1, 0, z1)
            glTexCoord2f((x + 1) * tile, z * tile);           glVertex3f(x2, 0, z1)
            glTexCoord2f((x + 1) * tile, (z + 1) * tile);     glVertex3f(x2, 0, z2)
            glTexCoord2f(x * tile, (z + 1) * tile);           glVertex3f(x1, 0, z2)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)
    glEnable(GL_LIGHTING)

    for z in range(MAZE_SIZE):
        for x in range(MAZE_SIZE):
            if game.maze[z][x] == 1:
                glPushMatrix()
                glTranslatef(x * CELL_SIZE + 2, WALL_HEIGHT / 2, z * CELL_SIZE + 2)

                glMaterialfv(GL_FRONT, GL_AMBIENT, (0.2, 0.2, 0.25, 1.0))
                glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.8, 0.8, 0.85, 1.0))
                glMaterialfv(GL_FRONT, GL_SPECULAR, (0.05, 0.05, 0.05, 1.0))
                glMaterialf(GL_FRONT, GL_SHININESS, 8)

                draw_textured_cube(CELL_SIZE, WALL_HEIGHT, CELL_SIZE, game.tex_wall, 1.0, WALL_HEIGHT / 1.5)
                glPopMatrix()

    for d in game.doors:
        d["obj"].update()
        d["obj"].draw(game)

    for l in game.logs:
        glPushMatrix()
        glTranslatef(l["pos"].x, l["pos"].y, l["pos"].z)
        if l["orientation"] != "x":
            glRotatef(90, 0, 1, 0)

        glBindTexture(GL_TEXTURE_2D, game.tex_log)
        glColor3f(1, 1, 1)

        glMaterialfv(GL_FRONT, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.9, 0.9, 0.9, 1.0))
        glMaterialfv(GL_FRONT, GL_SPECULAR, (0.15, 0.15, 0.15, 1.0))
        glMaterialf(GL_FRONT, GL_SHININESS, 16)

        radius = LOG_RADIUS
        length = LOG_LENGTH

        q = gluNewQuadric()
        gluQuadricNormals(q, GLU_SMOOTH)
        gluQuadricTexture(q, GL_TRUE)

        glMatrixMode(GL_TEXTURE)
        glPushMatrix()
        glLoadIdentity()
        glScalef(2.5, 1.0 + length * 0.6, 1.0)
        glMatrixMode(GL_MODELVIEW)

        glTranslatef(0, 0.02, -length / 2.0)
        gluCylinder(q, radius, radius, length, 18, 1)
        gluDisk(q, 0.0, radius, 18, 1)
        glTranslatef(0, 0, length)
        gluDisk(q, 0.0, radius, 18, 1)

        glMatrixMode(GL_TEXTURE)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        gluDeleteQuadric(q)
        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()

    for k in game.door_key_objects:
        if k["collecting"] and k["scale"] > 0.02:
            k["scale"] *= 0.88
        if k["collecting"] and k["scale"] <= 0.02:
            k["scale"] = 0.0
        if k["scale"] <= 0.0:
            continue

        glPushMatrix()
        glTranslatef(k["pos"].x, k["pos"].y, k["pos"].z)
        glRotatef(game.timer * 2 + k["rotation"], 0, 1, 0)
        glScalef(k["scale"], k["scale"], k["scale"])

        glMaterialfv(GL_FRONT, GL_AMBIENT, (0.25, 0.25, 0.28, 1.0))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (0.85, 0.85, 0.9, 1.0))
        glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
        glMaterialf(GL_FRONT, GL_SHININESS, 90)

        glColor3f(0.9, 0.9, 0.95)
        s = 0.45 / 2
        glBegin(GL_QUADS)
        glVertex3f(-s, -s,  s); glVertex3f(s, -s,  s); glVertex3f(s, s,  s); glVertex3f(-s, s,  s)
        glVertex3f( s, -s, -s); glVertex3f(-s, -s, -s); glVertex3f(-s, s, -s); glVertex3f( s, s, -s)
        glVertex3f(-s, -s, -s); glVertex3f(-s, -s,  s); glVertex3f(-s, s,  s); glVertex3f(-s, s, -s)
        glVertex3f( s, -s,  s); glVertex3f( s, -s, -s); glVertex3f( s, s, -s); glVertex3f( s, s,  s)
        glVertex3f(-s, s,  s); glVertex3f( s, s,  s); glVertex3f( s, s, -s); glVertex3f(-s, s, -s)
        glVertex3f(-s, -s, -s); glVertex3f( s, -s, -s); glVertex3f( s, -s,  s); glVertex3f(-s, -s,  s)
        glEnd()
        glPopMatrix()

    for key in game.key_objects:
        if key["collected"]:
            continue

        glPushMatrix()
        offset = math.sin(game.timer * 0.1) * 0.3
        glTranslatef(key["pos"].x, key["pos"].y + offset, key["pos"].z)
        glRotatef(game.timer * 3, 0, 1, 0)

        glDisable(GL_LIGHTING)
        glColor4f(1, 0.9, 0, 0.3)
        draw_sphere(0.8)
        glEnable(GL_LIGHTING)

        glMaterialfv(GL_FRONT, GL_AMBIENT, (0.8, 0.7, 0, 1.0))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, (1, 0.9, 0.2, 1.0))
        glMaterialfv(GL_FRONT, GL_SPECULAR, (1, 1, 0.5, 1.0))
        glMaterialf(GL_FRONT, GL_SHININESS, 100)

        glColor3f(1, 0.8, 0)
        s = 0.25
        glBegin(GL_QUADS)
        glVertex3f(-s, -s,  s); glVertex3f(s, -s,  s); glVertex3f(s, s,  s); glVertex3f(-s, s,  s)
        glVertex3f( s, -s, -s); glVertex3f(-s, -s, -s); glVertex3f(-s, s, -s); glVertex3f( s, s, -s)
        glVertex3f(-s, -s, -s); glVertex3f(-s, -s,  s); glVertex3f(-s, s,  s); glVertex3f(-s, s, -s)
        glVertex3f( s, -s,  s); glVertex3f( s, -s, -s); glVertex3f( s, s, -s); glVertex3f( s, s,  s)
        glVertex3f(-s, s,  s); glVertex3f( s, s,  s); glVertex3f( s, s, -s); glVertex3f(-s, s, -s)
        glVertex3f(-s, -s, -s); glVertex3f( s, -s, -s); glVertex3f( s, -s,  s); glVertex3f(-s, -s,  s)
        glEnd()

        glPopMatrix()

    glPushMatrix()
    glTranslatef(game.exit_pos.x, 1.5, game.exit_pos.z)

    color = (0, 1, 0) if game.keys_collected >= game.keys_total else (1, 0, 0)

    glPushAttrib(GL_ENABLE_BIT | GL_CURRENT_BIT | GL_LIGHTING_BIT | GL_DEPTH_BUFFER_BIT)
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)

    glColor4f(color[0], color[1], color[2], 0.18)
    draw_sphere(2.2, 24, 24)
    glColor4f(color[0], color[1], color[2], 0.28)
    draw_sphere(1.7, 24, 24)

    glDepthMask(GL_TRUE)
    glEnable(GL_LIGHTING)

    glRotatef(game.timer * 0.7, 0, 1, 0)
    glMaterialfv(GL_FRONT, GL_EMISSION, (color[0] * 0.6, color[1] * 0.6, color[2] * 0.6, 1.0))
    glColor3f(color[0], color[1], color[2])
    draw_sphere(1.3, 32, 32)
    glMaterialfv(GL_FRONT, GL_EMISSION, (0, 0, 0, 1.0))

    glPopAttrib()
    glPopMatrix()

    for ps in game.particle_systems[:]:
        ps.update(1)
        ps.draw()
        if len(ps.particles) == 0:
            game.particle_systems.remove(ps)
