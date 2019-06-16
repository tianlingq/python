import pyautogui as pg
import time
import json
from PIL import ImageGrab
import cv2
import numpy as np
import os

points_dict = json.load(open("json/points.json", "r", encoding='utf-8'))
marks_dict = json.load(open("json/marks.json", "r", encoding='utf-8'))

# img_mark = {}
# img_sucai = {}

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

def find_img(src,dist,threshold=0.8,region=None):
    # shotIm = pg.screenshot()
    # img = cv2.cvtColor(np.asarray(shotIm),cv2.COLOR_RGB2BGR)

    # 返回结果pos是个字典 {'result': (277.0, 528.0), 'rectangle': ((263, 518), (263, 538), (291, 518), (291, 538)), 'confidence': 0.9989873170852661}
    # pos = ac.find_template(src, dist,threshold=threshold)   
    # ac.find_template方法封装了 cv2.matchTemplate，但效率低下，不如直接使用原函数
    
    # 将图像的三个维度进行加权处理
    # s_bgr = cv2.split(src) # Blue Green Red
    # d_bgr = cv2.split(dist)
    # weight = (0.3, 0.3, 0.4)
    # resbgr = [0, 0, 0]    
    # for i in range(3): # bgr
    #     resbgr[i] = cv2.matchTemplate(s_bgr[i], d_bgr[i], method)
    # res = resbgr[0]*weight[0] + resbgr[1]*weight[1] + resbgr[2]*weight[2]

    # cv2.matchTemplate只能处理单通道图像，故需将图像转换为灰度图
    # cv2.TM_CCOEFF_NORMED 方法中匹配的最高的图像值最大，即取max_val
    method=cv2.TM_CCOEFF_NORMED

    # 返回值是最大和最小的匹配值，及其对应左上角坐标
    res = cv2.matchTemplate(src, dist, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print(max_val)
    if max_val < threshold:          
        return None
    else:
        if region != None:
            # max_loc = list(max_loc) + region[0:2]
            max_loc =(max_loc[0]+region[0],max_loc[1]+region[1])
        # print(max_loc)
        # opencv中图片存储为列优先，第0维是y轴，第1维是x轴
        pos = (max_loc[0]+dist.shape[1]//2,max_loc[1]+dist.shape[0]//2)        
        return pos

def chick_mark(src,temple,reg,threshold=0.8):
    h , w = temple.shape
    # 列优先
    img=src[reg[1]:reg[3],reg[0]:reg[2]]

    method=cv2.TM_CCOEFF_NORMED
    # 返回值是最大和最小的匹配值，及其对应左上角坐标
    res=cv2.matchTemplate(img, temple, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        pos = (max_loc[0]+reg[0],max_loc[1]+reg[1])
        return (pos[0]+w//2,pos[1]+h//2)
    else:
        return None

# 传入参数该为 cv2读取后的图片矩阵
def search_sucai(img_sucai):
    src=screenshot()
    for img in img_sucai:
        pos = find_img(src,img_sucai[img],threshold=0.8)
        if pos != None:
            pg.moveTo(pos)
            pg.click()
            time.sleep(0.5)

def get_xin(color):
    s = np.sum(color/color.max())
    # BGR颜色中由百分百可得 黑(1,0.5,0.5)  金(0.5,1,1) 白(1,1,1)
    # 然后将其分别定为 1,2,3 三个不同的质数，便于判断是否相同
    if s <= 2:
        return 1
    elif s <= 2.5:
        return 2
    else:
        return 3

def mouse_drag(start,end,interval=1):
    pg.mouseDown(start)
    pg.moveTo(end,duration=interval)
    pg.mouseUp()

# 1,2,3,4 分别对应1消，横2消，纵2消，4消
def jineng(index,mode):
    reg = points_dict['xin_region']
    dis = points_dict['juli'][0]

    if mode == 1:
        pg.click((reg[0]+index[0]*dis,reg[1]+index[1]*dis))
        return
    elif mode == 2:
        start=(reg[0]+index[0]*dis,reg[1]+index[1]*dis)
        end=(reg[0]+(index[0]+1)*dis,reg[1]+index[1]*dis)       
    elif mode == 3:
        start=(reg[0]+index[0]*dis,reg[1])
        end=(reg[0]+index[0]*dis,reg[1]+dis)
    else:
        start=(reg[0]+index[0]*dis,reg[1])
        end=(reg[0]+(index[0]+1)*dis,reg[1]+dis)
    mouse_drag(start,end)
     
def fight():
    reg = points_dict['xin_region']
    num = points_dict['xin_num'][0]
    dis = points_dict['juli'][0]
    # colors = points_dict['colors']

    xin = np.zeros((num,2))
    
    src = screenshot(region=reg,mode=cv2.COLOR_RGB2BGR)
    # src = cv2.imread("jietu/2.jpg")
    # src = src[780:920,480:1270]

    # 列优先 起点[y,x]  第一行[y,x+i*dis] 第二行[y+dis,x+i*dis]
    for i in range(num):
        xin[i,0] = get_xin(src[0,i*dis])
        xin[i,1] = get_xin(src[dis,i*dis])
    
    index = [0,0]
    max_xin = 1

    # 先查横向的2消，更容易出4消
    for j in range(2):
        for i in range(num-1):
            if xin[i,j]==xin[i+1,j]:
                # 判断是否可以4消
                if j == 0:
                    if xin[i,0] == xin[i,1] == xin[i+1,1]:
                        jineng([i,0],4)
                        return
                # 不行就记录第一个2消的位置
                if max_xin == 1:
                    index = [i,j]
                    max_xin = 2

    if max_xin == 2:
        jineng(index,2)
        return

    # 先查纵向的2消
    for i in range(num):
        if xin[i,0]==xin[i,1]:
            jineng([i,0],3)
            return
    
    jineng([0,0],3)

# 优先使用黑1，默认带诺瓦
def sushua():
    reg = points_dict['xin_region']
    num = points_dict['xin_num'][0]
    dis = points_dict['juli'][0]
    # colors = points_dict['colors']

    xin = np.zeros((num,2))
    
    src = screenshot(region=reg,mode=cv2.COLOR_RGB2BGR)
    # src = cv2.imread("jietu/2.jpg")
    # src = src[780:920,480:1270]

    # 列优先 起点[y,x]  第一行[y,x+i*dis] 第二行[y+dis,x+i*dis]
    for i in range(num):
        xin[i,0] = get_xin(src[0,i*dis])
        xin[i,1] = get_xin(src[dis,i*dis])
    
    index = [0,0]
    max_xin = 1

    # 先查横向的2消，更容易出4消
    for j in range(2):
        for i in range(num-1):
            # 优先黑1
            if xin[i,j] == 1:
                jineng([i,j],1)
                return

            if xin[i,j]==xin[i+1,j]:
                # 判断是否可以4消
                if j == 0:
                    if xin[i,0] == xin[i,1] == xin[i+1,1]:
                        jineng([i,0],4)
                        return
                # 不行就记录第一个2消的位置
                if max_xin == 1:
                    index = [i,j]
                    max_xin = 2

    if max_xin == 2:
        jineng(index,2)
        return

    # 先查纵向的2消
    for i in range(num):
        if xin[i,0]==xin[i,1]:
            jineng([i,0],3)
            return
    
    jineng([0,0],3)


if __name__ == '__main__':
    # time.sleep(1)
    # mouse_drag((220,300),(450,550))
    
    sucai_start()
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
    # load_image()
        # flags = 0表示灰度图，1表示bgr彩图
        # img_dict[f]=cv2.imread(path,flags = 0)
    