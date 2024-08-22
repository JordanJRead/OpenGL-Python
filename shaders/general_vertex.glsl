#version 330 core

layout (location=0) in vec3 vertexPos;
layout (location=1) in vec3 normal;
layout (location=2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;

uniform vec4 lightPos;
uniform float ambientLight;

out vec2 fragTexCoords;
out float light;

void main() {
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPos, 1);
    fragTexCoords = texCoords;
    vec4 lightDir = lightPos - (modelMatrix * vec4(vertexPos, 1));
    light = max(dot(normalize(vec4(normal, 1)), normalize(lightDir)), 0) + ambientLight;
    light = min(light, 1);
}