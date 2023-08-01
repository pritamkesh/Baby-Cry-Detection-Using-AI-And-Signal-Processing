import os
import io
import base64
import numpy as np
import soundfile as sf
from keras.models import model_from_json
from python_speech_features import mfcc
from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask import render_template
import ast

app = Flask(__name__)
socketio = SocketIO(app)

with open('/Users/pkesh/projects/Exp-Research-POC/app3/cnn.json', 'r') as f:
    mymodel = model_from_json(f.read())

mymodel.load_weights("/Users/pkesh/projects/Exp-Research-POC/app3/cnn.h5")
    
@app.route('/')
def index():
    print("Index route triggered") 
    return render_template('index.html')


def Mfcc(raw_audio_data, sample_rate):
    s = np.array(raw_audio_data)

    x = np.array_split(s, 64)

    logg = np.zeros((64, 12))
    for i in range(len(x)):
        m = np.mean(mfcc(x[i], sample_rate, numcep=12, nfft=2048), axis=0)
        logg[i, :] = m

    return logg



def predict_single_file(raw_audio_data, sample_rate, model):
    mfcc_features = Mfcc(raw_audio_data, sample_rate)
    mfcc_features = np.expand_dims(mfcc_features, axis=0)
    prediction = model.predict(mfcc_features)
    print("Prediction value:", prediction)  # Add this line
    predicted_class = 1 if prediction >= 1 else 0  # Change the threshold to 0.5
    return predicted_class, prediction



@socketio.on('classify_live')
def classify_live(data):
    print("classify_live event received")
    audio_data = data['audio_data']
    print("audio_data:", audio_data)

    if not isinstance(audio_data, list):
        print("Invalid audio_data format")
        return

    raw_audio_data, sample_rate = sf.read(io.BytesIO(bytes(audio_data)))
    soundclass, raw_prediction = predict_single_file(raw_audio_data, sample_rate, mymodel)
    print("Sound class:", soundclass)  # Add this line

    if soundclass == 1:
        result = "Baby is crying."
        emit('classification_result', {'result': result})




if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)
