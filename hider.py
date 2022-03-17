from PIL import Image
from pplib import *
from info import *


#Загрузка пересылаемой информации
fin = open(datafile)
data16 = fin.read()
fin.close()


#Загрузка носителя
src = Image.open(srcfile)
srcpx = src.load()

#Формирование выходного изображения
res = Image.new("RGB", src.size)
respx = res.load()

#Цикл по каждому пикселю
i = 0
for x in range(src.width):
    for y in range(src.height):
        if i < len(data16):
            tmp = rgb2hex(srcpx[x,y])
            tmp = tmp[:5] + data16[i]
            respx[x,y] = hex2rgb(tmp)
            i = i + 1
        else:
            respx[x,y] = srcpx[x,y]


res = res.save(encfile)





