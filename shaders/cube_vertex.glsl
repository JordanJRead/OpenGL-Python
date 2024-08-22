#version 330 core

layout (location=0) in vec3 vertexPos;
layout (location=1) in vec3 normal;

uniform mat4 modelMatrix;
uniform mat4 projectionMatrix;
uniform mat4 viewMatrix;
uniform vec4 lightPos;
uniform float ambientLight;

out vec3 cubeTexCoords;
out float light;

void main() {
    gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPos, 1);
    cubeTexCoords = vertexPos;
    vec4 lightDir = lightPos - (modelMatrix * vec4(vertexPos, 1));
    light = max(dot(normalize(vec4(normal, 1)), normalize(lightDir)), 0) + ambientLight;
    light = min(light, 1);
}