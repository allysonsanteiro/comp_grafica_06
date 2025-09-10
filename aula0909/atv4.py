import cv2
import numpy as np

# Criar imagem em branco (500x500 pixels, 3 canais de cor)
img = np.zeros((500, 500, 3), dtype="uint8")

# Desenhar formas
cv2.rectangle(img, (50,50), (200,200), (0,255,0), -1)  # Retângulo verde
cv2.circle(img, (300,300), 50, (255,0,0), -1)          # Círculo azul
cv2.line(img, (0,0), (500,500), (0,0,255), 5)          # Linha vermelha

# Texto
cv2.putText(img, "Meu Nome", (150,250), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

cv2.imshow("Desenho", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
