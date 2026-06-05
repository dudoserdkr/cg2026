//
// Created by Ivan Tiulpa
//
#include <iostream>
#include <cmath>
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

out vec2 TexCoord;

void main()
{
    gl_Position = model * vec4(aPos, 1.0);
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

// Generate a checkerboard texture
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

// Rectangle state
float rectX = 0.0f, rectY = 0.0f;    // position (center)
float rectW = 0.4f, rectH = 0.3f;    // half-width/half-height in NDC
float rotationAngle = 0.0f;
bool mouseHovering = false;

void keyCallback(GLFWwindow* window, int key, int /*scancode*/, int action, int /*mods*/)
{
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);
}

int main(void)
{
    if (!glfwInit())
        return -1;

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
#ifdef __APPLE__
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
#endif

    int winW = 800, winH = 600;
    GLFWwindow* window = glfwCreateWindow(winW, winH, "HW4 - Keyboard & Mouse", NULL, NULL);
    if (!window) {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);
    glfwSetKeyCallback(window, keyCallback);
    glfwSwapInterval(1);

    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    // ---------- compile & link shaders ----------
    unsigned int vs = compileShader(GL_VERTEX_SHADER, vertexShaderSource);
    unsigned int fs = compileShader(GL_FRAGMENT_SHADER, fragmentShaderSource);

    unsigned int shaderProgram = glCreateProgram();
    glAttachShader(shaderProgram, vs);
    glAttachShader(shaderProgram, fs);
    glLinkProgram(shaderProgram);
    {
        int success;
        char infoLog[512];
        glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
        if (!success) {
            glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
            std::cout << "LINK ERROR:\n" << infoLog << std::endl;
        }
    }
    glDeleteShader(vs);
    glDeleteShader(fs);

    // ---------- quad data ----------
    float quadVertices[] = {
        // pos                // texcoord
        -0.5f,  0.5f, 0.0f,  0.0f, 1.0f,
         0.5f,  0.5f, 0.0f,  1.0f, 1.0f,
         0.5f, -0.5f, 0.0f,  1.0f, 0.0f,
        -0.5f, -0.5f, 0.0f,  0.0f, 0.0f,
    };
    unsigned int quadIndices[] = { 0, 1, 3, 1, 2, 3 };

    unsigned int VAO, VBO, EBO;
    glGenVertexArrays(1, &VAO);
    glGenBuffers(1, &VBO);
    glGenBuffers(1, &EBO);

    glBindVertexArray(VAO);
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(quadVertices), quadVertices, GL_STATIC_DRAW);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(quadIndices), quadIndices, GL_STATIC_DRAW);

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(3 * sizeof(float)));
    glEnableVertexAttribArray(1);
    glBindVertexArray(0);

    // Texture: orange/white checkerboard
    GLuint tex = generateCheckerboard(64, 6, 240, 140, 30, 255, 255, 240);

    int modelLoc = glGetUniformLocation(shaderProgram, "model");

    glClearColor(0.12f, 0.12f, 0.14f, 1.0f);

    double lastTime = glfwGetTime();
    const float moveSpeed = 1.2f; // NDC units per second

    while (!glfwWindowShouldClose(window))
    {
        double currentTime = glfwGetTime();
        float deltaTime = (float)(currentTime - lastTime);
        lastTime = currentTime;

        // --- Keyboard: move rectangle ---
        if (glfwGetKey(window, GLFW_KEY_LEFT) == GLFW_PRESS ||
            glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
            rectX -= moveSpeed * deltaTime;
        if (glfwGetKey(window, GLFW_KEY_RIGHT) == GLFW_PRESS ||
            glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
            rectX += moveSpeed * deltaTime;
        if (glfwGetKey(window, GLFW_KEY_UP) == GLFW_PRESS ||
            glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
            rectY += moveSpeed * deltaTime;
        if (glfwGetKey(window, GLFW_KEY_DOWN) == GLFW_PRESS ||
            glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
            rectY -= moveSpeed * deltaTime;

        // Clamp to screen edges
        rectX = glm::clamp(rectX, -1.0f + rectW, 1.0f - rectW);
        rectY = glm::clamp(rectY, -1.0f + rectH, 1.0f - rectH);

        // --- Mouse: check if cursor is over the rectangle ---
        {
            double mx, my;
            glfwGetCursorPos(window, &mx, &my);

            // Get framebuffer size for accurate coordinate mapping
            int fbW, fbH;
            glfwGetFramebufferSize(window, &fbW, &fbH);

            // Get window size
            int wW, wH;
            glfwGetWindowSize(window, &wW, &wH);

            // Convert pixel coords to NDC
            float ndcX = (float)(mx / wW) * 2.0f - 1.0f;
            float ndcY = 1.0f - (float)(my / wH) * 2.0f; // flip Y

            // Check AABB (axis-aligned bounding box, ignoring rotation for simplicity)
            mouseHovering = (ndcX >= rectX - rectW && ndcX <= rectX + rectW &&
                             ndcY >= rectY - rectH && ndcY <= rectY + rectH);
        }

        // Rotate when hovering
        if (mouseHovering) {
            rotationAngle += deltaTime * 120.0f; // 120 deg/sec
        }

        // --- Render ---
        glClear(GL_COLOR_BUFFER_BIT);
        glUseProgram(shaderProgram);
        glBindVertexArray(VAO);

        glm::mat4 model = glm::mat4(1.0f);
        model = glm::translate(model, glm::vec3(rectX, rectY, 0.0f));
        model = glm::rotate(model, glm::radians(rotationAngle), glm::vec3(0.0f, 0.0f, 1.0f));
        model = glm::scale(model, glm::vec3(rectW * 2.0f, rectH * 2.0f, 1.0f));

        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(model));
        glBindTexture(GL_TEXTURE_2D, tex);
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteBuffers(1, &EBO);
    glDeleteTextures(1, &tex);
    glDeleteProgram(shaderProgram);

    glfwTerminate();
    return 0;
}
