from flask import Flask, render_template, request, json, jsonify
import os
import json
import numpy as np
import io
from PIL import Image
import wiotp.sdk.application
import wiotp.sdk.device
import base64
import math

app = Flask(__name__)
app.config.from_object(__name__)
port = int(os.getenv('PORT', 8080))

@app.route("/", methods=['GET'])
def hello():
    error=None
    return render_template('index.html', error=error)

def myEventCallback(event):
    return json.dumps(event.data)

@app.route("/iot", methods=['GET'])
def result():    
    options = wiotp.sdk.application.parseConfigFile("app.yaml")
    client = wiotp.sdk.application.ApplicationClient(options)
    client.subscribeToDeviceEvents(typeId="maratona", deviceId="d9", eventId="sensor", msgFormat="json")
    client.connect()
    eventId = "sensor"
    device = {"typeId": "maratona", "deviceId": "d9"}

    data = client.lec.get(device, eventId)
    payload = data['payload']
    dt = json.loads(base64.b64decode(payload).decode('utf-8'))
    dt = dados['data']
    volume = ((4 * math.pi * 1**3) / 3) / 2

    resposta = {
        "iotData": dt,
        "itu": dt['temperatura'] - 0.55 * ( 1 - dt['umidade_ar'] ) * (dt['temperatura'] - 14),
        "volumeAgua": dt['umidade_solo'] * volume,
        "fahrenheit": dt['temperatura'] * 9/5 + 32
    }
    response = app.response_class(
        response=json.dumps(resposta),
        status=200,
        mimetype='application/json'
    )
    return response

def prepare_image(image):
    image = image.resize(size=(96,96))
    image = np.array(image, dtype="float") / 255.0
    image = np.expand_dims(image,axis=0)
    image = image.tolist()
    return image

@app.route('/predict', methods=['POST'])
def predict():
    print(request)
    image = request.files["image"].read()
    image = Image.open(io.BytesIO(image))
    image = prepare_image(image)

    # Faça uma requisição para o serviço Watson Machine Learning aqui e retorne a classe detectada na variável 'resposta'
    
    resposta = {
        "class": "data"
    }
    return resposta

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)