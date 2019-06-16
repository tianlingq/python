from basic import *

shotIm = None

def tiaozhan_start():
    name = input("请输入任意字符\n")
    if name != None:
        print("5s后开始执行，请切到模拟器")
        for i in range(4, 0, -1):
            print("{} s".format(i))
            time.sleep(1)
        print("开始执行")
        
        # if name not in points_dict['colors']:
        #     print("关卡输入错误")
        #     return

        # 读取图片
        img_mark = load_image("mark")
        # img_sucai = load_image("sucai//%s"%(name))

        pg.FAILSAFE = True
        is_queren=False
        while True:
            shotIm = screenshot()
            # 点击确认       
            pos = chick_mark(shotIm,img_mark['queding'],marks_dict['queding'])
            if pos != None:
                pg.click(pos)
                
            pos = chick_mark(shotIm,img_mark['chuzhan'],marks_dict['chuzhan'])
            if pos != None :       
                # 点击过确认按钮说明，挑战失败 自动降低难度  
                if is_queren:
                    pg.click(tuple(points_dict['shangguan']))
                pg.moveTo(pos)
                pg.click(clicks=2,interval=1)
                time.sleep(3)
                continue
                # break
            
            

            pos = chick_mark(shotIm,img_mark['shizhong'],marks_dict['shizhong'])
            if pos != None:
                # 进入战斗场景，开始移动和寻找素材
                while True:
                    # 战斗结束
                    pos = chick_mark(shotIm,img_mark['jiesuan'],marks_dict['jiesuan'])
                    # pos = chick_mark(shotIm,'jiesuan')
                    if pos != None:
                        # pg.moveTo(pos)
                        pg.click(pos)
                        break
                    
                    # 捡素材
                    # search_sucai(img_sucai)

                    # 找战斗加成的宝箱意义不大
                    # pos = find_img(img,cv2.imread("image/baoxiang.jpg"))
                    # if pos != None:
                    #     pg.moveTo(pos)
                    #     pg.click() 
                    
                    # 战斗循环
                    while True:
                        shotIm = screenshot()
                        # pos = chick_mark(shotIm,'canmou',0.9)
                        pos = chick_mark(shotIm,img_mark['canmou'],marks_dict['canmou'],0.9)
                        if pos == None:
                            # pos = chick_mark(shotIm,'canmou2',0.9)
                            pos = chick_mark(shotIm,img_mark['canmou2'],marks_dict['canmou2'],0.9)
                            if pos == None:
                                break
                        # pg.click(points_dict['gongji'])
                        # fight()
                        sushua()
                        time.sleep(2)

                    # 啥都没有就向前走
                    pg.mouseDown(points_dict['yidong'])
                    time.sleep(0.5)
                    pg.mouseUp()
            
            # 战斗结束
            # pos = chick_mark(shotIm,'jiesuan')
            pos = chick_mark(shotIm,img_mark['jiesuan'],marks_dict['jiesuan'])
            if pos != None:
                pg.click(pos)
                time.sleep(3)
                continue
            
            # 战斗失败点击确认
            if is_queren == False:            
                pos = chick_mark(shotIm,img_mark['queren'],marks_dict['queren'])
                if pos != None:
                    pg.click(pos)
                    is_queren=True
                    time.sleep(3)

            # while True:
            #     pos = find_img(img,)


if __name__ == '__main__':
    # print(shotIm)
    tiaozhan_start()
    # for i in range(points_dict['xin_'])
    # ImageGrab.grab(bbox=[])
    # for i in range(6):
    #     img=cv2.imread("%d.jpg"%(i))
    #     # print(img[5,5],i)
    #     # img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #     print(img[5,5],i)

    