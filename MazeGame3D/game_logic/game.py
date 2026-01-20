import random
import glm

from config import (
    MAZE_SIZE, CELL_SIZE,
    PLAYER_HEIGHT,
    LOG_HEIGHT, LOG_LENGTH
)

from game_logic.maze import generate_maze
from game_logic.objects import InteractiveObject
from render.primitives import load_texture
from game_logic import collision


class MazeGame:
    def __init__(self):
        self.maze = generate_maze(MAZE_SIZE)

        self.tex_wall = load_texture("textures/wall.jpg", repeat=True)
        self.tex_floor = load_texture("textures/floor.jpg", repeat=True)
        self.tex_door = load_texture("textures/door.jpg", repeat=False)
        self.tex_log = load_texture("textures/log.jpg", repeat=True)

        self.pos = glm.vec3(CELL_SIZE + 2, PLAYER_HEIGHT, CELL_SIZE + 2)
        self.velocity_y = 0
        self.on_ground = True
        self.yaw = -90
        self.pitch = 0

        self.keys_total = 3
        self.keys_collected = 0
        self.key_objects = self.place_keys()

        self.door_keys_collected = 0
        self.door_key_objects = self.place_door_keys(count=23)

        self.exit_pos = glm.vec3((MAZE_SIZE - 2) * CELL_SIZE + 2, 0, (MAZE_SIZE - 2) * CELL_SIZE + 2)

        self.doors = self.place_doors(count=6)
        self.door_map = {(d["cell"][0], d["cell"][1]): d["obj"] for d in self.doors}

        self.logs = self.place_logs(count=10, min_cell_dist=3)

        self.particle_systems = []
        self.running = True
        self.game_state = "MENU"
        self.timer = 0

        self.show_interaction_hint = False
        self.nearest_interactive = None

    def place_keys(self):
        keys = []
        while len(keys) < self.keys_total:
            rx, rz = random.randint(1, MAZE_SIZE - 1), random.randint(1, MAZE_SIZE - 1)
            if self.maze[rz][rx] == 0 and (rx, rz) != (1, 1):
                keys.append({
                    "pos": glm.vec3(rx * CELL_SIZE + 2, 1, rz * CELL_SIZE + 2),
                    "collected": False,
                    "rotation": random.uniform(0, 360)
                })
        return keys

    def place_door_keys(self, count=18):
        keys = []
        used = set()
        blocked = {(1, 1), (MAZE_SIZE - 2, MAZE_SIZE - 2)}
        tries = 0

        while len(keys) < count and tries < 12000:
            tries += 1
            rx, rz = random.randint(1, MAZE_SIZE - 2), random.randint(1, MAZE_SIZE - 2)
            if self.maze[rz][rx] != 0:
                continue
            if (rx, rz) in blocked or (rx, rz) in used:
                continue

            used.add((rx, rz))
            keys.append({
                "pos": glm.vec3(rx * CELL_SIZE + 2, 1.0, rz * CELL_SIZE + 2),
                "taken": False,
                "collecting": False,
                "scale": 1.0,
                "rotation": random.uniform(0, 360)
            })
        return keys

    def place_doors(self, count=6, min_cell_dist=4):
        doors = []
        used = set()
        tries = 0

        while len(doors) < count and tries < 6000:
            tries += 1
            rx, rz = random.randint(2, MAZE_SIZE - 3), random.randint(2, MAZE_SIZE - 3)
            if self.maze[rz][rx] != 0:
                continue
            if (rx, rz) in used or (rx, rz) == (1, 1) or (rx, rz) == (MAZE_SIZE - 2, MAZE_SIZE - 2):
                continue

            too_close = False
            for (ux, uz) in used:
                if abs(rx - ux) + abs(rz - uz) < min_cell_dist:
                    too_close = True
                    break
            if too_close:
                continue

            left = self.maze[rz][rx - 1] == 0
            right = self.maze[rz][rx + 1] == 0
            up = self.maze[rz - 1][rx] == 0
            down = self.maze[rz + 1][rx] == 0

            corridor_x = left and right
            corridor_z = up and down
            if corridor_x == corridor_z:
                continue

            used.add((rx, rz))

            door = InteractiveObject((rx * CELL_SIZE + 2, 1.5, rz * CELL_SIZE + 2))
            door.orientation = "x" if corridor_x else "z"
            doors.append({"cell": (rx, rz), "obj": door})

        return doors

    def place_logs(self, count=10, min_cell_dist=3):
        logs = []
        used = set()
        blocked = {(1, 1), (MAZE_SIZE - 2, MAZE_SIZE - 2)}
        for d in getattr(self, "doors", []):
            blocked.add(d["cell"])

        tries = 0
        while len(logs) < count and tries < 12000:
            tries += 1
            rx, rz = random.randint(2, MAZE_SIZE - 3), random.randint(2, MAZE_SIZE - 3)
            if self.maze[rz][rx] != 0:
                continue
            if (rx, rz) in blocked or (rx, rz) in used:
                continue

            too_close = False
            for (ux, uz) in used:
                if abs(rx - ux) + abs(rz - uz) < min_cell_dist:
                    too_close = True
                    break
            if too_close:
                continue

            left = self.maze[rz][rx - 1] == 0
            right = self.maze[rz][rx + 1] == 0
            up = self.maze[rz - 1][rx] == 0
            down = self.maze[rz + 1][rx] == 0

            corridor_x = left and right
            corridor_z = up and down
            if corridor_x == corridor_z:
                continue

            used.add((rx, rz))
            from config import LOG_HEIGHT
            logs.append({
                "pos": glm.vec3(rx * CELL_SIZE + 2, LOG_HEIGHT / 2.0, rz * CELL_SIZE + 2),
                "orientation": "x" if corridor_x else "z"
            })

        return logs

    def try_open_door(self, door):
        is_closed = (door.animation_progress <= 0.05 and not door.target_open)
        if is_closed:
            if self.door_keys_collected <= 0:
                return False
            self.door_keys_collected -= 1
            door.target_open = True
            return True
        door.target_open = False
        return True

    def check_collision(self, next_pos):
        return collision.check_collision(self, next_pos)

    def check_interactions(self):
        collision.check_interactions(self)
