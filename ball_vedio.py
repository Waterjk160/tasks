# -*- coding: utf-8 -*-
"""
Created on Sat Dec 11 09:54:39 2021

@author: Lenovo
"""
#1.加上fps
#2.计算几何重心
#3.画出重心变化的轨迹x
#4.改为RGB
import cv2
import numpy as np
cap=cv2.VideoCapture(0)
alldots=[]#存储所有轨迹
dots=[]#存储单次轨迹的重心坐标
flag=0#用于判断是否开始新的轨迹
while(cap.isOpened()):
    ret,img=cap.read()
    r=cv2.boxFilter(img,-1,(5,5))
    #转化为hsv
    hsv=cv2.cvtColor(r,cv2.COLOR_BGR2HSV)
    #cv2.imshow("img_hsv",hsv)
    #提取橙色颜色
    minorange=np.array([0,150,150])
    maxorange=np.array([15,255,255])
    mask=cv2.inRange(hsv,minorange,maxorange)
    blue=cv2.bitwise_and(img,img,mask=mask)    
    #提取图像轮廓
    gray=cv2.cvtColor(blue,cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray",gray)
    ret,binary=cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
    #cv2.imshow("binary",binary)
    #闭运算
    k=np.ones((10,10),np.uint8)
    r1=cv2.morphologyEx(binary,cv2.MORPH_CLOSE,k)
    #cv2.imshow("r1",r1)
    #开运算
    k=np.ones((10,10),np.uint8)
    r2=cv2.morphologyEx(r1,cv2.MORPH_OPEN,k)
    #cv2.imshow("r2",r2)
    contours,hierarchy=cv2.findContours(r2,
                                    cv2.RETR_LIST,
                                    cv2.CHAIN_APPROX_SIMPLE)

    if len(contours)!=0:
        #找轨迹找重心代码省去
        #构造矩形边界
        x,y,w,h=cv2.boundingRect(contours[0])
        brcnt=np.array([[[x,y]],[[x+w,y]],[[x+w,y+h]],[[x,y+h]]])
        cv2.drawContours(img,[brcnt],-1,(255,127,0),2)
        ##获取红色小球的重心
        m = cv2.moments(contours[0])
        area = m['m00']
        x = int(m['m10'] / area)
        y = int(m['m01'] / area)
        img=cv2.circle(img,(x,y),3,(255,127,0),-1)
        #增加文字
        x2=str(x+w/2)
        y2=str(y+h/2)
        text='x='+x2+','+'y='+y2
        img=cv2.putText(img,text,(x-70,y+20),cv2.FONT_HERSHEY_PLAIN,1,
                    (255,127,0),2)
        #绘制重心坐标
        if flag==0 :#是新的轨迹
            dots=[]
            flag=1
        dots.append((x,y))
    else :
        flag=0
    if len(dots)>1 :
        alldots.append(dots)
    #用直线
    for i in range(len(alldots)):
        for j in range(len(alldots[i])-1):
            img=cv2.line(img,alldots[i][j],alldots[i][j+1],(255,127,0),2)
  
    #显示帧率
    fps = cap.get(cv2.CAP_PROP_FPS)
    text2='fps:'+str(fps)
    img=cv2.putText(img,text2,(20,20),cv2.FONT_HERSHEY_PLAIN,1,
                   (0,0,255),1) 
    
    cv2.imshow("result",img)
    c=cv2.waitKey(1)
    if c==27 :
        break;
cap.release()
cv2.destroyAllWindows()