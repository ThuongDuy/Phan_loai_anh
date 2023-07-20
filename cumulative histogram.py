import numpy as np 
import pandas as pd 
import cv2
import os
def cumulative_histogram(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    hist,bin= np.histogram(img, bins=256, range=(0, 255))
    cumulative_histogram=[]
    (h, w) = img.shape
    t=0
    for i in range(len(hist)):
        t=t+hist[i]
        cumulative_histogram.append(t/(h*w))
    return cumulative_histogram


path = "E:\\anh_csdldpt"
anh= os.listdir(os.path.expanduser(path))
arr=[]
for i in anh:
    p = path+'\\'+i
    a=cumulative_histogram(p)
    arr.append(a)
column=[]
for i in range(len(arr[0])):
    l = 'cot '+str(i)
    column.append(l)
df = pd.DataFrame(data = arr, columns = column)
df.to_csv("cumulative_histogram.csv",index=False)