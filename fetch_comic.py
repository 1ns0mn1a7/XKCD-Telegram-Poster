import requests
import json
import random
from pathlib import Path
from url_get_file_extension import get_file_extension
from download_tools import download_image


def get_latest_comic_id():
    response = requests.get("https://xkcd.com/info.0.json")
    response.raise_for_status()
    return response.json()["num"]


def fetch_comic(folder="images", comic_id=None):
    Path(folder).mkdir(parents=True, exist_ok=True)

    if comic_id is None:
        latest_id = get_latest_comic_id()
        comic_id = random.randint(1, latest_id)

    url = f"https://xkcd.com/{comic_id}/info.0.json"
    response = requests.get(url)
    response.raise_for_status()

    response_comic = response.json()

    image_url = response_comic["img"]
    extension = get_file_extension(image_url)
    filename = Path(folder) / f"xkcd_{comic_id}{extension}"

    download_image(image_url, filename)

    json_path = filename.with_suffix(".json")
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(response_comic, file, ensure_ascii=False, indent=2)

    return filename


def get_comic_text(image_path: Path) -> str:
    image_path = Path(image_path)
    json_path = image_path.with_suffix(".json")
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("alt", "")
    return ""
