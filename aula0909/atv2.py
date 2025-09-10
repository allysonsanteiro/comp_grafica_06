import cv2
img = cv2.imread("D:\Allyson\\ComputacaoGrafica\\aula0909\\dantedmc5.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow("Colorida", img)
cv2.imshow("Cinza", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()