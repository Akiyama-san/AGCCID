from PIL import Image
from PIL import ImageOps
from pylab import (
    array,
    histogram
)
import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def plot_hist(original, nova):
    fig = plt.figure()
    fig.suptitle('Histogramas')
    gs = gridspec.GridSpec(1, 2)
    hist_original = plt.subplot(gs[0, 0])
    hist_nova = plt.subplot(gs[0, 1])

    hist_original.set_xlim(0, 255)
    hist_nova.set_xlim(0, 255)
    hist_original.set_title('Imagem Original')
    hist_nova.set_title('Imagem Melhorada')

    fig.add_subplot(hist_original)
    fig.add_subplot(hist_nova)
    hist_original.hist(array(original.convert('L')))
    hist_nova.hist(array(nova.convert('L')))
    plt.ion()
    plt.show()


# Parser para os argumentos da linha de comando
parser = argparse.ArgumentParser(description='AGGCID')

parser.add_argument('filename', metavar='FILE', type=str,
                    help='Nome do arquivo')
parser.add_argument('-i', dest='invert', action='store_true', help='inverter')
parser.add_argument('-a', dest='alfa', metavar='ALFA', type=float, default=0.5,
                    help='alfa (padrao 0.5)')

args = parser.parse_args()

# Abre a imagem em RGB
imagem = Image.open(args.filename).convert('RGB')
# Mostra a imagem
imagem.show()

# Inverte a imagem para realizar realce para imagem clara
if(args.invert):
    inverted_image = ImageOps.invert(imagem)
    imagem = inverted_image

# Converte imagem para array
img = array(imagem)

# Separar os 3 canais
r = img[:, :, 0]
g = img[:, :, 1]
b = img[:, :, 2]

# Gera o histograma com 256 niveis
pdf_r, niveis = histogram(r.flatten(), 256, (0, 256))
pdf_g, niveis = histogram(g.flatten(), 256, (0, 256))
pdf_b, niveis = histogram(b.flatten(), 256, (0, 256))
niveis = range(256)

# Calcula as probabilidades com peso
pdfw_r = []
pdfw_g = []
pdfw_b = []
alfa = args.alfa
for i in niveis:
    pdfw_r.append(
        pow((float(pdf_r[i])-pdf_r.min())/(pdf_r.max()-pdf_r.min()), alfa) *
        pdf_r.max())
    pdfw_g.append(
        pow((float(pdf_g[i])-pdf_g.min())/(pdf_g.max()-pdf_g.min()), alfa) *
        pdf_g.max())
    pdfw_b.append(
        pow((float(pdf_b[i])-pdf_b.min())/(pdf_b.max()-pdf_b.min()), alfa) *
        pdf_b.max())

# Calcula CDFw
cdfw_r = []
cdfw_g = []
cdfw_b = []
sum_pdfw_r = sum(pdfw_r)
sum_pdfw_g = sum(pdfw_g)
sum_pdfw_b = sum(pdfw_b)
for i in niveis:
    c_r = 0
    c_g = 0
    c_b = 0
    for j in range(i+1):
        c_r += pdfw_r[j]/sum_pdfw_r
        c_g += pdfw_g[j]/sum_pdfw_g
        c_b += pdfw_b[j]/sum_pdfw_b
    cdfw_r.append(c_r)
    cdfw_g.append(c_g)
    cdfw_b.append(c_b)

# Calcula os novos niveis
novo_nivel_r = []
novo_nivel_g = []
novo_nivel_b = []
for i in niveis:
    novo_nivel_r.append(pow((float(i)/255), (1-float(cdfw_r[i])))*255)
    novo_nivel_g.append(pow((float(i)/255), (1-float(cdfw_g[i])))*255)
    novo_nivel_b.append(pow((float(i)/255), (1-float(cdfw_b[i])))*255)

# Edita a imagem
m, n = r.shape
for i in range(m):
    for j in range(n):
        r[i][j] = novo_nivel_r[r[i][j]]
        g[i][j] = novo_nivel_g[g[i][j]]
        b[i][j] = novo_nivel_b[b[i][j]]

# Cria nova imagem
img2 = np.empty(img.shape, dtype=np.uint8)
img2[:, :, 0] = r
img2[:, :, 1] = g
img2[:, :, 2] = b

# Mostra nova imagem
imagem2 = Image.fromarray(img2)

if(args.invert):
    ImageOps.invert(imagem2).show()
    plot_hist(ImageOps.invert(imagem), ImageOps.invert(imagem2))
else:
    imagem2.show()
    plot_hist(imagem, imagem2)

raw_input("Press Enter to continue...")
