from PIL import Image
from pplib import *
from info import *

def hex2str(hxd):
    s = ""
    while len(hxd)%3:
        hxd = hxd[:len(hxd)-1]
        
    for i in range(0,len(hxd),3):
        s = s + chr(int(hxd[i:i+3], 16))
    return s


#Открытие носителя
src = Image.open(encfile)
srcpx = src.load()

f = 0

#Цикл по каждому пикселю
data16 = ""

for x in range(src.width):
    for y in range(src.height):
        tmp = rgb2hex(srcpx[x,y])
        data16 = data16 + tmp[5]
        if data16[-3:] == "000":
            f = 1
            break
    if f:
        break


data = hex2str(data16)

with open(decfile, mode = "w") as fout:
    fout.write(data)

