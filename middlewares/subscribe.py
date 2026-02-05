from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware, types
from core.config import config

class SubscribeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any]
    ) -> Any:
        # We skip the /start command so that the user can see the subscription buttons.
        if event.text == "/start":
            return await handler(event, data)

        bot = data["bot"]
        for channel_id in config.channels:
            try:
                member = await bot.get_chat_member(channel_id, event.from_user.id)
                if member.status in ["left", "kicked"]:
                    await event.answer(
                        "🚫 **Для использования бота подпишитесь на каналы:**",
                        reply_markup=self.get_sub_keyboard()
                    )
                    return
            except Exception:
                continue
        
        return await handler(event, data)

    def get_sub_keyboard(self):
        buttons = [
            [types.InlineKeyboardButton(text=f"📢 Канал {i+1}", url=f"https://t.me/{c.lstrip('@')}")]
            for i, c in enumerate(config.channels)
        ]
        return types.InlineKeyboardMarkup(inline_keyboard=buttons)