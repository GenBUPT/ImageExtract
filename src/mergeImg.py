import os

import zipfile

from PIL import Image

import numpy as np

def getBigImgByDex(filelist:list):
    dexs = []
    for file in filelist:
        apkfile = zipfile.ZipFile(file,"r")
        for temp in apkfile.namelist():
            if temp.endswith('.dex'):
                dexs.append(apkfile.read(temp))
                break;
    return dexs
def genImg(filemap:dict,dirpath):
    typePoint = {'MethodOverload':[1,1,1],'Origin':[2,2,2],'Reflection':[3,3,3],'CallIndirection':[4,4,4],'Goto':[5,5,5],'Nop':[6,6,6],'Reorder':[7,7,7],'ArithmeticBranch':[8,8,8]}
    count = 0
    for key in filemap:
        if count== 7924:
            break
        count+=1
        dexs = getBigImgByDex(filemap[key])
        imgs = []
        pos = 0
        print(key)
        imgname = bytes(key,"ascii")
        imgname = Image.frombytes("L",(len(imgname),1),imgname)
        imgname = imgname.convert("RGB")
        imgname = imgname.tobytes()
        for dex in dexs:
            tmp = dex
            
            if len(dex)%8!=0:
                tmp += bytes(8-len(dex)%8)
            
            img = Image.frombytes("L",(len(tmp)//8,1),tmp[::8])
            img = img.convert("RGB")
            img = img.tobytes()
            img = list(img)+typePoint[filemap[key][pos].split("/")[-2]]+[251,252,253]
            pos+=1
            imgs+=img
        
        imgs = imgs+list(imgname)
        bigimg = Image.frombytes("RGB",(len(imgs)//3,1),bytes(imgs))
        
        try : 
            bigimg.save(dirpath+"/"+key+".png")
            print(dirpath+"/"+key+".png")
        except Exception as e:
            print(e)
            print(key)
def getfiles(dirpath:str):
    filelist = []
    for path,dir,files in os.walk(dirpath):
        for file in files:
            filelist.append(os.path.join(path,file))
    return filelist
def getfileDict(dirlist:list):
    imgs = []
    for dir in dirlist:
        imgs += getfiles(dir)

    filedict = {}
    for file in imgs:
    
        try : 
            name = file.split('/')[-1]
        except Exception as e:
            print(e)
            name = "void"
        if name not in filedict.keys():
            filedict[name] = []
            filedict[name].append(file)
        else:
            filedict[name].append(file)
    return filedict
    
    
"""
图片生成/切割流程：
1. 恶意文件生成：8个文件夹中生成7000+个图片，每个图片从8个文件夹中获得，按照一个顺序排列，插入标志位和序号（XD）以及文件名转的那个玩意（ascii码）
2. 白文件同理
3. 切割和检查：切割分解图片获得子图、序号和文件名，加载文件并检查切割正确

"""
if __name__=='__main__':
    os.chdir("benign")
    paths = ['MethodOverload','Origin','Reflection','CallIndirection','Goto','Nop','Reorder','ArithmeticBranch']
    dicts = getfileDict(paths)
    dirpath = "/home/gxj/ImageExtract/resource/benign"
    genImg(dicts,dirpath)
    
    
    
    
    
