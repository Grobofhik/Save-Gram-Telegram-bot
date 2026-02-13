from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

# Importing functions from your modules
from handlers.youtube import show_format_menu
from handlers.tiktok import download_and_send_video as tiktok_dl
from handlers.instagram import download_and_send_video as instagram_dl

router = Router()

@router.message(F.text.regexp(r'^(https?://[^\s]+)'))
async def link_handler(message: types.Message, state: FSMContext):
    url = message.text.strip()
    
    # YouTube
    if any(domain in url for domain in ["youtube.com", "youtu.be"]):
        await state.update_data(youtube_url=url)
        await show_format_menu(message)
    
    # TikTok
    elif "tiktok.com" in url:
        await tiktok_dl(message, state)
        
    # Instagram
    elif "instagram.com" in url:
        await instagram_dl(message, state)
        
    else:
        await message.reply("😔 Извини, я не поддерживаю эту платформу.")