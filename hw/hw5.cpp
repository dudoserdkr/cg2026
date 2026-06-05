//
// Created by Ivan Tiulpa
//
#include <iostream>
#include <cmath>
#include <vector>
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>

// ---------- shaders ----------
const char* vertexShaderSource = R"(
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 TexCoord;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    TexCoord = aTexCoord;
}
)";

const char* fragmentShaderSource = R"(
#version 330 core
in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D ourTexture;

void main()
{
    FragColor = texture(ourTexture, TexCoord);
}
)";

// Solid-color shader for stencil outline
const char* outlineVertexShaderSource = R"(
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}
)";

const char* outlineFragmentShaderSource = R"(
#version 330 core
out vec4 FragColor;

uniform vec3 outlineColor;

void main()
{
    FragColor = vec4(outlineColor, 1.0);
}
)";

// ---------- texture generation ----------
GLuint generateCheckerboard(int size, int squares,
                            unsigned char r1, unsigned char g1, unsigned char b1,
                            unsigned char r2, unsigned char g2, unsigned char b2)
{
    unsigned char* data = new unsigned char[size * size * 3];
    int cellSize = size / squares;
    for (int y = 0; y < size; y++) {
        for (int x = 0; x < size; x++) {
            bool isWhite = ((x / cellSize) + (y / cellSize)) % 2 == 0;
            int idx = (y * size + x) * 3;
            data[idx + 0] = isWhite ? r1 : r2;
            data[idx + 1] = isWhite ? g1 : g2;
            data[idx + 2] = isWhite ? b1 : b2;
        }
    }
    GLuint tex;
    glGenTextures(1, &tex);
    glBindTexture(GL_TEXTURE_2D, tex);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, size, size, 0, GL_RGB, GL_UNSIGNED_BYTE, data);
    delete[] data;
    return tex;
}

unsigned int compileShader(GLenum type, const char* source)
{
    unsigned int shader = glCreateShader(type);
    glShaderSource(shader, 1, &source, NULL);
    glCompileShader(shader);
    int success;
    char infoLog[512];
    glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
    if (!success) {
        glGetShaderInfoLog(shader, 512, NULL, infoLog);
        std::cout << "SHADER ERROR:\n" << infoLog << std::endl;
    }
    return shader;
}

unsigned int linkProgram(unsigned int vs, unsigned int fs)
{
    unsigned int program = glCreateProgram();
    glAttachShader(program, vs);
    glAttachShader(program, fs);
    glLinkProgram(program);
    int success;
    char infoLog[512];
    glGetProgramiv(program, GL_LINK_STATUS, &success);
    if (!success) {
        glGetProgramInfoLog(program, 512, NULL, infoLog);
        std::cout << "LINK ERROR:\n" << infoLog << std::endl;
    }
    return program;
}

// ---------- cube data ----------
struct CubeInfo {
    glm::vec3 position;
    float scale;
};

// ---------- camera ----------
glm::vec3 cameraPos   = glm::vec3(0.0f, 2.0f, 6.0f);
glm::vec3 cameraFront = glm::vec3(0.0f, -0.3f, -1.0f);
glm::vec3 cameraUp    = glm::vec3(0.0f, 1.0f, 0.0f);

float yaw   = -90.0f;
float pitch = -15.0f;
float cameraSpeed = 3.0f;
float mouseSensitivity = 0.1f;

bool firstMouse = true;
double lastMouseX = 400.0, lastMouseY = 300.0;
bool cursorCaptured = false;

int activeCubeIndex = 0;
const int NUM_CUBES = 5;

// ---------- callbacks ----------
void mouseCallback(GLFWwindow* /*window*/, double xpos, double ypos)
{
    if (!cursorCaptured) return;

    if (firstMouse) {
        lastMouseX = xpos;
        lastMouseY = ypos;
        firstMouse = false;
    }

    float xoffset = (float)(xpos - lastMouseX) * mouseSensitivity;
    float yoffset = (float)(lastMouseY - ypos) * mouseSensitivity; // reversed: y goes bottom-to-top
    lastMouseX = xpos;
    lastMouseY = ypos;

    yaw   += xoffset;
    pitch += yoffset;

    if (pitch > 89.0f)  pitch = 89.0f;
    if (pitch < -89.0f) pitch = -89.0f;

    glm::vec3 front;
    front.x = cos(glm::radians(yaw)) * cos(glm::radians(pitch));
    front.y = sin(glm::radians(pitch));
    front.z = sin(glm::radians(yaw)) * cos(glm::radians(pitch));
    cameraFront = glm::normalize(front);
}

