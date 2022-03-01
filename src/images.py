import random
from PIL import Image
import numpy as np 
from grayscale import getwidth
def getfilelist():
    """
        获得要合成的图
    """
    pass
def mergeImg(imglist):
    """
    将若干个图合成一个大图，返回数组，数组可以通过saveImage函数保存
    合成大图时在每个子图的最后加一位[251,252,253]作为标志位用来后续的随机切割
    """
    imgarray = []
    for file in imglist:
        img = np.array(Image.open(file).convert("RGB"))
        
        for raw in img:
            for pixiv in raw:
                imgarray.append(pixiv)
        imgarray.append([251,252,253])
    return imgarray
def splitImg(bigImg):
    """
    输入大图，随机切出一个小图
    """
    ind = [index for (index,value) in enumerate(bigImg) if value[0]==251 and value[1]==252 and value[2]==253]
    imgpos = random.randint(1,len(ind))
    ind.insert(0,-1)
    return bigImg[ind[imgpos-1]+1:ind[imgpos]]
def saveImg(img,filename):
    """
    输入一个RGB格式的图片数组，保存为灰度图
    img形式：
    [[23,23,23],[14,14,14]...
    ...
    [144,144,144],[3,3,3]...
    ]
    """
    width = getwidth(len(img))
    long = len(img)//width
    imgarray = []
    for raw in img:
        imgarray.append((raw[0]*299+raw[1]*587+raw[2]*114)//1000)
    if len(img)%width!=0:
        imgarray += (width-len(imgarray)%width)*[0]
    long = len(imgarray)//width
    newimg = np.array(imgarray).reshape(long,width)
    newimg = Image.fromarray(np.uint8(newimg))
    newimg.convert('L')
    newimg.save(filename)

if __name__ == "__main__":
    filelist = ['test1.png','test2.png','test3.png']
    bigImage = mergeImg(filelist)
    saveImg(splitImg(bigImage),"test.png")
    

    
