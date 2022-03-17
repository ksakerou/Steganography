import os

def hex2str(hxd):
    s = ""
    while len(hxd)%3:
        hxd = hxd[:len(hxd)-1]
    for i in range(0,len(hxd),3):
        s = s + chr(int(hxd[i:i+3], 16))
    return s

for file in os.listdir():
    if file.find(".txt") != -1:
        with open(file) as fin:
            data16 = fin.read()
            data = hex2str(data16)
        with open("str_"+ file, mode = "w") as fout:
            fout.write(data)
