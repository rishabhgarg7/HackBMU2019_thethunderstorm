import os
os.chdir('/home/rishabh/')
import warnings
warnings.filterwarnings('ignore')
import urllib 
import requests
#import time
import cv2
import numpy as np
import os
from scipy.misc import toimage

import os
os.chdir('/home/rishabh')
from keras.models import load_model,Model
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input
from keras.layers import Input , add , LSTM , Embedding, Dropout,Dense
from keras.preprocessing import image
import numpy as np
import pickle
import pyttsx3
from keras.preprocessing.sequence import pad_sequences

embedding_dim = 200
max_length = 34
vocab_size = 8763
model_inc = InceptionV3(weights='imagenet')
# Create a new model, by removing the last layer (output layer) from the inception v3
model_new = Model(model_inc.input, model_inc.layers[-2].output)
# Function to encode a given image into a vector of size (2048, )

def preprocess(image_path):
    # Convert all the images to size 299x299 as expected by the inception v3 model
    img = image.load_img(image_path, target_size=(299, 299))
    # Convert PIL image to numpy array of 3-dimensions
    x = image.img_to_array(img)
    # Add one more dimension
    x = np.expand_dims(x, axis=0)
    # preprocess the images using preprocess_input() from inception module
    x = preprocess_input(x)
    return x

def encode(image):
    image = preprocess(image) # preprocess the image
    fea_vec = model_new.predict(image) # Get the encoding vector for the image
    fea_vec = np.reshape(fea_vec, fea_vec.shape[1]) # reshape from (1, 2048) to (2048, )
    return fea_vec.reshape(1,-1)

def greedySearch(photo):
    in_text = 'startseq'
    for i in range(max_length):
        sequence = [wordtoix[w] for w in in_text.split() if w in wordtoix]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = model.predict([photo,sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = ixtoword[yhat]
        in_text += ' ' + word
        if word == 'endseq':
            break
    final = in_text.split()
    final = final[1:-1]
    final = ' '.join(final)
    return final
down = '/home/rishabh/Downloads/'
file_reader = open(down + "w_ix.pkl",'rb')
wordtoix = pickle.load(file_reader)

file_reader = open(down + 'ix_w.pkl','rb')
ixtoword = pickle.load(file_reader)

model = load_model('/home/rishabh/Downloads/model1.h5')






#url of ip cam
url="https://192.168.43.1:8080/shot.jpg"
frames=[]

try:
    if not os.path.exists('data'):
        os.makedirs('data')
except OSError:
    print('Error: creating directory of data')

currentFrame=0
dim = (299,299)
#cap = cv2.VideoCapture('/home/rishabh/Downloads/video.mp4')
while(True):
    img_resp=requests.get(url,verify=False) 
    img_array=np.array(bytearray(img_resp.content),dtype=np.uint8)
    img=cv2.imdecode(img_array,-1)
    #cap = cv2.VideoCapture('/home/rishabh/Downloads/video.mp4')
    """ret,frame = cap.read()
    if ret ==False:
        break"""
    img=cv2.resize(img,dim, interpolation = cv2.INTER_AREA)
    currentFrame+=1
    #cv2.imshow('Android',img)
    if currentFrame%30==0:
        file_name_path = '/home/rishabh/Desktop/data/frame'+str(currentFrame)+'.jpg'
        cv2.imwrite(file_name_path, img)
        text = greedySearch(encode(file_name_path))
        print(text)

        engine = pyttsx3.init()
        engine.say(text)
        engine.setProperty('rate',100)
        engine.setProperty('volume', 0.9)
        engine.runAndWait()
        #cv2.imwrite(file_name_path, img)
        print(currentFrame)
        if (cv2.waitKey(0)) == 27 or currentFrame>=150:
            cv2.destroyAllWindows()
            break
   