
import random
from PIL import Image
from matplotlib.cbook import flatten
import numpy as np
#from sklearn.mixture import BayesianGaussianMixture 
from grayscale import getwidth
import os
import unittest
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
        imgarray.append(np.uint8([251,252,253]))
    return imgarray
def splitImg(bigImg):
    """
    输入大图，随机切出一个小图,返回小图以及其在图片中的顺序
    """
    ind = [-1]
   
    for i in range(0,len(bigImg)):
        if bigImg[i][0]==251 and bigImg[i][1]==252 and bigImg[i][2]==253:
          
            ind.append(i)
   
    imgpos = random.randint(1,len(ind)-1)
    
    return bigImg[ind[imgpos-1]+1:ind[imgpos]],imgpos
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
    return long,width

class TestMerge(unittest.TestCase):

    def test_init(self):
        
        imgpath = "/home/gxj/binarys/deximg/"
     
        filelist = []
        for file in os.listdir(imgpath)[10:60]:
            filelist.append(os.path.join(imgpath,file))
        imgs = []
        for file in filelist:
            imgs.append(np.array(Image.open(file).convert("RGB")))
        bigimg = mergeImg(filelist)
        print("图片总数"+str(len(imgs)))
        width = getwidth(len(bigimg))
        if len(bigimg)%width!=0:
            
            for _ in range(0,(width-len(bigimg)%width)):
                c = np.uint8([0,0,0])
                
                bigimg.append(c)
        bigimg = [bigimg[i:i+width] for i in range(0,len(bigimg),width)]
      
        bigimg = np.array(bigimg)
        
        newimg = Image.fromarray(bigimg,"RGB")
        newimg.save("big.png")
        newimg = np.array(Image.open("big.png").convert("RGB"))
        bigimg = []
        for row in newimg:
            for p in row:
                bigimg.append(p)
        for _ in range(10):
            img,npos = splitImg(bigimg)  
            imgp = []
            for row in imgs[npos-1]:
                for p in row:
                    imgp.append(p)
            for i in range(len(img)):
                self.assertTrue((img[i]==imgp[i]).all())
if __name__ =="__main__":
    unittest.main()
    

    
