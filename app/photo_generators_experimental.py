import requests

from config import PHOTO_TOKEN

async def generator_photo(promt):
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/ultra",
        headers={
            "authorization": f"Bearer {PHOTO_TOKEN}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": promt,
            "output_format": "png",
        },
    )

    if response.status_code == 200:
        with open("output.png", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(f"Ошибка API: {response.status_code}, {response.text}")