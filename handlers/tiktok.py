import os
import logging
from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext
from services.ydl_service import ydl_service
from core.config import config

router = Router()
logger = logging.getLogger(__name__)

# Handler for processing TikTok links.
async def download_and_send_video(message: types.Message, state: FSMContext):

    url = message.text.strip()
    # We send a status message that we will edit or delete.
    status_msg = await message.answer("🌐 **TikTok:** Начинаю загрузку видео... ⏳", parse_mode="Markdown")
    
    tiktok_opts = {
        'format': 'best[ext=mp4]/best',
        #'cookiefile': 'tiktok_cookies.txt', # Uncomment if you use cookies
    }

    try:
        file_path = await ydl_service.download_video(url, tiktok_opts)

        if file_path and os.path.exists(file_path):
        
            bot_link = f"https://t.me/{config.BOT_USERNAME.lstrip('@')}" 
            caption_template = f"[Скачать любую песню или видео🎧]({bot_link})"
            
            await message.answer_video(
                video=FSInputFile(file_path),
                caption=caption_templateYt,
                parse_mode="Markdown" 
            )
            
            await status_msg.delete()
           
            os.remove(file_path)
            logger.info(f"Видео TikTok успешно отправлено и удалено: {file_path}")
        else:
            await status_msg.edit_text("❌ **TikTok:** Не удалось скачать видео. Возможно, ссылка неверна или видео скрыто.")

    except Exception as e:
        logger.error(f"Ошибка в хендлере TikTok: {e}")
        await status_msg.edit_text("❌ **TikTok:** Произошла непредвиденная ошибка при обработке видео.")
