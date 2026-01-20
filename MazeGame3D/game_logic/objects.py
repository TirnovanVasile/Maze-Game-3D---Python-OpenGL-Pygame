import random
import glm
from OpenGL.GL import *
from render.primitives import draw_textured_cube


class ParticleSystem:
    def __init__(self, pos, color, count=20):
        self.particles = []
        for _ in range(count):
            self.particles.append({
                "pos": glm.vec3(pos),
                "vel": glm.vec3(
                    random.uniform(-0.1, 0.1),
                    random.uniform(0.1, 0.3),
                    random.uniform(-0.1, 0.1)
                ),
                "life": random.uniform(0.5, 1.5),
                "color": color
            })

    def update(self, dt):
        for p in self.particles[:]:
            p["pos"] += p["vel"] * dt * 0.1
            p["vel"].y -= 0.01
            p["life"] -= dt * 0.01
            if p["life"] <= 0:
                self.particles.remove(p)

    def draw(self):
        glDisable(GL_LIGHTING)
        glPointSize(5)
        glBegin(GL_POINTS)
        for p in self.particles:
            a = max(0, p["life"])
            glColor4f(p["color"][0], p["color"][1], p["color"][2], a)
            glVertex3f(p["pos"].x, p["pos"].y, p["pos"].z)
        glEnd()
        glEnable(GL_LIGHTING)


class InteractiveObject:
    def __init__(self, pos):
        self.pos = glm.vec3(pos)
        self.target_open = False
        self.animation_progress = 0.0
        self.is_open = False
        self.orientation = "z"

    def update(self):
        speed = 0.03
        if self.target_open and self.animation_progress < 1.0:
            self.animation_progress = min(1.0, self.animation_progress + speed)
        elif (not self.target_open) and self.animation_progress > 0.0:
            self.animation_progress = max(0.0, self.animation_progress - speed)
        self.is_open = (self.animation_progress >= 0.95)

    def draw(self, game):
        glPushMatrix()
        glTranslatef(self.pos.x, self.pos.y, self.pos.z)

        door_h = 3.0
        door_t = 0.35
        from config import CELL_SIZE
        door_w = CELL_SIZE

        lift = self.animation_progress * 3.2
        glTranslatef(0, lift, 0)

        if self.orientation == "x":
            glRotatef(90, 0, 1, 0)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, game.tex_door)
        glColor3f(1, 1, 1)

        draw_textured_cube(door_w, door_h, door_t, game.tex_door, rep_u=1.0, rep_v=1.0)

        glBindTexture(GL_TEXTURE_2D, 0)
        glPopMatrix()
