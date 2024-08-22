import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

from vec3 import Vec3

from camera import Camera
from object import Object
from texture import CubeTexture
import input
import texture

class App:

    def __init__(self) -> None:

        # Initialize
        width = 1920
        height = 1080
        pg.init()
        pg.display.set_mode((width, height), pg.OPENGL|pg.DOUBLEBUF)
        glClearColor(0.2, 0.2, 0.2, 1)
        glEnable(GL_DEPTH_TEST)
        glActiveTexture(GL_TEXTURE0)

        self.clock = pg.time.Clock()

        self.camera = Camera(0.1, 10000, 90, 1920, 1080, 3, 0.005)

        # SHADERS
        self.cube_shader = self.create_simple_shader("./shaders/cube_vertex.glsl", "./shaders/cube_fragment.glsl")
        self.general_shader = self.create_simple_shader("./shaders/general_vertex.glsl", "./shaders/general_fragment.glsl")

        glUseProgram(self.cube_shader)
        glUniformMatrix4fv(glGetUniformLocation(self.cube_shader, "projectionMatrix"), 1, GL_TRUE, self.camera.projection_matrix)
        glUniform1i(glGetUniformLocation(self.cube_shader, "cubeTex"), 0)
        glUniform4f(glGetUniformLocation(self.cube_shader, "lightPos"), -4, 5, 1, 1)
        glUniform1f(glGetUniformLocation(self.cube_shader, "ambientLight"), 0.2)

        glUseProgram(self.general_shader)
        glUniformMatrix4fv(glGetUniformLocation(self.general_shader, "projectionMatrix"), 1, GL_TRUE, self.camera.projection_matrix)
        glUniform1i(glGetUniformLocation(self.general_shader, "imageTex"), 0)
        glUniform4f(glGetUniformLocation(self.general_shader, "lightPos"), -4, 5, 1, 1)
        glUniform1f(glGetUniformLocation(self.general_shader, "ambientLight"), 0.2)
        
        # TEXTURES
        cubeTex = CubeTexture([
            "Images/red.png",
            "Images/orange.png",
            "Images/yellow.png",
            "Images/white.png",
            "Images/green.png",
            "Images/blue.png",
        ])

        # OBJECTS
        cube_vertices = Object.cube_vertices(True)

        self.cube_objects = [
            Object(cube_vertices, Vec3(0, 0, 2), Vec3(1, 1, 1), cubeTex, True)
        ]
        
        self.skybox_objects = [
            Object(cube_vertices, Vec3(0, 0, 0), Vec3(10, 10, 10), cubeTex, True)
        ]

        self.general_objects = [
            Object(Object.billboard_vertices(), Vec3(0, -5, 0), Vec3(1, 1, 1), texture.Texture2D("Images/red.png"), False),
            Object(Object.cube_vertices(), Vec3(0, -10, 0,), Vec3(1, 5, 1), texture.Texture2D("Images/blue.png"), False)
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
            input_vec = input.get_move_vector()
            
            self.camera.move_forward(input_vec.normalize(), delta_time)

            self.camera.rotate()

            # Rendering
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            skybox_view_matrix = self.camera.get_view_matrix(False)

            # Cubes
            glUseProgram(self.cube_shader)

            # Skybox objects
            # if len(self.skybox_objects) > 0:

            #     glUniformMatrix4fv(glGetUniformLocation(self.cube_shader, "viewMatrix"), 1, GL_FALSE, skybox_view_matrix)

            #     for skybox_object in self.skybox_objects:
            #         glBindVertexArray(skybox_object.vao)
            #         glUniformMatrix4fv(glGetUniformLocation(self.cube_shader, "modelMatrix"), 1, GL_FALSE, skybox_object.model_matrix)
            #         glDrawArrays(GL_TRIANGLES, 0, len(skybox_object.vertices))

            glClear(GL_DEPTH_BUFFER_BIT)
            
            self.render_objects()

            pg.display.flip()
            delta_time = self.clock.tick() / 1000

    def destroy(self):
        glDeleteBuffers(len(self.cube_objects), [t.vbo for t in self.cube_objects])
        glDeleteVertexArrays(len(self.cube_objects), [t.vao for t in self.cube_objects])
        pg.quit()
    
    def render_objects(self):
        glUseProgram(self.cube_shader)
        
        # either do skybox code here or in a different function to be called elsewhere

        glUniformMatrix4fv(glGetUniformLocation(self.cube_shader, "viewMatrix"), 1, GL_FALSE, self.camera.get_view_matrix())

        # Cubes
        if len(self.cube_objects) > 0:
            for cube in self.cube_objects:
                self.render_object(self.cube_shader, cube)
        
        # General
        if len(self.general_objects) > 0:
            glUseProgram(self.general_shader)
            
            glUniformMatrix4fv(glGetUniformLocation(self.general_shader, "viewMatrix"), 1, GL_FALSE, self.camera.get_view_matrix())

            for obj in self.general_objects:
                self.render_object(self.general_shader, obj)
    
    def render_object(self, shader, obj: Object):
        glBindVertexArray(obj.vao)
        obj.texture.use()
        glUniformMatrix4fv(glGetUniformLocation(shader, "modelMatrix"), 1, GL_FALSE, obj.model_matrix)
        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertices))

    def create_simple_shader(self, vertex_path, fragment_path):

        vertex_src = ""
        fragment_src = ""

        with open(vertex_path) as vertex_file:
            vertex_src = vertex_file.readlines()

        with open(fragment_path) as fragment_file:
            fragment_src = fragment_file.readlines()
        
        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

if __name__ == "__main__":

    app = App()