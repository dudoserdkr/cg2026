//
// HW3 Part 1 — Three non-overlapping textured rectangles
// Created by Ivan Tiulpa
//
#include <iostream>
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

// Generate a striped texture
GLuint generateStripes(int size, int stripeWidth,
                       unsigned char r1, unsigned char g1, unsigned char b1,
                       unsigned char r2, unsigned char g2, unsigned char b2)
{
    unsigned char* data = new unsigned char[size * size * 3];
    for (int y = 0; y < size; y++) {
        for (int x = 0; x < size; x++) {
            bool stripe = (x / stripeWidth) % 2 == 0;
            int idx = (y * size + x) * 3;
            data[idx + 0] = stripe ? r1 : r2;
            data[idx + 1] = stripe ? g1 : g2;
            data[idx + 2] = stripe ? b1 : b2;
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

// Generate a gradient texture
GLuint generateGradient(int size,
                        unsigned char r1, unsigned char g1, unsigned char b1,
                        unsigned char r2, unsigned char g2, unsigned char b2)
{
    unsigned char* data = new unsigned char[size * size * 3];
    for (int y = 0; y < size; y++) {
        float t = (float)y / (float)(size - 1);
        for (int x = 0; x < size; x++) {
            int idx = (y * size + x) * 3;
            data[idx + 0] = (unsigned char)(r1 + t * (r2 - r1));
            data[idx + 1] = (unsigned char)(g1 + t * (g2 - g1));
            data[idx + 2] = (unsigned char)(b1 + t * (b2 - b1));
        }
    }
    GLuint tex;
    glGenTextures(1, &tex);
    glBindTexture(GL_TEXTURE_2D, tex);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
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

    GLFWwindow* window = glfwCreateWindow(800, 600, "HW3.1 - Textured Rectangles", NULL, NULL);
    if (!window) {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }

    glfwMakeContextCurrent(window);
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

    // ---------- quad data (unit quad centered at origin) ----------
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

    // ---------- generate 3 procedural textures ----------
    GLuint tex1 = generateCheckerboard(64, 8, 255, 60, 60, 255, 255, 255);
    GLuint tex2 = generateStripes(64, 8, 30, 60, 200, 100, 220, 255);
    GLuint tex3 = generateGradient(64, 30, 180, 30, 240, 240, 60);

    int modelLoc = glGetUniformLocation(shaderProgram, "model");

    glClearColor(0.12f, 0.12f, 0.14f, 1.0f);

    while (!glfwWindowShouldClose(window) && !glfwGetKey(window, GLFW_KEY_ESCAPE))
    {
        glClear(GL_COLOR_BUFFER_BIT);
        glUseProgram(shaderProgram);
        glBindVertexArray(VAO);

        // Rectangle 1 (top-left) — red/white checkerboard
        {
            glm::mat4 model = glm::mat4(1.0f);
            model = glm::translate(model, glm::vec3(-0.55f, 0.45f, 0.0f));
            model = glm::scale(model, glm::vec3(0.6f, 0.45f, 1.0f));
            glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(model));
            glBindTexture(GL_TEXTURE_2D, tex1);
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
        }

        // Rectangle 2 (top-right) — blue/cyan stripes
        {
            glm::mat4 model = glm::mat4(1.0f);
            model = glm::translate(model, glm::vec3(0.55f, 0.45f, 0.0f));
            model = glm::scale(model, glm::vec3(0.6f, 0.45f, 1.0f));
            glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(model));
            glBindTexture(GL_TEXTURE_2D, tex2);
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
        }

        // Rectangle 3 (bottom-center) — green-yellow gradient
        {
            glm::mat4 model = glm::mat4(1.0f);
            model = glm::translate(model, glm::vec3(0.0f, -0.35f, 0.0f));
            model = glm::scale(model, glm::vec3(0.7f, 0.45f, 1.0f));
            glUniformMatrix4fv(modelLoc, 1, GL_FALSE, glm::value_ptr(model));
            glBindTexture(GL_TEXTURE_2D, tex3);
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, 0);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glDeleteVertexArrays(1, &VAO);
    glDeleteBuffers(1, &VBO);
    glDeleteBuffers(1, &EBO);
    glDeleteTextures(1, &tex1);
    glDeleteTextures(1, &tex2);
    glDeleteTextures(1, &tex3);
    glDeleteProgram(shaderProgram);

    glfwTerminate();
    return 0;
}
