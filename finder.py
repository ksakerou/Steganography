from PIL import Image
from pplib import *
from info import *

#Открытие носителя
src = Image.open(encfile)
srcpx = src.load()


#Цикл по каждому пикселю
data16 = ""

for x in range(src.width):
    for y in range(src.height):
        tmp = rgb2hex(srcpx[x,y])
        data16 = data16 + tmp[5] 


data = hex2str(data16)

with open(decfile, mode = "w") as fout:
    fout.write(data)

