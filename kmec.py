import cv2
import math
import os
import pandas as pd 
import numpy as np 
def distance(a,b):
    d=0
    for i in range(len(a)):
        d=d+pow(b[i]-a[i],2)
    d=math.sqrt(d)
    return d
def min_distance(dis):
    min=dis[0]
    vt=0
    for i in range(len(dis)):
        if(min>dis[i]):
            min = dis[i]
            vt=i
    return vt
def kmec(img_path):
    color = {'red':[0,0,255],
    'green' : [0,128,0],
    'blue' : [255,0,0],
    'yellow' : [0,255,255],
    'orange' : [0,165,255],
    'purple' : [128,0,128]}
    H=[] # lưu vecto
    for i in range(len(color)):
        H.append(0)
    img = cv2.imread(img_path)
    (h, w, d) = img.shape #lây kich thuoc anh
    for i in range(h):
        for j in range(w):
            D=[] #luu khoang cach giua diem anh vs cac mau trong color
            for k in color: 
                D.append(distance(color[k],img[i,j]))
            H[min_distance(D)] = H[min_distance(D)]+1
    s = sum(H)
    for i in range(len(H)):
        H[i] = H[i]/s
    return H

path = "E:\\anh_csdldpt"
anh= os.listdir(os.path.expanduser(path))
arr=[]
for i in anh:
    p = path+'\\'+i
    a=kmec(p)
    arr.append(a)
column=[]
for i in range(len(arr[0])):
    l = 'cot '+str(i)
    column.append(l)
df = pd.DataFrame(data = arr, columns = column)
df.to_csv("kmec.csv",index=False)

