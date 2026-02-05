import os
import logging
from aiogram import Router, types
from aiogram.types import FSInputFile
from aiogram.fsm.context import FSMContext

from services.ydl_service import ydl_service
from core.config import config

router = Router()
logger = logging.getLogger(__name__)

# Handler for processing Instagram links (Reels, Video).
async def download_and_send_video(message: types.Message, state: FSMContext):
    url = message.text.strip()
    
    # Sending a status message
    status_msg = await message.answer("🌐 **Instagram:** Начинаю загрузку видео... ⏳", parse_mode="Markdown")
    
    # Instagram-specific settings
    instagram_opts = {
        'format': 'best',
        # You can add cookies or headers here if needed.
    }

    try:
        # We call the universal service (it will return the exact path to the file with the UUID)
        file_path = await ydl_service.download_video(url, instagram_opts)

        if file_path and os.path.exists(file_path):
            # Use a single signature template from config.py
            caption = config.CAPTION_TEMPLATE.format(username=config.BOT_USERNAME.lstrip('@'))
            
            # Sending the result to the user
            await message.answer_video(
                video=FSInputFile(file_path),
                caption=caption,
                parse_mode="Markdown" 
            )
            
            # Delete the status message and temporary file
            await status_msg.delete()
            os.remove(file_path)
            logger.info(f"Видео Instagram успешно отправлено и удалено: {file_path}")
            
        else:
            await status_msg.edit_text(
                "❌ **Instagram:** Не удалось скачать видео. Убедитесь, что профиль открыт и ссылка верна."
            )

    except Exception as e:
        logger.error(f"Ошибка в хендлере Instagram: {e}")
        await status_msg.edit_text("❌ **Instagram:** Произошла ошибка при обработке видео.")