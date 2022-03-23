import sys
import glm # Versão em Python da OpenGL Mathematics (GLM)
import OpenGL.GL as gl # Funcoes da API OpenGL
import OpenGL.GLUT as glut # Criacao de janelas acesso ao teclado


# Variáveis globais
shaderProgramFrag1 = None
shaderProgramFrag2 = None
VBO = [None, None] # Vertex Buffer Object
VAO = [None, None] # Vertex Array Object

vertex_shader_codigo= """
#version 330 core
in vec3 vPos;
void main()
{
    gl_Position = vec4(vPos.x, vPos.y, vPos.z, 1.0f);
}
"""

fragment_shader_codigo_1= """
#version 330 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
"""

fragment_shader_codigo_2= """
#version 330 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0f, 1.0f, 0.0f, 1.0f);
}
"""

def create_data_triangulo_1():
    
    # Vertices do triangulo
    v1 = glm.vec3(-0.9, -0.5, 0.0) # esquerda abaixo
    v2 = glm.vec3(0.0, -0.5, 0.0) # meio abaixo
    v3 = glm.vec3(-0.45, 0.5, 0.0) # esquerda acima 
    tri = glm.mat3(v1, v2, v3) 
    return tri


def create_data_triangulo_2():
    
    # Vertices do triangulo
    v1 = glm.vec3(0.0, -0.5, 0.0) # 
    v2 = glm.vec3(0.9, -0.5, 0.0) # 
    v3 = glm.vec3(0.45, 0.5, 0.0) # 
    tri = glm.mat3(v1, v2, v3) 
    return tri


def create_buffers(data_t1, data_t2):

    global VAO
    global VBO 

    VAO[0] = gl.glGenVertexArrays(1) 
    VAO[1] = gl.glGenVertexArrays(1) 
    VBO[0] = gl.glGenBuffers(1) 
    VBO[1] = gl.glGenBuffers(1)

    # Triangulo 1
    gl.glBindVertexArray(VAO[0])
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO[0]) # Efetua o bind do VBO
    gl.glBufferData(target=gl.GL_ARRAY_BUFFER, size= glm.sizeof(data_t1), data=glm.value_ptr(data_t1), usage=gl.GL_STATIC_DRAW)
    local = gl.glGetAttribLocation(shaderProgramFrag1, 'vPos')
    vertexDim = 3 # quantidade de elementos do vetor declarado no shader
    stride = 0 # Espaço em bytes até o próximo valor. E.g. próximo x, quando for posição (X | Y | Z | X | Y | ...)
    offset = None # Onde os dados iniciam no Vertex Buffer
    # Descreve a forma de organização dos dados dentro do último buffer (VBO) vinculado (glBindBuffer)
    gl.glVertexAttribPointer(local, vertexDim, gl.GL_FLOAT, gl.GL_FALSE, stride, offset) 
    gl.glEnableVertexAttribArray(local) # Associa e habilita os dados do Vertex Buffer (VBO) no Array

    # Desvincula o VAO, VBO
    gl.glBindVertexArray(0) # Importante: Unbind do VAO primeiro
    gl.glDisableVertexAttribArray(local)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0) 

    # Triangulo 2
    gl.glBindVertexArray(VAO[1])
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO[1]) # Efetua o bind do VBO
    gl.glBufferData(target=gl.GL_ARRAY_BUFFER, size= glm.sizeof(data_t2), data=glm.value_ptr(data_t2), usage=gl.GL_STATIC_DRAW)
    local = gl.glGetAttribLocation(shaderProgramFrag2, 'vPos')
    vertexDim = 3 # quantidade de elementos do vetor declarado no shader
    stride = 0 # Espaço em bytes até o próximo valor. E.g. próximo x, quando for posição (X | Y | Z | X | Y | ...)
    offset = None # Onde os dados iniciam no Vertex Buffer
    # Descreve a forma de organização dos dados dentro do último buffer (VBO) vinculado (glBindBuffer)
    gl.glVertexAttribPointer(local, vertexDim, gl.GL_FLOAT, gl.GL_FALSE, stride, offset) 
    gl.glEnableVertexAttribArray(local) # Associa e habilita os dados do Vertex Buffer (VBO) no Array

    # Desvincula o VAO, VBO
    gl.glBindVertexArray(0) # Importante: Unbind do VAO primeiro
    gl.glDisableVertexAttribArray(local)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0) 


