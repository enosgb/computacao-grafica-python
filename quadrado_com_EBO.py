import sys
import glm # Versão em Python da OpenGL Mathematics (GLM)
import OpenGL.GL as gl # Funcoes da API OpenGL
import OpenGL.GLUT as glut # Criacao de janelas acesso ao teclado


# Variáveis globais
shaderProgram = None
VBO = None # Vertex Buffer Object
VAO = None # Vertex Array Object
EBO = None # Element Buffer Object
cor = 5
mudar_cor_loc = None # Variavel uniform para mudar cor quadrado


vertex_shader_codigo= """
#version 330 core
in vec3 vPos;
void main()
{
    gl_Position = vec4(vPos.x, vPos.y, vPos.z, 1.0f);
}
"""

fragment_shader_codigo= """
#version 330
out vec4 FragColor;
uniform int muda_cor;
void main()
{
    if (muda_cor == 0){
       FragColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
    }
    else{
        if (muda_cor == 1){
           FragColor = vec4(0.0f, 0.0f, 1.0f, 1.0f);
        }
        else{
           FragColor = vec4(0.0f, 1.0f, 0.2f, 1.0f);
        }
    }
    
}
"""

def create_shader_program():
    """
    Compila os códigos fontes dos shaders e 
    armazena o programa shader compilado 
    na variável global shaderProgram.
    """
    global shaderProgram
    global vertex_shader_codigo
    global fragment_shader_codigo

    # Compilar vertex shader
    vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER) # Cria objeto shader do tipo GL_VERTEX_SHADER
    gl.glShaderSource(vertexShader, vertex_shader_codigo) # Associa o código fonte ao objeto
    gl.glCompileShader(vertexShader) # Compila o shader

    status = gl.glGetShaderiv(vertexShader, gl.GL_COMPILE_STATUS) # verifica se houve erro na compilação
    if status == gl.GL_FALSE:
        raise RuntimeError("Falha na compilação do shader:" + gl.glGetShaderInfoLog(vertexShader).decode('utf-8'))

    # Compilar fragment shader
    fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    gl.glShaderSource(fragmentShader, fragment_shader_codigo)
    gl.glCompileShader(fragmentShader)

    status = gl.glGetShaderiv(fragmentShader, gl.GL_COMPILE_STATUS)
    if status == gl.GL_FALSE:
        raise RuntimeError("Falha na compilação do shader:" + gl.glGetShaderInfoLog(fragmentShader).decode('utf-8'))

    shaderProgram = gl.glCreateProgram()

    gl.glAttachShader(shaderProgram, vertexShader)
    gl.glAttachShader(shaderProgram, fragmentShader)
    
    gl.glLinkProgram(shaderProgram)
    status = gl.glGetProgramiv(shaderProgram, gl.GL_LINK_STATUS)
    
    if status == gl.GL_FALSE:
        raise RuntimeError("Falha na etapa de link do shader:" + gl.glGetShaderInfoLog(shaderProgram).decode('utf-8'))

    gl.glDeleteShader(vertexShader)  
    gl.glDeleteShader(fragmentShader) 

    # Localizacao da variavel Uniform muda_cor no fragment shader
    global mudar_cor_loc
    mudar_cor_loc = gl.glGetUniformLocation(shaderProgram, "muda_cor")
        

def create_data_vertices():
    
    # Vertices do quadrado
    A = glm.vec3(0.5, 0.5, 0.0) # direita acima
    B = glm.vec3(0.5, -0.5, 0.0) # direita abaixo
    C = glm.vec3(-0.5, -0.5, 0.0) # esquerda abaixo 
    D = glm.vec3(-0.5, 0.5, 0.0) # esquerda acima 
    quadrado = glm.mat4x3(A, B, C, D) 
    return quadrado


def create_data_indexes():
    triangulo1_idx = glm.ivec3(0, 1, 3)
    triangulo2_idx = glm.ivec3(1, 2, 3)
    idxs = glm.i32mat2x3(triangulo1_idx, triangulo2_idx)
    return idxs


