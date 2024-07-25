from vec3 import Vec3
import numpy as np
import pygame as pg
from math import tan, radians, sin, cos, pi
import pyrr

class Camera:
    
    def __init__(self, near_distance: float, far_distance: float, horizontal_fov_deg: float, aspect_ratio, speed, sens, position: Vec3 = Vec3(0, 0, 0)) -> None:
        self.position = position
        self.pitch = 0
        self.yaw = 0
        self.speed = speed
        self.sens = sens
        self.horizontal_fov_deg = horizontal_fov_deg
        self.near_distance = near_distance
        self.far_distance = far_distance
        self.aspect_ratio = aspect_ratio
        self.prev_mouse_position = pg.mouse.get_pos()

    def get_projection_matrix(self):
        width = self.near_distance*tan(radians(self.horizontal_fov_deg / 2))
        height = width / self.aspect_ratio

        a = (self.near_distance + self.far_distance) / (self.far_distance - self.near_distance)
        b = (-2 * self.far_distance * self.near_distance) / (self.far_distance - self.near_distance)

        projection = np.array([
            [self.near_distance / width, 0,                           0, 0],
            [0,                          self.near_distance / height, 0, 0],
            [0,                          0,                           a, b],
            [0,                          0,                           1, 0]
        ], dtype=np.float32)

        return projection
    
    def get_view_matrix(self):
        camera_matrix = pyrr.matrix44.create_identity(dtype=np.float32)
        camera_matrix = pyrr.matrix44.multiply(camera_matrix, pyrr.matrix44.create_from_axis_rotation([1, 0, 0], self.pitch, dtype=np.float32))
        camera_matrix = pyrr.matrix44.multiply(camera_matrix, pyrr.matrix44.create_from_axis_rotation([0, 1, 0], self.yaw, dtype=np.float32))
        camera_matrix = pyrr.matrix44.multiply(camera_matrix, pyrr.matrix44.create_from_translation(self.position.to_list()))
        return pyrr.matrix44.inverse(camera_matrix)
    
    def move_forward(self, move_by: Vec3, delta_time: float):
        rotated_vector = Vec3(move_by.x * cos(-self.yaw) - move_by.z * sin(-self.yaw), move_by.y, move_by.x * sin(-self.yaw) + move_by.z * cos(-self.yaw))
        self.position += rotated_vector * self.speed * delta_time
    
    def rotate(self):
        current_mouse_x = pg.mouse.get_pos()[0]
        delta_mouse_x = current_mouse_x - self.prev_mouse_position[0]
        self.yaw += delta_mouse_x * self.sens
        if self.yaw > 2 * pi:
            self.yaw -= 2 * pi
        if self.yaw < 0:
            self.yaw += 2 * pi
        
        current_mouse_y = pg.mouse.get_pos()[1]
        delta_mouse_y = current_mouse_y - self.prev_mouse_position[1]
        self.pitch += delta_mouse_y * self.sens
        if self.pitch >= pi / 2:
            self.pitch = pi / 2 -0.001
        if self.pitch <= -pi / 2:
            self.pitch = -pi / 2 + 0.001

        self.prev_mouse_position = pg.mouse.get_pos()