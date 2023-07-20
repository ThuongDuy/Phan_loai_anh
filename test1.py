import numpy as np 
import pandas as pd 
import os
import cv2
import math
from sklearn.linear_model import SGDClassifier
from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
import imutils
from pathlib import Path
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
    H=[]
    for i in range(len(color)):
        H.append(0)
    img = cv2.imread(img_path)
    (h, w, d) = img.shape
    for i in range(h):
        for j in range(w):
            D=[]
            for k in color:
                D.append(distance(color[k],img[i,j]))
            H[min_distance(D)] = H[min_distance(D)]+1
    s = sum(H)
    for i in range(len(H)):
        H[i] = H[i]/s
    return H
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
    # cell_x = 8
    # cell_y = 8
    # bin_num=9
    # histogram = np.zeros([h/cell_y, w/cell_x, bin_num])
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
def key_min(dict,min_values):
    for i in dict:
        if dict[i]==min_values:
            return i

def find(dict,values):
    for i in dict:
        if dict[i]==values:
            return i
base_path = Path(__file__).parent
path = (base_path / "../csdl_dpt/anh_test").resolve()
anh= os.listdir(os.path.expanduser(path))
arr=[]

data=pd.read_csv('feature.csv')
data=data.values

lable = pd.read_csv('lable.csv')
lable = dict([(i,[x]) for i,x in zip(lable['anh'], lable['lable'])])
Y_pred=[]
for i in anh:
    p = str(path)+'\\'+i
    arr1=kmec(p)
    arr2=cumulative_histogram(p)
    arr3=hog(p,8,8,9,2)
    arr3=arr3.tolist()
    a=arr1+arr2+arr3
    dis={}
    count=0
    for j in lable:
        dis[j]=distance(a,data[count])
        count=count+1
    m=find(dis,min(dis.values()))
    Y_pred.append(lable[m][0])
print(Y_pred)
thuc=  [2, 2, 2, 2, 1, 0, 2, 2, 0, 1, 2, 0, 2, 2, 1, 0, 2, 1]
d=0
s=0
for i in range(len(Y_pred)):
    if Y_pred[i]==thuc[i]:
        d=d+1
    else:
        s=s+1
print('Accuracy: ',d/(d+s))

