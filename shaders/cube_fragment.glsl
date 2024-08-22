#version 330 core

uniform samplerCube cubeTex;

in vec3 cubeTexCoords;
in float light;

out vec4 color;

void main() {
    color = texture(cubeTex, cubeTexCoords) * light;
}