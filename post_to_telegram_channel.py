import os
from dotenv import load_dotenv
import telegram
from fetch_comic import get_comic_text, fetch_comic
from pathlib import Path


def publish_photo(bot, directory: str, channel_id: str):
    image_path = fetch_comic(folder=directory)
    caption = get_comic_text(image_path)

    send_photo_to_channel(bot, image_path, channel_id, caption)

    try:
        os.remove(image_path)
    except Exception as error:
        print(f"Не удалось удалить изображение: {error}")

    json_path = Path(image_path).with_suffix(".json")
    if json_path.exists():
        try:
            json_path.unlink()
        except Exception as error:
            print(f"Не удалось удалить JSON: {error}")


def send_photo_to_channel(bot, photo_path: str, chat_id: str, caption: str = ""):
    with open(photo_path, "rb") as photo:
        bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)


def main():
    load_dotenv()
    bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")

    publish_photo(bot, directory="images", channel_id=channel_id)


if __name__ == "__main__":
    main()
