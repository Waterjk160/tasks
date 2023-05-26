# -*- coding: utf-8 -*-
"""
Created on Tue Dec 21 22:47:33 2021

@author: Lenovo
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

img=cv2.imread("image.png",cv2.IMREAD_GRAYSCALE)
h,w=img.shape[:2]
size = (int(w * 0.2), int(h * 0.2)) 
img=cv2.resize(img,size, interpolation=cv2.INTER_AREA)
img1=cv2.resize(img,size, interpolation=cv2.INTER_AREA)
h1,w1=img.shape[:2]
img = img[0:h1-150, 0:870]
height = img.shape[0]
width = img.shape[1]
#利用线性灰度变换
#方法一
a = np.array(img, np.uint8)
tra = 2* a+1
plt.hist(tra.ravel(),256)
# =============================================================================
# #对数变换
# a = np.array(dst, np.uint8)
# b2=50* np.log((1.0 + a))
# print(b2)
# cv2.imshow("res",b2)
# plt.hist(b2.ravel(),256)
# =============================================================================
# =============================================================================
# #伽马变换
# result = 2 * np.power(dst / float(np.max(dst)), 2) * 255.0
# result = np.uint8(result)
# cv2.imshow("res",result)
# plt.hist(result.ravel(),256)
# =============================================================================
retval,binary=cv2.threshold(tra,65,255,cv2.THRESH_BINARY)
k=np.ones((11,11),np.uint8)
binary=cv2.morphologyEx(binary,cv2.MORPH_CLOSE,k)
kernel=np.zeros((7,7),np.uint8)
binary=cv2.erode(binary,kernel,iterations=3)
binary=cv2.morphologyEx(binary,cv2.MORPH_OPEN,k)
contours,hierarchy=cv2.findContours(binary,
                                    cv2.RETR_LIST,
                                    cv2.CHAIN_APPROX_SIMPLE)
color=cv2.cvtColor(binary,cv2.COLOR_GRAY2BGR)
n=len(contours)
dots=[]
rows,cols=color.shape[:2]
for i in range(n):
    m = cv2.moments(contours[i])
    area = m['m00']
    x = int(m['m10'] / area)
    y = int(m['m01'] / area)
    img1=cv2.circle(color,(x,y),3,(0,0,255),-1)
    dots.append((x,y))
    text=str(i)
    res=cv2.putText(color,text,(x,y),cv2.FONT_HERSHEY_PLAIN,1,
                (0,100,0),2)
    if i%10==9:
        nptest=np.array(dots)
        [vx,vy,x,y]=cv2.fitLine(nptest,cv2.DIST_L2,0,0.01,0.01)
        lefty=int((-x*vy/vx)+y)
        righty=int(((cols-x)*vy/vx)+y)
        img = cv2.line(color,(cols-1,righty),(0,lefty),(0,255,0),2)
        dots=[]
cv2.imshow("res",color)
cv2.imwrite("germany_beer.jpg",color)
cv2.waitKey()
cv2.destroyAllWindows()