def create_buffers(data_to_buffer, idxs_to_buffer):

    global VAO
    global VBO 
    global EBO

    VAO = gl.glGenVertexArrays(1)
    VBO = gl.glGenBuffers(1)
    EBO = gl.glGenBuffers(1)

    # === Dados acessados via VAO == #
    gl.glBindVertexArray(VAO) # Array com ponteiros para os dados do VBO

    # Copia os dados para o VBO
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO) # Efetua o bind do VBO
    gl.glBufferData(target=gl.GL_ARRAY_BUFFER, size= glm.sizeof(data_to_buffer), data=glm.value_ptr(data_to_buffer), usage=gl.GL_STATIC_DRAW)

    # Copia os índices referentes aos dados EBO
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
    gl.glBufferData(target=gl.GL_ELEMENT_ARRAY_BUFFER, size= glm.sizeof(idxs_to_buffer), data=glm.value_ptr(idxs_to_buffer), usage=gl.GL_STATIC_DRAW)

    local_vPos = gl.glGetAttribLocation(shaderProgram, 'vPos')

    vertexDim = 3 # Quantidade de posições em vPos (Vertex Shader), que são 3 pois é do tipo vec3
    stride = 0 # Espaço entre os dados (i.e. cada vértice)
    offset = None # Onde os dados iniciam no Vertex Buffer
    # Descreve a forma de organização dos dados dentro do último buffer (VBO) vinculado (glBindBuffer)
    gl.glVertexAttribPointer(local_vPos, vertexDim, gl.GL_FLOAT, gl.GL_FALSE, stride, offset) 
    gl.glEnableVertexAttribArray(local_vPos) # Associa e habilita os dados do Vertex Buffer (VBO) no Array
    # ============================== #


    # Desvincula o VAO, VBO e location
    gl.glBindVertexArray(0) # Importante: Unbind do VAO primeiro
    gl.glDisableVertexAttribArray(local_vPos)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0) 


def display():

    gl.glClearColor(0.5, 0.5, 0.5, 1.0)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    gl.glUseProgram(shaderProgram)
    gl.glBindVertexArray(VAO) # Chamada ao VAO

    gl.glUniform1i(mudar_cor_loc, cor)

    quant = 6 # 3 índices de vertices do triangulo 1 + 3 indíces vertices do triangulo 2
    # Chamada do OpenGL para desenhar usando os índices
    gl.glDrawElements(gl.GL_TRIANGLES, quant, gl.GL_UNSIGNED_INT, None) 

    gl.glBindVertexArray(0) # Desvincula o VAO
    gl.glUseProgram(0) # Desvincula o Shader Program


    glut.glutSwapBuffers()


def reshape(width,height):

    gl.glViewport(0, 0, width, height)


def keyboard( key, x, y ):

    print("TECLA PRESSIONADA: {}".format(key))

    global cor

    if key == b'a':
        cor = 1
        display()
        
    if key == b'v':
        cor = 0
        display()

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
    glut.glutCreateWindow('Quadrado com EBO')

    # Inicialização
    create_shader_program()
    quadrado_vertices = create_data_vertices() # Especifica os dados da geometria
    quadrado_indices = create_data_indexes() # Especifica os índices dos dados da geometria
    create_buffers(data_to_buffer=quadrado_vertices, idxs_to_buffer=quadrado_indices)

    # Chama funcoes Callback
    glut.glutReshapeFunc(reshape)
    glut.glutDisplayFunc(display)
    glut.glutKeyboardFunc(keyboard)

    print("Fornecedor do Driver: {}".format(gl.glGetString(gl.GL_VENDOR).decode()))
    print("Hardware Video: {}".format(gl.glGetString(gl.GL_RENDERER).decode()))
    print("Versao do OpenGL: {}".format(gl.glGetString(gl.GL_VERSION).decode()))

    glut.glutMainLoop()


if __name__ == '__main__':
    print("\QUADRADO 2D : USANDO EBO")

    main_opengl()