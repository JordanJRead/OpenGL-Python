from vec3 import Vec3
import pyrr
import numpy as np
from OpenGL.GL import *
from texture import Texture

class Object:

    def __init__(self, vertices: tuple[float], position: Vec3, scale: Vec3, texture: Texture, cubemap: bool = False) -> None:
        self.vertices = np.array(vertices, dtype=np.float32)
        self.model_matrix = pyrr.matrix44.create_identity(dtype=np.float32)
        self.model_matrix = pyrr.matrix44.multiply(self.model_matrix, pyrr.matrix44.create_from_scale(scale.to_list(), dtype=np.float32))
        self.model_matrix = pyrr.matrix44.multiply(self.model_matrix, pyrr.matrix44.create_from_translation(position.to_list(), dtype=np.float32))
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        if cubemap:
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
            
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))

        else:
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(0))
            
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(3 * 4))

            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * 4, ctypes.c_void_p(6 * 4))

        self.texture = texture

    @staticmethod
    def billboard_vertices() -> list[float]:
        # x y z nx ny nz s t
        vertices = [
            # Bottom left
            -0.5, 0.5, 0, 0, 0, 1, 0, 0,
            -0.5, -0.5, 0, 0, 0, 1, 0, 1,
            0.5, -0.5, 0, 0, 0, 1, 1, 1,

            # Top right
            0.5, -0.5, 0, 0, 0, 1, 1, 1,
            0.5, 0.5, 0, 0, 0, 1, 1, 0,
            -0.5, 0.5, 0, 0, 0, 1, 0, 0
        ]

        return vertices

    @staticmethod
    def cube_vertices(cubemap: bool = False) -> list[float]:
        
        if cubemap:
            # x y z nx ny nz
            vertices = [
                # Front bottom right
                -0.5, -0.5,  0.5, 0, 0, 1,
                0.5, -0.5,  0.5, 0, 0, 1,
                0.5,  0.5,  0.5, 0, 0, 1,

                # Front top left
                0.5,  0.5,  0.5, 0, 0, 1,
                -0.5,  0.5,  0.5, 0, 0, 1,
                -0.5, -0.5,  0.5, 0, 0, 1,

                # Back bottom right
                -0.5, -0.5,  -0.5, 0, 0, -1,
                0.5, -0.5,  -0.5, 0, 0, -1,
                0.5,  0.5,  -0.5, 0, 0, -1,

                # Back top left
                0.5,  0.5,  -0.5, 0, 0, -1,
                -0.5,  0.5,  -0.5, 0, 0, -1,
                -0.5, -0.5,  -0.5, 0, 0, -1,

                # Left top forward
                -0.5,  0.5, -0.5, -1, 0, 0,
                -0.5,  0.5,  0.5, -1, 0, 0,
                -0.5, -0.5,  0.5, -1, 0, 0,

                # Left bottom back
                -0.5, -0.5,  0.5, -1, 0, 0,
                -0.5, -0.5, -0.5, -1, 0, 0,
                -0.5,  0.5, -0.5, -1, 0, 0,

                # Right forward up
                0.5,  0.5, -0.5, 1, 0, 0,
                0.5,  0.5,  0.5, 1, 0, 0,
                0.5, -0.5,  0.5, 1, 0, 0,

                0.5, -0.5,  0.5, 1, 0, 0,
                0.5, -0.5, -0.5, 1, 0, 0,
                0.5,  0.5, -0.5, 1, 0, 0,

                # Bottom
                -0.5, -0.5,  0.5, 0, -1, 0,
                0.5, -0.5,  0.5, 0, -1, 0,
                0.5, -0.5, -0.5, 0, -1, 0,

                0.5, -0.5, -0.5, 0, -1, 0,
                -0.5, -0.5, -0.5, 0, -1, 0,
                -0.5, -0.5,  0.5, 0, -1, 0,

                # Top
                -0.5,  0.5,  0.5, 0, 1, 0,
                0.5,  0.5,  0.5, 0, 1, 0,
                0.5,  0.5, -0.5, 0, 1, 0,

                0.5,  0.5, -0.5, 0, 1, 0,
                -0.5,  0.5, -0.5, 0, 1, 0,
                -0.5,  0.5,  0.5, 0, 1, 0
            ]

            return vertices
        
        else:
            # x y z nx ny nz s t
            vertices = [
                # Front bottom right
                -0.5, -0.5,  0.5, 0, 0, 1, 0, 1,
                0.5, -0.5,  0.5, 0, 0, 1, 1, 1,
                0.5,  0.5,  0.5, 0, 0, 1, 1, 0,

                # Front top left
                0.5,  0.5,  0.5, 0, 0, 1, 1, 0,
                -0.5,  0.5,  0.5, 0, 0, 1, 0, 0,
                -0.5, -0.5,  0.5, 0, 0, 1, 0, 1,

                # Back bottom right
                -0.5, -0.5,  -0.5, 0, 0, -1, 1, 1,
                0.5, -0.5,  -0.5, 0, 0, -1, 0, 1,
                0.5,  0.5,  -0.5, 0, 0, -1, 0, 0,

                # Back top left
                0.5,  0.5,  -0.5, 0, 0, -1, 0, 0,
                -0.5,  0.5,  -0.5, 0, 0, -1, 1, 0,
                -0.5, -0.5,  -0.5, 0, 0, -1, 1, 1,

                # Left top forward
                -0.5,  0.5, -0.5, -1, 0, 0, 0, 0,
                -0.5,  0.5,  0.5, -1, 0, 0, 1, 0,
                -0.5, -0.5,  0.5, -1, 0, 0, 1, 1,

                # Left bottom back
                -0.5, -0.5,  0.5, -1, 0, 0, 1, 1,
                -0.5, -0.5, -0.5, -1, 0, 0, 0, 1,
                -0.5,  0.5, -0.5, -1, 0, 0, 0, 0,

                # Right forward up
                0.5,  0.5, -0.5, 1, 0, 0, 1, 0,
                0.5,  0.5,  0.5, 1, 0, 0, 0, 0,
                0.5, -0.5,  0.5, 1, 0, 0, 0, 1,

                0.5, -0.5,  0.5, 1, 0, 0, 0, 1,
                0.5, -0.5, -0.5, 1, 0, 0, 1, 1,
                0.5,  0.5, -0.5, 1, 0, 0, 1, 0,

                # Bottom
                -0.5, -0.5,  0.5, 0, -1, 0, 0, 0,
                0.5, -0.5,  0.5, 0, -1, 0, 1, 0,
                0.5, -0.5, -0.5, 0, -1, 0, 1, 1,

                0.5, -0.5, -0.5, 0, -1, 0, 1, 1,
                -0.5, -0.5, -0.5, 0, -1, 0, 0, 1,
                -0.5, -0.5,  0.5, 0, -1, 0, 0, 0,

                # Top
                -0.5,  0.5,  0.5, 0, 1, 0, 0, 1,
                0.5,  0.5,  0.5, 0, 1, 0, 1, 1,
                0.5,  0.5, -0.5, 0, 1, 0, 1, 0,

                0.5,  0.5, -0.5, 0, 1, 0, 1, 0,
                -0.5,  0.5, -0.5, 0, 1, 0, 0, 0,
                -0.5,  0.5,  0.5, 0, 1, 0, 0, 1
            ]
            return vertices