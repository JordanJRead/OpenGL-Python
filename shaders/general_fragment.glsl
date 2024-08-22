#version 330 core

uniform sampler2D imageTex;

in vec2 fragTexCoords;
in float light;

out vec4 color;

void main() {
    color = texture(imageTex, fragTexCoords) * light;
}