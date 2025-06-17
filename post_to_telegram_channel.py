import os
from dotenv import load_dotenv
import telegram
from fetch_comic import fetch_random_comic
from pathlib import Path


def get_comic(directory: str):
    return fetch_random_comic(folder=directory)


def publish_comic(bot, channel_id: str, image_path: Path, caption: str):
    with open(image_path, "rb") as photo:
        bot.send_photo(chat_id=channel_id, photo=photo, caption=caption)


def main():
    load_dotenv()
    Path("images").mkdir(parents=True, exist_ok=True)

    try:
        bot = telegram.Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
        channel_id = os.environ["TELEGRAM_CHANNEL_ID"]
    except KeyError as error:
        print(f"Не найдена обязательная переменная окружения: {error}")
        return

    image_path = None
    try:
        image_path, caption = get_comic("images")
        publish_comic(bot, channel_id, image_path, caption)
    finally:
        if image_path and Path(image_path).exists():
            try:
                os.remove(image_path)
            except (FileNotFoundError, PermissionError) as error:
                print(f"Не удалось удалить изображение: {error}")


if __name__ == "__main__":
    main()
