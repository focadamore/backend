import asyncio
from time import sleep

from fastapi import UploadFile
from PIL import Image
import os

from src.database import async_session_maker, async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


@celery_instance.task
def test_task():
    sleep(5)
    print("Тестовая таска завершена")


@celery_instance.task
def resize_image(image_path: str):
    target_widths = [1000, 500, 200]
    output_folder = "src/static/images"

    image = Image.open(image_path)

    saved_paths = []

    for width in target_widths:
        ratio = width / float(image.width)
        height = int(float(image.height) * ratio)

        resized_image = image.resize((width, height), Image.LANCZOS)

        base_name = os.path.basename(image_path)
        filename, ext = os.path.splitext(base_name)
        new_filename = f"{filename}_{width}{ext}"
        output_path = os.path.join(output_folder, new_filename)

        resized_image.save(output_path, quality=85)

        saved_paths.append(output_path)
        print("Формирование картинки")

    return saved_paths


async def get_today_checkin_helper():
    print("Я ЗАПУСКАЮСЬ")
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        bookings = await db.bookings.get_today_checkin()
        print(f"{bookings=}")


@celery_instance.task(name="bookings_today_checkin")
def send_email_to_users_with_today_checkin():
    asyncio.run(get_today_checkin_helper())
