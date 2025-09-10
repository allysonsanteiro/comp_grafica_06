import cv2
import numpy as np

# Criar imagem em branco
img = np.zeros((500,500,3), dtype="uint8")

def desenhar(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (x,y), 20, (0,255,0), -1)

cv2.namedWindow("Desenho")
cv2.setMouseCallback("Desenho", desenhar)

while True:
    cv2.imshow("Desenho", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
