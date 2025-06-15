import requests


def download_image(url, filename):
    img_response = requests.get(url, timeout=10)
    img_response.raise_for_status()
    with open(filename, "wb") as file:
        file.write(img_response.content)
