import sys
import glm # Versão em Python da OpenGL Mathematics (GLM)
import OpenGL.GL as gl # Funcoes da API OpenGL
import OpenGL.GLUT as glut # Criacao de janelas acesso ao teclado
import numpy as np


# Variáveis globais
shaderProgramRef = None


#Shaders escritos na linguagem GLSL
vertex_shader_codigo= """
in vec3 position;
void main()
{
    gl_Position = vec4(position.x, position.y, position.z, 1.0f);
}
"""

fragment_shader_codigo= """
out vec4 FragColor;
uniform int muda_cor;
void main()
{
    if(muda_cor == 0){
        FragColor = vec4(0.92f, 0.10f, 0.14f,1.0f);
    }else{
        FragColor = vec4(1.0f, 1.0f, 0.0f, 1.0f);
    }
}
"""
        
def create_triangulo_vertices():
    '''
    Vertices para desenhar Triangulo
    '''
    lista_vertices = [
        [ -0.5,  -0.5,  0.0], # esquerda embaixo
        [ 0.5,  -0.5,  0.0], # direita embaixo
        [0.0,  0.5,  0.0] # centro cima
    ]

    vertices = np.array(lista_vertices, dtype=np.float32)
    quant_vertices = len(vertices)
    #print("quant_vertices: {}".format(quant_vertices))
    
    return vertices, quant_vertices

def create_square_vertices():
    '''
    Vertices para desenhar quadrado
    '''
    lista_vertices = [
        [0.5, 0.5, 0.0],
        [0.5, -0.5, 0.0],
        [-0.5, -0.5, 0.0],
        [-0.5, 0.5, 0.0]
    ]

    vertices = np.array(lista_vertices, dtype=np.float32)
    quant_vertices = len(vertices)
    #print("quant_vertices: {}".format(quant_vertices))
    
    return vertices, quant_vertices


def refer_to_var_program( program_ref, var_in_program, var_data_type, vbo_ref):
    '''
    '''

    # Retornar uma referencia para variavel no shader ( com qualificador in ) 
    var_ref = gl.glGetAttribLocation( program_ref, var_in_program)

    # Se a variavel nao foi encontrada no shader
    if var_ref == -1:
        raise Exception(f'\n\nErro Shader : Variavel {var_in_program} nao encontrada no shader.\n')

    if var_ref != -1:
        # Seleciona o Buffer
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo_ref)

        # Configura como os dados serao lidos do buffer atual e armazenados na variavel do shader
        # glVertexAttribPointer esta associando ao VAO (chamado anteriormete) o VBO com a variavel do shader, 
        # i.e., ao VAO ativo no momento.
        if var_data_type == "int":
            gl.glVertexAttribPointer(var_ref, 1, gl.GL_INT, False, 0, None) # var_ref recebe dados do VBO ativo
        elif var_data_type == "float":
            gl.glVertexAttribPointer(var_ref, 1, gl.GL_FLOAT, False, 0, None)
        elif var_data_type == "vec2":
            gl.glVertexAttribPointer(var_ref, 2, gl.GL_FLOAT, False, 0, None)
        elif var_data_type == "vec3":
            gl.glVertexAttribPointer(var_ref, 3, gl.GL_FLOAT, False, 0, None)
        elif var_data_type == "vec4":
            gl.glVertexAttribPointer(var_ref, 4, gl.GL_FLOAT, False, 0, None)
        else:
            raise Exception(f'\n\nErro Shader : Variavel {var_in_program} com tipo desconhecido = {var_data_type}.\n')
        
        # Dados no VBO atual associados a variavel no shader 
        # serao utilizados no processo de renderizacao
        gl.glEnableVertexAttribArray(var_ref)


def data_buffer(data_to_buffer, program_ref, var_in_program, var_data_type):
    '''
    Observacao:
        data_to_buffer: pode ser atualizada caso os vertices sejam alterados.
        Nesse caso esta funcao pode ser chamada novamente.
    '''

    # Converte os dados para numpy com float de 32 bits
    data = np.array(data_to_buffer).astype(np.float32)

    # Retorna um conjunto de referências de vertex buffer (VBO) disponivel na GPU
    VertexBufferObject = gl.glGenBuffers(1)
   
    # Cria buffer (VBO) 
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VertexBufferObject)

    # Armazena os dados no buffer atualmente vinculado (usando numpy)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, data.ravel(), gl.GL_STATIC_DRAW)
    # # Armazena os dados no buffer atualmente vinculado (usando GLM)
    # gl.glBufferData(target=gl.GL_ARRAY_BUFFER, size= glm.sizeof(data), data=glm.value_ptr(data), usage=gl.GL_STATIC_DRAW)

    refer_to_var_program(program_ref, var_in_program, var_data_type, VertexBufferObject)

