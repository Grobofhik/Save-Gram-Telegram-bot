from aiogram import Router, types, F
from aiogram.filters import Command
from core.config import config

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="📥 Скачать видео")],
        [types.KeyboardButton(text="ℹ️ Помощь")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    
    await message.answer(
        f"👋 **Привет!** Я бот для скачивания видео и аудио.\n"
        f"Просто отправь мне ссылку на контент из:\n\n"
        f"🔹 **YouTube**\n"
        f"🔸 **Pinterest**\n"
        f"🔹 **TikTok**\n"
        f"🔴 **(new!) Instagram**\n\n",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@router.message(F.text == "📥 Скачать видео")
async def ask_link(message: types.Message):
    await message.answer("Пришлите ссылку на видео 🔗", reply_markup=types.ReplyKeyboardRemove())

@router.message(F.text == "ℹ️ Помощь")
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "📝 **Как пользоваться ботом:**\n"
        "1. Скопируйте ссылку на видео.\n"
        "2. Вставьте её в чат с ботом.\n"
        "3. Дождитесь загрузки и получите файл!\n\n"
        "⚠️ Лимит на размер файла: 50 МБ (для видео).",
        parse_mode="Markdown"
    )