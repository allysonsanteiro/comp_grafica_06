import cv2

img = cv2.imread("D:\Allyson\\ComputacaoGrafica\\aula0909\\dantedmc5.jpg")

# Rotação 90 graus
rot90 = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

# Rotação 45 graus em torno do centro
(h, w) = img.shape[:2]
centro = (w//2, h//2)
matriz = cv2.getRotationMatrix2D(centro, 45, 1.0)
rot45 = cv2.warpAffine(img, matriz, (w, h))

cv2.imshow("Original", img)
cv2.imshow("90 graus", rot90)
cv2.imshow("45 graus", rot45)
cv2.waitKey(0)
cv2.destroyAllWindows()