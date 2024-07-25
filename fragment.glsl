#version 330 core

uniform samplerCube cubeTex;

in vec3 fragmentColor;
in vec3 cubeTexCoords;

out vec4 color;

void main() {
    color = texture(cubeTex, cubeTexCoords);
}