def draw_triangulo(shaderProgramRef):
    '''
    '''
    # Seleciona o shader program para renderizar as geometrias
    gl.glUseProgram(shaderProgramRef)

    # Cria um objeto Buffer (VAO)
    # Enquanto este VAO estiver ativo ele armazena informações que incluem 
    # as associações entre vertex buffers (VBO) e variáveis de atributo dentro do shader program, 
    # assim como a organização dos dados dentro do buffer.
    VertexArrayObject = gl.glGenVertexArrays(1) # Cria ID para objeto OpenGL VAO
    gl.glBindVertexArray(VertexArrayObject) # Vincula objeto OpenGL VAO

    # Especifica os dados da geometria
    data_vertices, quant_vert =  create_triangulo_vertices()

    # Associa a variavel especificada no shader com os dados da geometria no buffer 
    data_buffer(data_to_buffer=data_vertices, program_ref=shaderProgramRef, var_in_program='position', var_data_type='vec3')

    gl.glDrawArrays(gl.GL_TRIANGLES, 0, quant_vert)

    return VertexArrayObject, quant_vert

def draw_square(shaderProgramRef):
    '''
    '''

    # Seleciona o shader program para renderizar as geometrias
    gl.glUseProgram(shaderProgramRef)

    # Cria um objeto Buffer (VAO)
    # Enquanto este VAO estiver ativo ele armazena informações que incluem 
    # as associações entre vertex buffers (VBO) e variáveis de atributo dentro do shader program, 
    # assim como a organização dos dados dentro do buffer.
    VertexArrayObject = gl.glGenVertexArrays(1) # Cria ID para objeto OpenGL VAO
    gl.glBindVertexArray(VertexArrayObject) # Vincula objeto OpenGL VAO

    # Especifica os dados da geometria
    data_vertices, quant_vert = create_square_vertices()

    # Associa a variavel especificada no shader com os dados da geometria no buffer VBO
    data_buffer(data_to_buffer=data_vertices, program_ref=shaderProgramRef, var_in_program='position', var_data_type='vec3')

    gl.glDrawArrays(gl.GL_LINE_LOOP, 0, quant_vert)

    return VertexArrayObject, quant_vert

def display():

    gl.glClearColor(0.5, 0.5, 0.5,0.5)
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    draw_square(shaderProgramRef)
    draw_triangulo(shaderProgramRef)

    glut.glutSwapBuffers()


def reshape(width,height):
    gl.glViewport(0, 0, width, height)


def keyboard( key, x, y ):
    print("TECLA PRESSIONADA: {}".format(key))
    if key == b'\x1b': # ESC
        sys.exit( ) 

def init_shader(codigo_shader, tipo_shader, glsl_version_str = '#version 330\n'): 

    # glsl_version_str = '#version 330\n'
    codigo_shader = glsl_version_str + codigo_shader

    # Compilar vertex shader
    shader_object = gl.glCreateShader(tipo_shader) # Cria objeto shader do tipo GL_VERTEX_SHADER
    gl.glShaderSource(shader_object, codigo_shader) # Associa o código fonte ao objeto
    gl.glCompileShader(shader_object) # Compila o shader

    sucesso_compilacao = gl.glGetShaderiv(shader_object, gl.GL_COMPILE_STATUS)

    if not sucesso_compilacao:
        mensagem_erro = gl.glGetShaderInfoLog(shader_object).decode('utf-8')
        gl.glDeleteShader(shader_object)  
        raise RuntimeError(mensagem_erro)
    
    return shader_object

def init_shader_program(vertex_shader_codigo, fragment_shader_codigo):

    vertex_shader_object = init_shader(vertex_shader_codigo, gl.GL_VERTEX_SHADER)
    fragment_shader_object = init_shader(fragment_shader_codigo, gl.GL_FRAGMENT_SHADER)

    shaderProgram = gl.glCreateProgram()

    gl.glAttachShader(shaderProgram, vertex_shader_object)
    gl.glAttachShader(shaderProgram, fragment_shader_object)
    
    gl.glLinkProgram(shaderProgram)

    sucesso_linking = gl.glGetProgramiv(shaderProgram, gl.GL_LINK_STATUS)

    if not sucesso_linking:
        mensagem_erro = gl.glGetProgramInfoLog(shaderProgram).decode('utf-8')
        gl.glDeleteProgram(shaderProgram)  
        raise RuntimeError(mensagem_erro)
    
    return shaderProgram


def init_window(title_str, largura, altura):
    
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGBA)
    glut.glutInitWindowSize(largura, altura)
    glut.glutCreateWindow(title_str)

def main_opengl(titulo_janela):
    print(" ==== main_opengl ====")

    init_window(titulo_janela, 400, 400)

    glut.glutReshapeFunc(reshape)
    glut.glutDisplayFunc(display)
    glut.glutKeyboardFunc(keyboard)

    global shaderProgramRef 
    # Compila os shaders
    shaderProgramRef = init_shader_program(vertex_shader_codigo, fragment_shader_codigo)

    glut.glutMainLoop()

if __name__ == '__main__':

    titulo_janela = 'HEXAGONO'
    print("\n")
    print(titulo_janela)
    print("\n")

    main_opengl(titulo_janela)