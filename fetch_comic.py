import requests
import random
from pathlib import Path
from url_get_file_extension import get_file_extension
from download_tools import download_image


def get_latest_comic_id():
    response = requests.get("https://xkcd.com/info.0.json")
    response.raise_for_status()
    return response.json()["num"]


def get_random_comic_id():
    latest_id = get_latest_comic_id()
    return random.randint(1, latest_id)


def fetch_random_comic(folder):
    comic_id = get_random_comic_id()
    url = f"https://xkcd.com/{comic_id}/info.0.json"

    response = requests.get(url)
    response.raise_for_status()
    comic_response = response.json()

    image_url = comic_response["img"]
    alt_text = comic_response.get("alt", "")

    extension = get_file_extension(image_url)
    filename = Path(folder) / f"xkcd_{comic_id}{extension}"

    download_image(image_url, filename)
    return filename, alt_text
