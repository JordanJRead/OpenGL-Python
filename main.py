import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from vec3 import Vec3
from camera import Camera
from mesh import Mesh
from math import pi
from texture import CubeTexture

class App:

    def __init__(self) -> None:
        # Initialize
        width = 1920
        height = 1080
        pg.init()
        pg.display.set_mode((width, height), pg.OPENGL|pg.DOUBLEBUF)
        glClearColor(0.2, 0.2, 0.2, 1)
        glEnable(GL_DEPTH_TEST)

        self.clock = pg.time.Clock()

        # Shaders
        vertex_src: str = ""
        with open("./vertex.glsl") as file:
            vertex_src = file.readlines()
            
        fragment_src: str = ""
        with open("./fragment.glsl") as file:
            fragment_src = file.readlines()

        self.shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        glUseProgram(self.shader)

        self.camera = Camera(0.1, 100, 90, 1920/1080, 3, 0.005)
    
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "projectionMatrix"), 1, GL_TRUE, self.camera.get_projection_matrix())

        # Cube texture
        self.cubeTex = CubeTexture([
            "Images/red.png",
            "Images/orange.png",
            "Images/yellow.png",
            "Images/white.png",
            "Images/green.png",
            "Images/blue.png",
        ])

        glUniform1i(glGetUniformLocation(self.shader, "cubeTex"), 0)
        glActiveTexture(GL_TEXTURE0)

        # x y z r g b s t
        vertices = [
            # Front bottom right
            -0.5, -0.5, -0.5, 1, 0, 0, #0, 1,
             0.5, -0.5, -0.5, 0, 1, 0, #1, 1,
             0.5,  0.5, -0.5, 0, 0, 1, #1, 0,

            # Front top left
             0.5,  0.5, -0.5, 1, 0, 0, #1, 0,
            -0.5,  0.5, -0.5, 0, 1, 0, #0, 0,
            -0.5, -0.5, -0.5, 0, 0, 1, #0, 1,

            # Back bottom right
            -0.5, -0.5,  0.5, 1, 0, 0, #0, 1,
             0.5, -0.5,  0.5, 0, 1, 0, #1, 1,
             0.5,  0.5,  0.5, 0, 0, 1, #1, 0

            # Back top left
             0.5,  0.5,  0.5, 1, 0, 0, #1, 0,
            -0.5,  0.5,  0.5, 0, 1, 0, #0, 0,
            -0.5, -0.5,  0.5, 0, 0, 1, #0, 1,

            # Left top forward
            -0.5,  0.5,  0.5, 1, 0, 0, #0, 0,
            -0.5,  0.5, -0.5, 0, 1, 0, #1, 0,
            -0.5, -0.5, -0.5, 0, 0, 1, #1, 1,

            # Left bottom back
            -0.5, -0.5, -0.5, 1, 0, 0, #1, 1,
            -0.5, -0.5,  0.5, 0, 1, 0, #0, 1,
            -0.5,  0.5,  0.5, 0, 0, 1, #0, 0,

            # Right forward up
             0.5,  0.5,  0.5, 1, 0, 0, #
             0.5,  0.5, -0.5, 0, 1, 0,
             0.5, -0.5, -0.5, 0, 0, 1,

             0.5, -0.5, -0.5, 1, 0, 0,
             0.5, -0.5,  0.5, 0, 1, 0,
             0.5,  0.5,  0.5, 0, 0, 1,

            -0.5, -0.5, -0.5, 1, 0, 0,
             0.5, -0.5, -0.5, 0, 1, 0,
             0.5, -0.5,  0.5, 0, 0, 1,

             0.5, -0.5,  0.5, 1, 0, 0,
            -0.5, -0.5,  0.5, 0, 1, 0,
            -0.5, -0.5, -0.5, 0, 0, 1,

            -0.5,  0.5, -0.5, 1, 0, 0,
             0.5,  0.5, -0.5, 0, 1, 0,
             0.5,  0.5,  0.5, 0, 0, 1,

             0.5,  0.5,  0.5, 1, 0, 0,
            -0.5,  0.5,  0.5, 0, 1, 0,
            -0.5,  0.5, -0.5, 0, 0, 1
        ]

        # Meshes
        self.meshes = [
            Mesh(vertices, Vec3(0, 0, 2), Vec3(1, 1, 1))
        ]
        
        self.main_loop()
        self.destroy()

    def main_loop(self):
        running = True
        delta_time = self.clock.tick() / 1000
        while running:

            # Event loop
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        running = False

            # Movement
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
            
            self.camera.move_forward(input_vec.normalize(), delta_time)

            self.camera.rotate()

            # Rendering
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glUniformMatrix4fv(glGetUniformLocation(self.shader, "viewMatrix"), 1, GL_FALSE, self.camera.get_view_matrix())

            for mesh in self.meshes:
                glBindVertexArray(mesh.vao)
                glUniformMatrix4fv(glGetUniformLocation(self.shader, "modelMatrix"), 1, GL_FALSE, mesh.model_matrix)
                glDrawArrays(GL_TRIANGLES, 0, len(mesh.vertices))

            pg.display.flip()
            delta_time = self.clock.tick() / 1000

    def destroy(self):
        glDeleteBuffers(len(self.meshes), [t.vbo for t in self.meshes])
        glDeleteVertexArrays(len(self.meshes), [t.vao for t in self.meshes])
        pg.quit()

if __name__ == "__main__":
    app = App()