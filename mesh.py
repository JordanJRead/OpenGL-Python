from vec3 import Vec3
import pyrr
import numpy as np
from OpenGL.GL import *

class Mesh:

    def __init__(self, vertices: tuple[float], position: Vec3, scale: Vec3 = Vec3(1, 1, 1)) -> None:
        self.vertices = np.array(vertices, dtype=np.float32)
        self.model_matrix = pyrr.matrix44.create_identity(dtype=np.float32)
        self.model_matrix = pyrr.matrix44.multiply(self.model_matrix, pyrr.matrix44.create_from_scale(scale.to_list(), dtype=np.float32))
        self.model_matrix = pyrr.matrix44.multiply(self.model_matrix, pyrr.matrix44.create_from_translation(position.to_list(), dtype=np.float32))
        print(self.model_matrix)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))