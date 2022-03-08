import zipfile
from PIL import Image
import numpy as np
p = Image.open("test.png").convert("RGB")
img = np.array(p)[0]
ind = [-1]
for i in range(len(img)):
    if img[i][0]!=img[i][1]:
        print(img[i])
        ind.append(i)
k = p.tobytes()[3*(ind[0]+1):3*ind[1]]
s = p.tobytes()[3*8124211:]
name = Image.frombytes("RGB",(len(s)//3,1),s).convert("L").tobytes().decode("ascii")
typePoint = ['MethodOverload','Origin','Reflection','CallIndirection','Goto','Nop','Reorder','ArithmeticBranch']
path = "/home/public/rmt/malware/Simclr/malware/"
print(name)
origin = path+typePoint[k[-1]-1]+"/"+name

dex= bytes()
apkfile = zipfile.ZipFile(origin,"r")
for temp in apkfile.namelist():
    if temp.endswith(".dex"):
        dex = apkfile.read(temp)
        break
tmp = dex
if(len(dex)%8!=0):
    tmp +=bytes(8-len(dex)%8)
img = Image.frombytes("L",(len(tmp)//8,1),tmp[::8])
img = img.convert("RGB")
img = img.tobytes()

print(img==k[:-3])