def create_shader_program():
    """
    Compila os códigos fontes dos shaders e 
    armazena o programa shader compilado 
    na variável global shaderProgram.
    """
    global shaderProgramFrag1
    global shaderProgramFrag2
    global vertex_shader_codigo
    global fragment_shader_codigo_1
    global fragment_shader_codigo_2

    # Compilar vertex shader
    vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER) # Cria objeto shader do tipo GL_VERTEX_SHADER
    gl.glShaderSource(vertexShader, vertex_shader_codigo) # Associa o código fonte ao objeto
    gl.glCompileShader(vertexShader) # Compila o shader

    status = gl.glGetShaderiv(vertexShader, gl.GL_COMPILE_STATUS) # verifica se houve erro na compilação
    if status == gl.GL_FALSE:
        raise RuntimeError("Falha na compilação do shader:" + gl.glGetShaderInfoLog(vertexShader).decode('utf-8'))

    # Compilar fragment shader
    fragmentShader1 = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(fragmentShader1, fragment_shader_codigo_1)
    gl.glCompileShader(fragmentShader1)

    status = gl.glGetShaderiv(fragmentShader1, gl.GL_COMPILE_STATUS)
    if status == gl.GL_FALSE:
        raise RuntimeError("Falha na compilação do shader:" + gl.glGetShaderInfoLog(fragmentShader1).decode('utf-8'))

    # Compilar fragment shader
    fragmentShader2 = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(fragmentShader2, fragment_shader_codigo_2)
    gl.glCompileShader(fragmentShader2)

    status = gl.glGetShaderiv(fragmentShader2, gl.GL_COMPILE_STATUS)
    if status == gl.GL_FALSE:
        raise RuntimeError("Falha na compilação do shader:" + gl.glGetShaderInfoLog(fragmentShader2).decode('utf-8'))

    # Cria um shader program para cada fragment shader
    shaderProgramFrag1 = gl.glCreateProgram()
    shaderProgramFrag2 = gl.glCreateProgram()

    # Fragment Shader 1
    gl.glAttachShader(shaderProgramFrag1, vertexShader)
    gl.glAttachShader(shaderProgramFrag1, fragmentShader1)
    
    gl.glLinkProgram(shaderProgramFrag1)
    status = gl.glGetProgramiv(shaderProgramFrag1, gl.GL_LINK_STATUS)
    
    if status == gl.GL_FALSE:
        raise RuntimeError("Falha na etapa de link do shader:" + gl.glGetShaderInfoLog(shaderProgramFrag1).decode('utf-8'))

    # Fragment Shader 2
    gl.glAttachShader(shaderProgramFrag2, vertexShader) 
    gl.glAttachShader(shaderProgramFrag2, fragmentShader2)
    
    gl.glLinkProgram(shaderProgramFrag2)
    status = gl.glGetProgramiv(shaderProgramFrag2, gl.GL_LINK_STATUS)
    
    if status == gl.GL_FALSE:
        raise RuntimeError("Falha na etapa de link do shader:" + gl.glGetShaderInfoLog(shaderProgramFrag2).decode('utf-8'))

    gl.glDeleteShader(vertexShader)  
    gl.glDeleteShader(fragmentShader1) 
    gl.glDeleteShader(fragmentShader2) 


def display():

    gl.glClearColor(0.5, 0.5, 0.5, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    # Triangulo 1
    gl.glUseProgram(shaderProgramFrag1)
    gl.glBindVertexArray(VAO[0])
    quant_vertices = 3 
    gl.glDrawArrays(gl.GL_TRIANGLES, 0, quant_vertices)
    gl.glBindVertexArray(0) # Desvincula o VAO
    gl.glUseProgram(0) # Desvincula o Shader Program

    
    # Triangulo 2
    gl.glUseProgram(shaderProgramFrag2)
    gl.glBindVertexArray(VAO[1])
    quant_vertices = 3 
    gl.glDrawArrays(gl.GL_TRIANGLES, 0, quant_vertices)
    gl.glBindVertexArray(0) # Desvincula o VAO
    gl.glUseProgram(0) # Desvincula o Shader Program

    glut.glutSwapBuffers()


def reshape(width,height):

    gl.glViewport(0, 0, width, height)


def keyboard( key, x, y ):

    print("TECLA PRESSIONADA: {}".format(key))

    if key == b'\x1b': # ESC
        sys.exit( )  

def main_opengl():
    print(" ==== main_opengl ====")

    # Cria contexto OpenGL e configura janela
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
    largura = 400
    altura = 400
    glut.glutInitWindowSize(largura, altura)
    glut.glutCreateWindow('Dois Triangulos')

    # Inicialização
    create_shader_program()
    t1 = create_data_triangulo_1()
    t2 = create_data_triangulo_2()
    create_buffers(data_t1=t1, data_t2=t2)
    
    # Chama funcoes Callback
    glut.glutReshapeFunc(reshape)
    glut.glutDisplayFunc(display)
    glut.glutKeyboardFunc(keyboard)

    print("Fornecedor do Driver: {}".format(gl.glGetString(gl.GL_VENDOR).decode()))
    print("Hardware Video: {}".format(gl.glGetString(gl.GL_RENDERER).decode()))
    print("Versao do OpenGL: {}".format(gl.glGetString(gl.GL_VERSION).decode()))

    glut.glutMainLoop()


if __name__ == '__main__':
    print("\nDOIS TRIANGULOS")

    main_opengl()