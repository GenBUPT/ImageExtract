import numpy as np
import zipfile
import os
from PIL import Image
def getdex(filename):
    apkfile = zipfile.ZipFile(filename,'r')
    dex = ""
    for tempfile in apkfile.namelist():
        if tempfile.endswith('.dex'):
            dex = apkfile.read(tempfile)
            break
    return dex
def get_dex_info(dex):
    # 输入dex二进制串，按照dex文件结构分段
    pass
def getwidth(size):
    filesize = size//1024
    if filesize < 10:
        return 32
    if filesize >= 10 and filesize <30:
        return 64
    if filesize >=30 and filesize <60:
        return 128
    if filesize >=60 and filesize < 100:
        return 256
    if filesize >=100 and filesize < 200:
        return 384
    if filesize >=200 and filesize < 500:
        return 512
    if filesize >=500 and filesize < 1000 :
        return 768
    if filesize >=1000:
        return 1024
    return size
def generator_img(filename,dex):
    size = len(dex)//8
    width = getwidth(size)
    long = size//width
    if size%width!=0:
        dex = dex + bytes(width*8-(len(dex)-width*long*8))
    imgs = dex[::8]
    long = len(dex)//(8*width)
    imgs = np.array(list(imgs)).reshape(long,width)
    imgs = Image.fromarray(np.uint8(imgs))
    imgs.convert("L")
    filename = filename.split('/')[-1]
    imgs.save("deximg/"+filename+".png")
def getfiles(filepath):
    filelists = []
    for path,dirlist, filelist in os.walk(filepath):
        for f in filelist:
            if f.endswith('.apk'):
                filelists.append(os.path.join(path,f))
    return filelists
def generatorGrayscale(filepath,outputpath):
    """
    filepath 待处理apk文件夹 outputpath 图片存放地址
    """
    filelist = getfiles(filepath)
    if os.path.isdir(outputpath) == False:
        os.makedirs(outputpath)
    success = 0
    failed = []
    whole = len(filelist)
    for file in filelist:
        try:
            dex = getdex(file)
            generator_img(file,dex)
            success+=1
        except :
            failed.append(file)
    f = open(filepath+"_log.txt","a")
    f.write("success :"+str(success))
    f.write("total : "+str(whole))
    f.close()
    if len(failed)!=0:
        f = open(filepath+"_failed.txt","w")
        f.write(str(failed))
        f.close()
if __name__ == '__main__':
    filepath = "/home/public/rmt/malware/benign_1000"
    outputpath = "./deximg"
    generatorGrayscale(filepath,outputpath)
    
    