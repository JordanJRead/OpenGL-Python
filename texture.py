import pygame as pg
from OpenGL.GL import *

class CubeTexture:
    def __init__(self, filepaths: list[str]):
        images = []
        width = pg.image.load(filepaths[0]).get_width()
        for path in filepaths:
            image = pg.image.load(path).convert_alpha()
            image = pg.transform.flip(image, True, False)
            image_data = pg.image.tostring(image, "RGBA")
            images.append(image_data)
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)
        
        faces = [GL_TEXTURE_CUBE_MAP_POSITIVE_X, GL_TEXTURE_CUBE_MAP_NEGATIVE_X, GL_TEXTURE_CUBE_MAP_POSITIVE_Y, GL_TEXTURE_CUBE_MAP_NEGATIVE_Y, GL_TEXTURE_CUBE_MAP_POSITIVE_Z, GL_TEXTURE_CUBE_MAP_NEGATIVE_Z]

        for i, data in enumerate(images):
            glTexImage2D(faces[i], 0, GL_RGBA, width, width, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    
    def use(self):
        glBindTexture(GL_TEXTURE_CUBE_MAP, self.texture)
    
    def destroy(self):
        glDeleteTextures(1, (self.texture,))