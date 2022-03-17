import os

def str2hex(s):
    hxd = ""
    for i in s:
        tmp = hex(ord(i))[2:]
        if len(tmp) > 3:
            print(i)
            raise ValueError("Too strange symbols in string")
        hxd = hxd + '0'*(3 - len(tmp)) + tmp
    return hxd


for file in os.listdir():
    if file.find(".txt") != -1:
        with open(file) as fin:
            data = fin.read()
            try:
                data16 = str2hex(data)
            except Exception:
                print("in",file)
        with open("hxd_"+ file, mode = "w") as fout:
            fout.write(data16)
