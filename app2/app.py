import os
import numpy as np
import soundfile as sf
from keras.models import model_from_json
from python_speech_features import mfcc
from flask import Flask, request, jsonify
from flask import render_template

app = Flask(__name__)

with open('/Users/pkesh/projects/Exp-Research-POC/app2/cnn.json', 'r') as f:
    mymodel = model_from_json(f.read())

mymodel.load_weights("/Users/pkesh/projects/Exp-Research-POC/app2/cnn.h5")

def Mfcc(audiofile):
    s,r=sf.read(audiofile)
    
    x=np.array_split(s,64)
    
    logg=np.zeros((64,12))
    for i in range(len(x)):
        
        m=np.mean(mfcc(x[i],r, numcep=12,nfft=2048),axis=0)
        logg[i,:]=m

    return logg

def predict_single_file(file, model):
    # Extract MFCC features
    mfcc_features = Mfcc(file)

    # Reshape the MFCC features to match the input shape of the model
    mfcc_features = np.expand_dims(mfcc_features, axis=0)

    # Make a prediction using the model
    prediction = model.predict(mfcc_features)

    # Convert the prediction to class label
    predicted_class = 1 if prediction >= 0.5 else 0

    return predicted_class

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file provided'}), 400

    file_path = 'uploaded.wav'
    file.save(file_path)

    # Use the predict_single_file function to get the predicted class
    soundclass = predict_single_file(file_path, mymodel)

    os.remove(file_path)
    
    return jsonify({'soundclass': int(soundclass)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
