from PIL import Image
from config import *

def modify_c(colour, s):
    if s == '0':
        colour = colour + colour%2
        if colour == 256:
            colour = colour - 2
    else:
        colour  = colour + int(not (colour%2))
    return colour    

def getlsb(px):
    return str(px[0]%2) + str(px[1]%2) + str(px[2]%2)

def steganize(user):
    with open(srcpath + user.src, 'rb') as fin:
        file_src = fin.read()

    file_src = bytes(user.src[user.src.find('.'):] + '0', encoding='utf-8') + file_src
    
    bin_src = ''
    for i in file_src:
        zeros = 8 - len(bin(i)[2:])
        bin_src = bin_src + '0'*zeros + bin(i)[2:]
    
    bin_src = '0'*(28-len(bin(len(bin_src))[2:])) + bin(len(bin_src))[2:] + bin_src

    pic = Image.open(picpath + user.pic)
    picpx = pic.load()
    
    if len(bin_src) > 3*pic.height*pic.width:
        return None

    res = Image.new('RGB', pic.size)
    respx = res.load()

    i = 0
    tmp = [0,0,0]

    for x in range(pic.width):
        for y in range(pic.height):
            for j in range(3):
                if i < len(bin_src):
                    tmp[j] = modify_c(picpx[x,y][j], bin_src[i])
                    i = i + 1
                else:
                    tmp[j] = picpx[x,y][j]
            respx[x,y] = tuple(tmp)
    
    res = res.save(picpath + str(user.id) + '.png')

    return open(picpath + str(user.id) + '.png', 'rb')
    

def desteganize(user):
    pic = Image.open(picpath + user.pic)
    picpx = pic.load()

    bin_res = ''
    for x in range(pic.width):
        for y in range(pic.height):
            bin_res = bin_res + getlsb(picpx[x,y])

    res_len = int(bin_res[:28],2)
    bin_res = bin_res[28:28 + res_len]
    
    res = []
    
    for i in range(0, len(bin_res), 8):
        res.append(int(bin_res[i:i + 8], 2))
    
    res = bytes(res)
    file_name = str(user.id) + str(res[:res.find(ord('0'))])[2:-1]
    res = res[res.find(ord('0')) + 1:]
    
    with open(srcpath + file_name, 'wb') as fileout:
        fileout.write(res)

    return open(srcpath + file_name,'rb')

def genpic(file_name, sizes):
    expic = Image.open(picpath + ex_pic)
    res = expic.resize(sizes)
    res.save(picpath + file_name)