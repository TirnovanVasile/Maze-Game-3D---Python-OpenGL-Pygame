import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
import glm

from config import SENSITIVITY, SPEED, JUMP_FORCE, GRAVITY, PLAYER_HEIGHT
from render.gl_setup import setup_gl
from render.world import draw_world
from ui.hud import draw_hud
from ui.menu import draw_menu, draw_win_screen
from game_logic.game import MazeGame
from game_logic.objects import ParticleSystem

def main():
    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Maze Game 3D")

    ui_surface = pygame.Surface(display, pygame.SRCALPHA)

    setup_gl()
    game = MazeGame()
    clock = pygame.time.Clock()

    while game.running:
        clock.tick(60)
        game.timer += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                game.running = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    if game.game_state == "MENU":
                        game.running = False
                    else:
                        game.game_state = "MENU"

                if event.key == K_SPACE:
                    if game.game_state == "MENU":
                        game.game_state = "PLAY"
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)
                    elif game.game_state == "WON":
                        game = MazeGame()
                        game.game_state = "PLAY"
                        pygame.mouse.set_visible(False)
                        pygame.event.set_grab(True)

                if game.game_state == "PLAY":
                    if event.key == K_e and game.nearest_interactive:
                        itype, obj = game.nearest_interactive

                        if itype == "key":
                            obj["collected"] = True
                            game.keys_collected += 1
                            game.particle_systems.append(ParticleSystem(obj["pos"], (1, 1, 0)))

                        elif itype == "door_key":
                            if not obj.get("taken", False) and not obj.get("collecting", False):
                                obj["collecting"] = True
                                obj["taken"] = True
                                game.door_keys_collected += 1
                                game.particle_systems.append(ParticleSystem(obj["pos"], (0.8, 0.8, 0.9)))

                        elif itype == "door":
                            ok = game.try_open_door(obj)
                            game.particle_systems.append(ParticleSystem(obj.pos, (1, 1, 1) if ok else (1, 0, 0)))

                        elif itype == "exit":
                            game.game_state = "WON"
                            pygame.mouse.set_visible(True)
                            pygame.event.set_grab(False)

                    if event.key == K_SPACE and game.on_ground:
                        game.velocity_y = JUMP_FORCE
                        game.on_ground = False

        if game.game_state == "PLAY":
            dx, dy = pygame.mouse.get_rel()
            game.yaw += dx * SENSITIVITY
            game.pitch = max(-80, min(80, game.pitch - dy * SENSITIVITY))

            keys = pygame.key.get_pressed()
            move_vec = glm.vec3(0)
            front = glm.vec3(math.cos(glm.radians(game.yaw)), 0, math.sin(glm.radians(game.yaw)))
            right = glm.normalize(glm.cross(front, glm.vec3(0, 1, 0)))

            if keys[K_w]:
                move_vec += front
            if keys[K_s]:
                move_vec -= front
            if keys[K_a]:
                move_vec -= right
            if keys[K_d]:
                move_vec += right

            if glm.length(move_vec) > 0:
                next_pos = game.pos + glm.normalize(move_vec) * SPEED
                game.pos = game.check_collision(next_pos)

            game.velocity_y -= GRAVITY
            next_y = game.pos.y + game.velocity_y
            if next_y <= PLAYER_HEIGHT:
                next_y = PLAYER_HEIGHT
                game.velocity_y = 0
                game.on_ground = True
            else:
                game.on_ground = False
            game.pos.y = next_y

            game.check_interactions()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.05, 0.05, 0.1, 1)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65, display[0] / display[1], 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        if game.game_state == "PLAY":
            look_dir = glm.vec3(
                math.cos(glm.radians(game.yaw)) * math.cos(glm.radians(game.pitch)),
                math.sin(glm.radians(game.pitch)),
                math.sin(glm.radians(game.yaw)) * math.cos(glm.radians(game.pitch))
            )
            gluLookAt(
                game.pos.x, game.pos.y, game.pos.z,
                game.pos.x + look_dir.x, game.pos.y + look_dir.y, game.pos.z + look_dir.z,
                0, 1, 0
            )

            flicker = random.uniform(0.85, 1.0)
            glLightfv(GL_LIGHT0, GL_POSITION, (game.pos.x, game.pos.y, game.pos.z, 1.0))
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0 * flicker, 0.9 * flicker, 0.7 * flicker, 1.0))

            draw_world(game)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, display[0], display[1], 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_FOG)

        ui_surface.fill((0, 0, 0, 0))

        if game.game_state == "MENU":
            pygame.mouse.set_visible(True)
            pygame.event.set_grab(False)
            draw_menu(ui_surface)
        elif game.game_state == "WON":
            draw_win_screen(ui_surface)
        else:
            draw_hud(ui_surface, game)

        texture_data = pygame.image.tostring(ui_surface, "RGBA", True)
        glWindowPos2d(0, 0)
        glDrawPixels(display[0], display[1], GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_FOG)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
