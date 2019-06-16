import pyautogui as pg
import time
import json
from PIL import Image
import aircv as ac
import cv2
import numpy as np
import os

points_dict = json.load(open("json/points.json", "r", encoding='utf-8'))
colors=['hei','jin','bai']

img_sucai = {}
img_mark = {}

# 将图片读入内存
# def load_image():
#     images_dict = json.load(open("json/images.json", "r", encoding='utf-8'))
#     # print(images_dict)
#     for key in images_dict.keys():
#         # print(images_dict[key])
#         images_dict[key]=cv2.imread(images_dict[key])

#     for col in colors:
#         images_dict[col]=[]
#         rootdir = "image/sucai/%s"%(col)
#         files = os.listdir(rootdir)
#         for f in files:
#             path = os.path.join(rootdir,f)
#             images_dict[col].append(cv2.imread(path)) 

#     return images_dict   
# 将图片读入内存 需将图片读取为灰度图
def load_image(rootdir,flags = 0):
    img_dict={}
    files = os.listdir(rootdir)
    for f in files:        
        path = os.path.join(rootdir,f)
        f = f.split(".jpg")[0]       
        # flags = 0表示灰度图，1表示bgr彩图
        img_dict[f]=cv2.imread(path,flags = flags)
    return img_dict

# region应该有四个参数，起点的x，y坐标，截取区域的宽，高
def screenshot(region=None,mode=cv2.COLOR_RGB2GRAY):
    if region == None:
        shotIm =  pg.screenshot()
    else:
        shotIm = pg.screenshot(region=region)    
    
    return cv2.cvtColor(np.asarray(shotIm),mode)#cv2.COLOR_RGB2BGR

def make_color():
    img=screenshot()
    x,y=pg.position()
    r,g,b=img.getpixel((x,y))
    return x,y,r,g,b

def find_color(xd,yd,r,g,b,size=5,coss=3):
    img=screenshot()
    wide,high=img.size
    for i in range(xd-5,xd+5):
        for j in range(yd-5,yd+5):
            pg.moveTo(i,j)
            R,G,B=img.getpixel((i,j))
            print("颜色%d %d %d"%(R,G,B))
            if(r,g,b)==(None,None,None):
                print("未获取颜色值！")
                return
            # if(R,G,B)==(r,g,b):
            if(abs(R-r)<coss and abs(G-g)<coss and abs(B-b)<coss ):
                pg.moveTo(i,j)
                print('x坐标为%d,y坐标为%d'%(i,j))
                return

def find_img(src,dist,threshold=0.8,region=0,rgb=False):
    # shotIm = pg.screenshot()
    # img = cv2.cvtColor(np.asarray(shotIm),cv2.COLOR_RGB2BGR)

    # 返回结果pos是个字典 {'result': (277.0, 528.0), 'rectangle': ((263, 518), (263, 538), (291, 518), (291, 538)), 'confidence': 0.9989873170852661}
    pos = ac.find_template(src, dist,threshold=threshold,rgb=rgb)
    if pos is None:        
        return None
    else:
        if region == 0:
            return pos['result']
        else:
            return pos['rectangle']

# 传入参数该为 cv2读取后的图片矩阵
def search_sucai(img_sucai):
    shot=screenshot()
    for img in img_sucai:
        pos = find_img(shot,img,threshold=0.8)
        if pos != None:
            pg.moveTo(pos)
            pg.click()
            time.sleep(0.5)
# def search_sucai(name):
#     img=screenshot()
#     rootdir = "image/sucai/%s"%(name)
#     list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
#     for i in range(len(list)):
#         path = os.path.join(rootdir,list[i])
#         if os.path.isfile(path):
#             pos = find_img(img,cv2.imread(path),threshold=0.8)
#             if pos != None:
#                 pg.moveTo(pos)
#                 pg.click()
#                 time.sleep(0.5)

# 错得离谱 先用单点法
def fight(order=[0,1,2]):
    img = screenshot()    
    color=['hei','jin','bai']
    # 连消技能
    for i in range(4):
        for j in range(3):
            pos = find_img(img,cv2.imread("image/xin/%s%d.jpg"%(color[order[j]],i)),threshold=0.8,region=1,rgb=True)
            if pos != None:
                pg.moveTo(pos[0])
                pg.dragTo(pos[3],duration=1)
                print(color[order[j]],i)
                return 0

    # 单点技能
    for j in range(3):
        pos = find_img(img,cv2.imread("image/xin/%s3.jpg"%(color[order[j]])),threshold=0.9,region=0,rgb=True)
        if pos != None:
            pg.moveTo(pos[0])
            pg.click()
            print(color[order[j]],3)
            return 0
    
    return 1
 
if __name__ == '__main__':
    # print(ac.find_template(cv2.imread("image/shizhong.jpg"),cv2.imread("image/shizhong.jpg")))
    # print( find_color(1464, 844, 69, 54, 42,coss=10))
    # color=['hei','jin','bai']
    # order=[0,1,2]
    # for i in range(4):
    #     for j in range(3):
    #         print("image/xin/%s%d.jpg"%(color[order[j]],i))

    # while True:
    #     input("开始")
    #     time.sleep(2)
    #     fight()
    # images_dict=load_image()
    load_image()
        # flags = 0表示灰度图，1表示bgr彩图
        # img_dict[f]=cv2.imread(path,flags = 0)
    