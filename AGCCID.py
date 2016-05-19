from PIL import Image
from pylab import *

#Abre e converte para grayscale
imagem = Image.open('low-contrast.jpg').convert('L')
imagem.show()

#Converte pra array
img = array(imagem)
#Gera o histograma com 255 divisoes
pdf, niveis = histogram(img.flatten(), 256, (0, 256))
niveis = range(256)

#print(pdf)

#Calcula as probabilidades com peso
pdfw = []
alfa = 0.5
for i in niveis:
    p = pow((float(pdf[i])-pdf.min())/(pdf.max()-pdf.min()), alfa)*pdf.max()
    pdfw.append(p)
#print(pdfw)

#Calcula CDFw
cdfw = []
for i in niveis:
    c = 0
    for j in range(i+1):
        c += pdfw[j]/sum(pdfw)
    cdfw.append(c)

#print(cdfw)

#Edita a imagem
m, n = img.shape
for i in range(m):
    for j in range(n):
        img[i][j] = pow((float(img[i][j])/255), (1-float(cdfw[img[i][j]])))*255

imagem2 = Image.fromarray(img)
imagem2.show()
#pdf, niveis = histogram(img.flatten(), 256, (0, 256))
#print(pdf)
