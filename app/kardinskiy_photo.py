import json
import time
import requests

from app.keyboards.inline import styles
from config import API_KEY_KARDINSKIY
from config import SECRET_KEY_KARDINSKIY


URL = 'https://api-key.fusionbrain.ai/'

AUTH_HEADERS = {
    'X-Key': f'Key {API_KEY_KARDINSKIY}',
    'X-Secret': f'Secret {SECRET_KEY_KARDINSKIY}',
}


def get_model():
    response = requests.get(URL + 'key/api/v1/models', headers=AUTH_HEADERS)
    data = response.json()
    return data[0]['id']



def generatee(prompt, model, styles, images=1, width=1024, height=1024):
    params = {
        "type": "GENERATE",
        "style": f"{styles}",
        "numImages": images,
        "width": width,
        "height": height,
        "generateParams": {
            "query": f"{prompt}"
        }
    }

    data = {
        'model_id': (None, model),
        'params': (None, json.dumps(params), 'application/json')
    }
    response = requests.post(URL + 'key/api/v1/text2image/run', headers=AUTH_HEADERS, files=data)
    data = response.json()
    return data['uuid']



def check_generation(request_id, attempts=10, delay=10):
    while attempts > 0:
        response = requests.get(URL + 'key/api/v1/text2image/status/' + request_id, headers=AUTH_HEADERS)
        data = response.json()
        if data['status'] == 'DONE':
            return data['images']

        attempts -= 1
        time.sleep(delay)




