"""
Version: 0.0.1
Company: Sybrid Pvt. Ltd.

This file contains the code which returns the output Spectrograms which results for a flag if the call is Good or Unusual.

"""

from keras.models import model_from_json
import os
import pandas as pd
# from keras.preprocessing import image
import keras.utils as image
import numpy as np

import librosa.display
import librosa.util
from pathlib import Path

# load json and create model
json_file = open('Files/Model/model_MCD.json','r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights('Files/Model/model_MCD.h5')
print("Loaded model from disk")
print(loaded_model_json)


# Spectrogram Directory
test_dir = 'Files/Extracted_spectrograms'


x= os.listdir(test_dir)

# Binary train CSV
train = pd.read_csv("Files/Model/binary_train.csv")
os.chdir(test_dir)



# The following code is directly integrated in METADATA_Extractor.py

a = []

for file in x:
    # test a particular image
    img = image.load_img ( file , target_size = (400 , 400 , 3) )
    img = image.img_to_array ( img )
    img = img / 255

    classes = np.array ( train.columns[2:] )
    proba = loaded_model.predict ( img.reshape ( 1 , 400 , 400 , 3 ) )
    top_3 = np.argsort ( proba[0] )[:-4:-1]

    # print ( file )
    for i in range ( 1 ):
        a.append ( [classes[top_3[i]]] )
