import os
import logging
import asyncio
import shutil
from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import F
from dotenv import load_dotenv

from services.pinterest_downloader import download_pinterest_media
from core.config import config

load_dotenv()
BOT_USERNAME = os.getenv("BOT_USERNAME")

router = Router()
logger = logging.getLogger(__name__)

# Handler for handling Pinterest links.
@router.message(F.text.regexp(r'^(https?://)?(www\.)?(pinterest\.com|pin\.it)/.+'))
async def download_and_send_pinterest_media(message: types.Message, state: FSMContext):
    url = message.text.strip()
    user_id = message.from_user.id
    
    status_message = await message.reply("🌐 **Pinterest:** Начинаю загрузку ⏳", parse_mode="Markdown")
    
    try:
        downloaded_file = await download_pinterest_media(url, user_id)

        if downloaded_file and os.path.exists(downloaded_file):
            bot_link = f"https://t.me/{BOT_USERNAME.lstrip('@')}" 
            caption_template = f"[Скачать любую песню или видео🎧]({bot_link})"

            # Determine content type
            if downloaded_file.lower().endswith(('.mp4', '.mov', '.webm')):
                await message.answer_video(
                    video=FSInputFile(downloaded_file),
                    caption=caption_template,
                    parse_mode="Markdown"
                )
            else:
                await message.answer_photo(
                    photo=FSInputFile(downloaded_file),
                    caption=caption,
                    parse_mode="Markdown"
                )
            
            await status_message.delete()
            logger.info(f"Медиа Pinterest успешно отправлено: {downloaded_file}")
            
        else:
            await status_message.edit_text(
                "❌ **Pinterest:** Не удалось скачать медиа. Возможно, ссылка ведет на защищенный контент."
            )

    except Exception as e:
        logger.error(f"Ошибка в хендлере Pinterest: {e}")
        await status_message.edit_text("❌ **Pinterest:** Произошла ошибка при обработке ссылки.")
    finally:
        # Clean up the downloaded directory after sending
        download_dir = f"downloads/pin_{user_id}"
        if os.path.exists(download_dir):
            try:
                shutil.rmtree(download_dir)
                logger.info(f"Временная директория {download_dir} успешно удалена.")
            except Exception as e:
                logger.error(f"Ошибка при очистке временной директории {download_dir}: {e}")