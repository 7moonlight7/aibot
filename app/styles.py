import requests


URL = 'https://cdn.fusionbrain.ai/static/styles/key'

API_KEY = 'YOUR_API_KEY'
SECRET_KEY = 'YOUR_SECRET_KEY'


def get_styles():
    response = requests.get(URL)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка: {response.status_code}")
        return None

