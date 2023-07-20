import cv2
import numpy as np 
import pandas as pd 
import math
import os
import imutils
def hog (img_path,cell_x,cell_y,bin_num,block_size):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    edeged = imutils.auto_canny(img)
    cnts = cv2.findContours(edeged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key = cv2.contourArea)
    (x, y, w, h) = cv2.boundingRect(c)
    img = img[y:y+h, x:x+w]
    img = cv2.resize(img, (128, 128))
    
    xkernel = np.array([[-1, 0, 1]])
    ykernel = np.array([[-1], [0], [1]])
    dx = cv2.filter2D(img, cv2.CV_32F, xkernel)
    dy = cv2.filter2D(img, cv2.CV_32F, ykernel)
    bien_do = []
    for i in range(len(dx)):
        t=[]
        for j in range(len(dx[i])):
            a = math.sqrt(pow(dx[i][j],2)+pow(dy[i][j],2))
            t.append(a)
        bien_do.append(t)
    huong=[]
    for i in range(len(dx)):
        t=[]
        for j in range(len(dx[i])):
            a = math.degrees(math.atan(dy[i][j]/(dx[i][j]+0.00001)))+90
            t.append(a)
        huong.append(t)
    (h, w) = img.shape
    histogram =[]
    bien_do=np.array(bien_do)
    huong=np.array(huong)
    for i in range(0,h,cell_y):
        hist_y=[]
        for j in range(0,w,cell_x):
            h = huong[i:i+cell_y, j:j+cell_x] #lấy phần tử ở hàng thứ i đến hàng thứ i+cell_y và từ cột j đến cột j+cell_x
            bd = bien_do[i:i+cell_y, j:j+cell_x]
            hist,bin= np.histogram(h, bins=bin_num, range=(0, 180), weights=bd)
            hist_y.append(hist.tolist())
        histogram.append(hist_y)
    histogram=np.array(histogram)
    x,y,z = histogram.shape
    # print(x,y,z)
    # block_size=2
    feature=[]
    for i in range(x-block_size+1):
        block=[]
        for j in range(y-block_size+1):
            v=histogram[i:i+block_size,j:j+block_size]
            v=v.flatten()
            v= v / np.sqrt(np.sum(v**2)+0.000001**2)
            block.append(v)
        feature.append(block)
    feature = np.array(feature)
    feature = feature.flatten()
    return feature

path = "E:\\anh_csdldpt"
anh= os.listdir(os.path.expanduser(path))
arr=[]
for i in anh:
    p = path+'\\'+i
    a=hog(p,8,8,9,2)
    a=a.tolist()
    arr.append(a)
column=[]
for i in range(len(arr[0])):
    l = 'cot '+str(i)
    column.append(l)
df = pd.DataFrame(data = arr, columns = column)
df.to_csv("hog.csv",index=False)