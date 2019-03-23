import urllib 
import requests
#import time
import cv2
import numpy as np
import os
from scipy.misc import toimage
#url of ip cam
url="https://192.168.43.1:8080/shot.jpg"
frames=[]

try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print('Error: creating directory of data')

currentFrame=0

while(True):
    img_resp=requests.get(url,verify=False) 
    img_array=np.array(bytearray(img_resp.content),dtype=np.uint8)
    img=cv2.imdecode(img_array,-1)
    img=cv2.resize(img,(224,224))
    cv2.imshow('Android',img)
    file_name_path='C:/Users/HP/Desktop/data/frame'+str(currentFrame)+'.jpg'
    cv2.imwrite(file_name_path, img)
    cv2.destroyAllWindows()
    if cv2.waitKey(0)==13 or currentFrame==50:
        break
    currentFrame+=1
