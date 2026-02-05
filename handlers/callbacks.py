from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from handlers.youtube import download_and_send_video as yt_dl_process

router = Router()

@router.callback_query(F.data.startswith("yt_format:"))
async def yt_callback(callback: types.CallbackQuery, state: FSMContext):
    
    await callback.answer() 

    selected_format = callback.data.split(":")[1]
    data = await state.get_data()
    url = data.get("youtube_url")

    if not url:
        await callback.message.answer("Ошибка: ссылка потеряна. Отправьте её еще раз.")
        return

    await callback.message.edit_text("⏳ Видео добавлено в очередь на скачивание...")
    
    await yt_dl_process(callback.message, state, url, selected_format)