void keyCallback(GLFWwindow* window, int key, int /*scancode*/, int action, int /*mods*/)
{
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);

    // Tab to switch active cube
    if (key == GLFW_KEY_TAB && action == GLFW_PRESS)
        activeCubeIndex = (activeCubeIndex + 1) % NUM_CUBES;

    // 1-5 keys to select cube directly
    if (action == GLFW_PRESS && key >= GLFW_KEY_1 && key <= GLFW_KEY_5) {
        int idx = key - GLFW_KEY_1;
        if (idx < NUM_CUBES) activeCubeIndex = idx;
    }

    // Right-click toggle: press C to capture/release cursor for camera
    if (key == GLFW_KEY_C && action == GLFW_PRESS) {
        cursorCaptured = !cursorCaptured;
        if (cursorCaptured) {
            glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
            firstMouse = true;
        } else {
            glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL);
        }
    }
}

void mouseButtonCallback(GLFWwindow* window, int button, int action, int /*mods*/)
{
    if (button == GLFW_MOUSE_BUTTON_RIGHT && action == GLFW_PRESS) {
        cursorCaptured = !cursorCaptured;
        if (cursorCaptured) {
            glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);
            firstMouse = true;
        } else {
            glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL);
        }
    }
}

int main(void)
{
    if (!glfwInit())
        return -1;

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    glfwWindowHint(GLFW_STENCIL_BITS, 8);
#ifdef __APPLE__
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
#endif

    int winW = 1024, winH = 768;
    GLFWwindow* window = glfwCreateWindow(winW, winH, "HW5 - Cubes + Stencil Outline + Camera", NULL, NULL);
    if (!window) {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);
    glfwSetKeyCallback(window, keyCallback);
    glfwSetCursorPosCallback(window, mouseCallback);
    glfwSetMouseButtonCallback(window, mouseButtonCallback);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    // ---------- compile shaders ----------
    // Main textured shader
    unsigned int vs  = compileShader(GL_VERTEX_SHADER, vertexShaderSource);
    unsigned int fs  = compileShader(GL_FRAGMENT_SHADER, fragmentShaderSource);
    unsigned int mainShader = linkProgram(vs, fs);
    glDeleteShader(vs);
    glDeleteShader(fs);

    // Outline solid-color shader
    unsigned int ovs = compileShader(GL_VERTEX_SHADER, outlineVertexShaderSource);
    unsigned int ofs = compileShader(GL_FRAGMENT_SHADER, outlineFragmentShaderSource);
    unsigned int outlineShader = linkProgram(ovs, ofs);
    glDeleteShader(ovs);
    glDeleteShader(ofs);

    // ---------- cube vertex data (pos + texcoord) ----------
    float cubeVertices[] = {
        // Back face
        -0.5f, -0.5f, -0.5f,  0.0f, 0.0f,
         0.5f, -0.5f, -0.5f,  1.0f, 0.0f,
         0.5f,  0.5f, -0.5f,  1.0f, 1.0f,
         0.5f,  0.5f, -0.5f,  1.0f, 1.0f,
        -0.5f,  0.5f, -0.5f,  0.0f, 1.0f,
        -0.5f, -0.5f, -0.5f,  0.0f, 0.0f,
        // Front face
        -0.5f, -0.5f,  0.5f,  0.0f, 0.0f,
         0.5f, -0.5f,  0.5f,  1.0f, 0.0f,
         0.5f,  0.5f,  0.5f,  1.0f, 1.0f,
         0.5f,  0.5f,  0.5f,  1.0f, 1.0f,
        -0.5f,  0.5f,  0.5f,  0.0f, 1.0f,
        -0.5f, -0.5f,  0.5f,  0.0f, 0.0f,
        // Left face
        -0.5f,  0.5f,  0.5f,  1.0f, 1.0f,
        -0.5f,  0.5f, -0.5f,  0.0f, 1.0f,
        -0.5f, -0.5f, -0.5f,  0.0f, 0.0f,
        -0.5f, -0.5f, -0.5f,  0.0f, 0.0f,
        -0.5f, -0.5f,  0.5f,  1.0f, 0.0f,
        -0.5f,  0.5f,  0.5f,  1.0f, 1.0f,
        // Right face
         0.5f,  0.5f,  0.5f,  1.0f, 1.0f,
         0.5f,  0.5f, -0.5f,  0.0f, 1.0f,
         0.5f, -0.5f, -0.5f,  0.0f, 0.0f,
         0.5f, -0.5f, -0.5f,  0.0f, 0.0f,
         0.5f, -0.5f,  0.5f,  1.0f, 0.0f,
         0.5f,  0.5f,  0.5f,  1.0f, 1.0f,
        // Bottom face
        -0.5f, -0.5f, -0.5f,  0.0f, 0.0f,
         0.5f, -0.5f, -0.5f,  1.0f, 0.0f,
         0.5f, -0.5f,  0.5f,  1.0f, 1.0f,
         0.5f, -0.5f,  0.5f,  1.0f, 1.0f,
        -0.5f, -0.5f,  0.5f,  0.0f, 1.0f,
        -0.5f, -0.5f, -0.5f,  0.0f, 0.0f,
        // Top face
        -0.5f,  0.5f, -0.5f,  0.0f, 0.0f,
         0.5f,  0.5f, -0.5f,  1.0f, 0.0f,
         0.5f,  0.5f,  0.5f,  1.0f, 1.0f,
         0.5f,  0.5f,  0.5f,  1.0f, 1.0f,
        -0.5f,  0.5f,  0.5f,  0.0f, 1.0f,
        -0.5f,  0.5f, -0.5f,  0.0f, 0.0f,
    };

    unsigned int VAO, VBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);

    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(cubeVertices), cubeVertices, GL_STATIC_DRAW);

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);
    glBindVertexArray(0);

    // ---------- cube configurations ----------
    std::vector<CubeInfo> cubes = {
        { glm::vec3( 0.0f, 0.5f,  0.0f), 1.0f },
        { glm::vec3( 2.5f, 0.4f,  1.0f), 0.8f },
        { glm::vec3(-2.0f, 0.75f, -1.5f), 1.5f },
        { glm::vec3( 1.5f, 0.3f, -2.5f), 0.6f },
        { glm::vec3(-1.0f, 0.25f,  2.0f), 0.5f },
    };

    // ---------- textures (one per cube, different colors) ----------
    std::vector<GLuint> textures;
    textures.push_back(generateCheckerboard(64, 6, 240, 140,  30, 255, 255, 240)); // orange/cream
    textures.push_back(generateCheckerboard(64, 6,  50, 120, 200, 220, 220, 220)); // blue/gray
    textures.push_back(generateCheckerboard(64, 6, 180,  50,  50, 240, 200, 200)); // red/pink
    textures.push_back(generateCheckerboard(64, 6,  50, 180,  80, 200, 240, 200)); // green/light
    textures.push_back(generateCheckerboard(64, 6, 160,  80, 200, 230, 220, 240)); // purple/lavender

    // Uniform locations — main shader
    int modelLoc = glGetUniformLocation(mainShader, "model");
    int viewLoc  = glGetUniformLocation(mainShader, "view");
    int projLoc  = glGetUniformLocation(mainShader, "projection");

    // Uniform locations — outline shader
    int oModelLoc = glGetUniformLocation(outlineShader, "model");
    int oViewLoc  = glGetUniformLocation(outlineShader, "view");
    int oProjLoc  = glGetUniformLocation(outlineShader, "projection");
    int oColorLoc = glGetUniformLocation(outlineShader, "outlineColor");

    glEnable(GL_DEPTH_TEST);
    glClearColor(0.12f, 0.12f, 0.14f, 1.0f);

    double lastTime = glfwGetTime();
    float activeRotation = 0.0f;

    std::cout << "Controls:" << std::endl;
    std::cout << "  WASD       - move camera" << std::endl;
    std::cout << "  Mouse      - look around (right-click or C to toggle capture)" << std::endl;
    std::cout << "  Q/E        - move camera down/up" << std::endl;
    std::cout << "  Tab / 1-5  - select active cube" << std::endl;
    std::cout << "  Esc        - quit" << std::endl;

    while (!glfwWindowShouldClose(window))
    {
        double currentTime = glfwGetTime();
        float deltaTime = (float)(currentTime - lastTime);
        lastTime = currentTime;

        // --- Camera movement (WASD + QE) ---
        float velocity = cameraSpeed * deltaTime;
        if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
            cameraPos += velocity * cameraFront;
        if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
            cameraPos -= velocity * cameraFront;
        if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
            cameraPos -= glm::normalize(glm::cross(cameraFront, cameraUp)) * velocity;
        if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
            cameraPos += glm::normalize(glm::cross(cameraFront, cameraUp)) * velocity;
        if (glfwGetKey(window, GLFW_KEY_E) == GLFW_PRESS)
            cameraPos += cameraUp * velocity;
        if (glfwGetKey(window, GLFW_KEY_Q) == GLFW_PRESS)
            cameraPos -= cameraUp * velocity;

        // --- Active cube animation: rotation around its center ---
        activeRotation += deltaTime * 90.0f; // 90 deg/sec

        // --- Matrices ---
        int fbW, fbH;
        glfwGetFramebufferSize(window, &fbW, &fbH);
        glViewport(0, 0, fbW, fbH);

        float aspect = (float)fbW / (float)fbH;
        glm::mat4 projection = glm::perspective(glm::radians(45.0f), aspect, 0.1f, 100.0f);
        glm::mat4 view = glm::lookAt(cameraPos, cameraPos + cameraFront, cameraUp);

        // --- Render ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);

        // ====== PASS 1: Draw all cubes, writing stencil for active cube ======
        glEnable(GL_STENCIL_TEST);
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE);

        glUseProgram(mainShader);
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, glm::value_ptr(view));
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, glm::value_ptr(projection));
        glBindVertexArray(VAO);

        for (int i = 0; i < NUM_CUBES; i++) {
            // Write 1 to stencil buffer only for the active cube
            if (i == activeCubeIndex) {
                glStencilFunc(GL_ALWAYS, 1, 0xFF);
                glStencilMask(0xFF);
            } else {
                glStencilFunc(GL_ALWAYS, 0, 0xFF);
                glStencilMask(0x00); // don't write stencil for inactive cubes
            }

            glm::mat4 model = glm::mat4(1.0f);
            model = glm::translate(model, cubes[i].position);

            // Active cube rotates around its center
            if (i == activeCubeIndex) {
                model = glm::rotate(model, glm::radians(activeRotation), glm::vec3(0.0f, 1.0f, 0.0f));
            }

            model = glm::scale(model, glm::vec3(cubes[i].scale));

            glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(model));
            glBindTexture(GL_TEXTURE_2D, textures[i]);
            glDrawArrays(GL_TRIANGLES, 0, 36);
        }

        // ====== PASS 2: Draw outline for active cube using stencil ======
        glStencilFunc(GL_NOTEQUAL, 1, 0xFF);
        glStencilMask(0x00);
        glDisable(GL_DEPTH_TEST);

        glUseProgram(outlineShader);
        glUniformMatrix4fv(oViewLoc, 1, GL_FALSE, glm::value_ptr(view));
        glUniformMatrix4fv(oProjLoc, 1, GL_FALSE, glm::value_ptr(projection));
        glUniform3f(oColorLoc, 1.0f, 0.85f, 0.0f); // yellow outline

        {
            float outlineScale = 1.08f; // slightly larger
            glm::mat4 model = glm::mat4(1.0f);
            model = glm::translate(model, cubes[activeCubeIndex].position);
            model = glm::rotate(model, glm::radians(activeRotation), glm::vec3(0.0f, 1.0f, 0.0f));
            model = glm::scale(model, glm::vec3(cubes[activeCubeIndex].scale * outlineScale));

            glUniformMatrix4fv(oModelLoc, 1, GL_FALSE, glm::value_ptr(model));
            glBindVertexArray(VAO);
            glDrawArrays(GL_TRIANGLES, 0, 36);
        }

        // Restore state
        glStencilMask(0xFF);
        glStencilFunc(GL_ALWAYS, 0, 0xFF);
        glEnable(GL_DEPTH_TEST);
        glDisable(GL_STENCIL_TEST);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // Cleanup
    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    for (auto& t : textures) glDeleteTextures(1, &t);
    glDeleteProgram(mainShader);
    glDeleteProgram(outlineShader);

    glfwTerminate();
    return 0;
}
