from vec3 import Vec3
import pygame as pg

def get_move_vector() -> Vec3:
    input_vec = Vec3(0, 0, 0)
    keys = pg.key.get_pressed()
    if keys[pg.K_w]:
        input_vec.z += 1
    if keys[pg.K_s]:
        input_vec.z -= 1
    if keys[pg.K_d]:
        input_vec.x += 1
    if keys[pg.K_a]:
        input_vec.x -= 1
    if keys[pg.K_SPACE]:
        input_vec.y += 1
    if keys[pg.K_LSHIFT]:
        input_vec.y -= 1
    
    return input_vec