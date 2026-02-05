import os
import logging
from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext

# Importing the universal service and config
from services.ydl_service import ydl_service
from core.config import config

router = Router()
logger = logging.getLogger(__name__)

# Handler for handling Pinterest links.
async def download_and_send_video(message: types.Message, state: FSMContext):
   
    url = message.text.strip()
    
    status_msg = await message.answer("🌐 **Pinterest:** Начинаю загрузку видео... ⏳", parse_mode="Markdown")
    
    # Pinterest-specific settings (converting to mp4 via ffmpeg)
    pinterest_opts = {
        'format': 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
    }

    try:
        file_path = await ydl_service.download_video(url, pinterest_opts)

        if file_path and os.path.exists(file_path):
            caption = config.CAPTION_TEMPLATE.format(username=config.BOT_USERNAME.lstrip('@'))
            
            await message.answer_video(
                video=FSInputFile(file_path),
                caption=caption,
                parse_mode="Markdown" 
            )
            
            # Delete the status message and temporary file
            await status_msg.delete()
            os.remove(file_path)
            logger.info(f"Видео Pinterest успешно отправлено и удалено: {file_path}")
            
        else:
            await status_msg.edit_text(
                "❌ **Pinterest:** Не удалось скачать видео. Попробуйте другую ссылку."
            )

    except Exception as e:
        logger.error(f"Ошибка в хендлере Pinterest: {e}")
        await status_msg.edit_text("❌ **Pinterest:** Произошла ошибка при обработке видео.")