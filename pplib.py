def rgb2hex(rgb):
    return '%02x%02x%02x' % rgb

def hex2rgb(hxd):
    r = int(hxd[:2], 16)
    g = int(hxd[2:4], 16)
    b = int(hxd[4:], 16)
    return (r,g,b)

def str2hex(s):
    hxd = ""
    for i in s:
        tmp = hex(ord(i))[2:]
        if len(tmp) > 3:
            raise ValueError("Too strange symbols in string")
        hxd = hxd + '0'*(3 - len(tmp)) + tmp
    return hxd

def hex2str(hxd):
    s = ""
    while len(hxd)%3:
        hxd = hxd[:len(hxd)-1]
    for i in range(0,len(hxd),3):
        s = s + chr(int(hxd[i:i+3], 16))
    return s
        
