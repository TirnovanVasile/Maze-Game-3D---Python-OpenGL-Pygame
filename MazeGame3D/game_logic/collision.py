import glm
from config import (
    MAZE_SIZE, CELL_SIZE,
    PLAYER_HEIGHT, PLAYER_RADIUS,
    LOG_HEIGHT, LOG_LENGTH, LOG_RADIUS
)


def check_collision(game, next_pos):
    adjusted = glm.vec3(next_pos)

    for axis in ["x", "z"]:
        temp = glm.vec3(game.pos)
        if axis == "x":
            temp.x = next_pos.x
        else:
            temp.z = next_pos.z

        collision = False

        for ox in [-PLAYER_RADIUS, PLAYER_RADIUS]:
            for oz in [-PLAYER_RADIUS, PLAYER_RADIUS]:
                cx = int((temp.x + ox) / CELL_SIZE)
                cz = int((temp.z + oz) / CELL_SIZE)
                if not (0 <= cx < MAZE_SIZE and 0 <= cz < MAZE_SIZE):
                    continue

                door = game.door_map.get((cx, cz))
                if door and not door.is_open:
                    collision = True
                    break

                if game.maze[cz][cx] == 1:
                    collision = True
                    break
            if collision:
                break

        feet_y = next_pos.y - PLAYER_HEIGHT
        if not collision and feet_y < (LOG_HEIGHT - 0.05):
            half_len = LOG_LENGTH / 2.0
            half_thick = LOG_RADIUS
            for l in game.logs:
                dx = abs(temp.x - l["pos"].x)
                dz = abs(temp.z - l["pos"].z)
                if l["orientation"] == "x":
                    hit = (dx < (half_thick + PLAYER_RADIUS)) and (dz < (half_len + PLAYER_RADIUS))
                else:
                    hit = (dz < (half_thick + PLAYER_RADIUS)) and (dx < (half_len + PLAYER_RADIUS))
                if hit:
                    collision = True
                    break

        if collision:
            if axis == "x":
                adjusted.x = game.pos.x
            else:
                adjusted.z = game.pos.z

    return adjusted


def check_interactions(game):
    game.show_interaction_hint = False
    game.nearest_interactive = None

    best = None
    best_dist = 1e9

    def consider(kind, obj, dist, threshold):
        nonlocal best, best_dist
        if dist < threshold and dist < best_dist:
            best_dist = dist
            best = (kind, obj)

    for k in game.door_key_objects:
        if k.get("taken", False):
            continue
        consider("door_key", k, glm.distance(game.pos, k["pos"]), 2.0)

    for key in game.key_objects:
        if key["collected"]:
            continue
        consider("key", key, glm.distance(game.pos, key["pos"]), 2.0)

    for d in game.doors:
        door = d["obj"]
        consider("door", door, glm.distance(game.pos, door.pos), 2.5)

    if game.keys_collected >= game.keys_total:
        consider("exit", None, glm.distance(game.pos, game.exit_pos), 2.5)

    if best is not None:
        game.show_interaction_hint = True
        game.nearest_interactive = best
