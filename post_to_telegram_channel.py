import os
from dotenv import load_dotenv
import telegram
from fetch_comic import fetch_random_comic
from pathlib import Path


def publish_comic(bot, directory: str, channel_id: str) -> Path:
    image_path, caption = fetch_random_comic(folder=directory)

    with open(image_path, "rb") as photo:
        bot.send_photo(chat_id=channel_id, photo=photo, caption=caption)

    return image_path


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
        image_path = publish_comic(bot, directory="images", channel_id=channel_id)
    finally:
        if image_path and Path(image_path).exists():
            try:
                os.remove(image_path)
            except (FileNotFoundError, PermissionError) as error:
                print(f"Не удалось удалить изображение: {error}")


if __name__ == "__main__":
    main()
