import cv2           #Importa a biblioteca OpenCV, usada para janelas, eventos e desenho.
import numpy as np   #Importa a biblioteca NumPy, para criar/manipular arrays (a imagem/canvas).

WIDTH, HEIGHT = 960, 540     #Define a largura e a altura do canvas (960 x 540 pixels).

canvas = np.ones((HEIGHT, WIDTH, 3), dtype=np.uint8) * 255  #Cria uma imagem branca (altura x largura x 3 canais BGR) preenchida com 255.

mode = "line"        #Seta o modo inicial como 'line' (desenhar linhas).
drawing = False      #Flag booleana que indica se o botão esquerdo do mouse está pressionado.
start_pt = None      #Ponto inicial (x, y) do gesto de desenho; começa sem valor.
curr_pt = None       #Ponto corrente (x, y) do mouse usado para pré-visualização; começa sem valor.

def put_help(img):                 #Define a função que desenha uma barra de ajuda com atalhos no topo da imagem.
    """-----"""                    #Docstring da função (aqui é apenas um marcador/placeholder).
    txt = "Teclas: [1]Linha  [2]Ret  [3]Circ  [4]Livre  |  [c] limpar  [s] salvar  [ESC] sair"  #Texto com os atalhos que será exibido na barra de ajuda.
    cv2.rectangle(img, (0, 0), (WIDTH, 30), (240, 240, 240), -1)                              #Desenha um retângulo cinza claro no topo (0,0)-(WIDTH,30) como barra de ajuda.
    cv2.putText(img, txt, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 1, cv2.LINE_AA)     #Escreve o texto de atalhos sobre a barra de ajuda (fonte, tamanho, cor).

def mouse_cb(event, x, y, flags, param):    #Define o callback de mouse, chamado pela janela a cada evento do mouse.
    """Controla o desenho com o mouse."""   #Docstring:               #explica que esta função controla o desenho via mouse.
    global drawing, start_pt, curr_pt, canvas, mode      #Declara que a função vai modificar variáveis globais (estado do desenho e do canvas).

    if event == cv2.EVENT_LBUTTONDOWN:    #Quando o botão esquerdo é pressionado: inicia um gesto de desenho.
        drawing = True      #Flag booleana que indica se o botão esquerdo do mouse está pressionado.
        start_pt = (x, y)   #Linha de código executada conforme o contexto acima.
        curr_pt = (x, y)    #Atualiza o ponto corrente do mouse com as coordenadas (x, y).

    elif event == cv2.EVENT_MOUSEMOVE:      #Quando o mouse se move: atualiza a posição corrente e, se necessário, des
        curr_pt = (x, y)                    #Atualiza o ponto corrente do mouse com as coordenadas (x, y).

        if drawing and mode == "free":          #Se estiver desenhando no modo 'free', desenha um traço contínuo no canvas.
            cv2.line(canvas, start_pt, curr_pt, (50, 50, 50), 2)   # Desenha uma linha no canvas do ponto anterior ao ponto atual (pincel simples).
            start_pt = curr_pt                  #avança o ponto inicial para continuar o traço. Atualiza o ponto inicial para a posição atual, permitindo um traço contínuo.
    elif event == cv2.EVENT_LBUTTONUP:      #Quando o botão esquerdo é solto: finaliza o gesto e fixa a forma.
        drawing = False             #Flag booleana que indica se o botão esquerdo do mouse está pressionado.

        if mode == "line":                        #Se o modo atual for linha: desenha a linha final no canvas (espessura 2).
            cv2.line(canvas, start_pt, (x, y), (0, 0, 255), 2)         #Linha de código executada conforme o contexto acima.
        elif mode == "rect":                      #Se o modo atual for retângulo: desenha o retângulo final no canvas.
            cv2.rectangle(canvas, start_pt, (x, y), (0, 128, 255), 2)    #Desenha um retângulo cinza claro no topo (0,0)-(WIDTH,30) como barra de ajuda.
        elif mode == "circle":                    #Se o modo atual for círculo: calcula o raio e desenha o círculo final no canvas.
            r = int(((x - start_pt[0])**2 + (y - start_pt[1])**2)**0.5)  #Calcula o raio como a distância euclidiana entre start_pt e o ponto atual.
            cv2.circle(canvas, start_pt, r, (0, 255, 0), 2)       #Desenha o círculo final com o raio calculado e cor verde.

cv2.namedWindow("Canvas", cv2.WINDOW_AUTOSIZE)    #Cria a janela chamada 'Canvas' com tamanho auto-ajustável.
cv2.setMouseCallback("Canvas", mouse_cb)          #Registra a função de callback do mouse para a janela 'Canvas'.

while True:
    # Loop principal da aplicação — roda até que o usuário saia (tecla ESC)

    display = canvas.copy()
    # Cria uma cópia do canvas para desenhar a pré-visualização sem alterar o desenho final

    if drawing and mode in ("line", "rect", "circle") and start_pt and curr_pt:
        # Se estiver desenhando em um dos modos com preview, desenha a forma na cópia 'display'

        if mode == "line":
            # Modo linha: desenha uma linha de pré-visualização (fina, vermelha)
            cv2.line(display, start_pt, curr_pt, (0, 0, 255), 1)

        elif mode == "rect":
            # Modo retângulo: desenha o retângulo de pré-visualização (laranja)
            cv2.rectangle(display, start_pt, curr_pt, (0, 128, 255), 1)

        elif mode == "circle":
            # Modo círculo: calcula o raio e desenha o círculo de pré-visualização (verde)
            r = int(((curr_pt[0] - start_pt[0])**2 + (curr_pt[1] - start_pt[1])**2)**0.5)
            cv2.circle(display, start_pt, r, (0, 255, 0), 1)

    put_help(display)
    # Desenha a barra de ajuda sobre a imagem que será exibida

    cv2.imshow("Canvas", display)
    # Mostra a imagem 'display' na janela 'Canvas'

    k = cv2.waitKey(20) & 0xFF
    # Espera ~20ms por uma tecla; lê o código da tecla pressionada (8 bits)

    if k == 27:
        # Tecla ESC: sai do loop (fecha o programa)
        break

    elif k == ord('c'):
        # Tecla 'c': limpa o canvas (pinta de branco)
        canvas[:] = 255

    elif k == ord('s'):
        # Tecla 's': salva a imagem atual do canvas
        cv2.imwrite("canvas_saida.png", canvas)
        print("Imagem salva em canvas_saida.png")

    elif k == ord('1'):
        # Tecla '1': muda para modo linha
        mode = "line"

    elif k == ord('2'):
        # Tecla '2': muda para modo retângulo
        mode = "rect"

    elif k == ord('3'):
        # Tecla '3': muda para modo círculo
        mode = "circle"

    elif k == ord('4'):
        # Tecla '4': muda para modo desenho livre (pincel)
        mode = "free"

cv2.destroyAllWindows()
# Fecha todas as janelas do OpenCV ao encerrar o programa







