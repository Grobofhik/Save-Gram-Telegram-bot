from aiogram import Router, types, F
from aiogram.filters import Command
from core.config import config

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="📥 Скачать видео", style='success')],
        [types.KeyboardButton(text="ℹ️ Помощь")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        f"<tg-emoji emoji-id='5377439736245790091'>👋</tg-emoji> <b>Привет!</b> Я бот для скачивания видео и аудио.\n"
        f"Просто отправь мне ссылку на контент из:\n\n"
        f"<tg-emoji emoji-id='5152129054727472184'>🔹</tg-emoji> <b>YouTube</b>\n"
        f"<tg-emoji emoji-id='5377686550836433982'>🔸</tg-emoji> <b>Pinterest</b>\n"
        f"<tg-emoji emoji-id='4976864431653782935'>🔹</tg-emoji> <b>TikTok</b>\n"
        f"<tg-emoji emoji-id='5102852233515500814'>🔴</tg-emoji> <b>(new!) Instagram</b>\n\n"
        f"<blockquote>Теперь можно в любой момент отправить ссылку. Писать команду /start больше не нужно</blockquote>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@router.message(F.text == "📥 Скачать видео")
async def ask_link(message: types.Message):
    await message.answer("Пришлите ссылку на видео 🔗", reply_markup=types.ReplyKeyboardRemove())

@router.message(F.text == "ℹ️ Помощь")
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "<tg-emoji emoji-id='5217465016357248073'>📝</tg-emoji> <b>Как пользоваться ботом:</b>\n\n"
        "<b>1. Скопируйте ссылку на видео.</b>\n"
        "<b>2. Вставьте её в чат с ботом.</b>\n"
        "<b>3. Дождитесь загрузки и получите файл!</b>\n\n"
        "<blockquote>⚠️ Лимит на размер файла: 50 МБ (для видео).</blockquote>",
        parse_mode="HTML"
    )