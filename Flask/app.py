 

from __future__ import division, print_function
# coding=utf-8
import sys
import os
import glob
import numpy as np

from tensorflow.keras.preprocessing import image 


from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions

from keras.models import load_model
from keras import backend

from tensorflow.keras import backend
#from tensorflow.keras.models import load_model

import tensorflow as tf

 # global graph
# graph=tf.get_default_graph()


from skimage.transform import resize

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Load your trained model
model = load_model("breastcancer.h5")
print('Model loaded. Check http://127.0.0.1:5000/')




@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('bcancer.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['image']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        img = image.load_img(file_path, target_size=(64, 64))
        
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
       #  with graph.as_default():
        preds = model.predict(x)
        if preds[0][0]==0:
            text = "The tumor is benign.. Need not worry!"
        else:
            text = "It is a malignant tumor... Please Consult Doctor"
        text = text
        
               # ImageNet Decode

        return text

if __name__ == '__main__':
    app.run(debug=False,threaded = False)
