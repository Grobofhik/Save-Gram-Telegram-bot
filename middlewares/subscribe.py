from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware, types
from aiogram.enums.chat_member_status import ChatMemberStatus
from core.config import config
import logging

logger = logging.getLogger(__name__)

class SubscribeMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any]
    ) -> Any:
        if not isinstance(event, types.Message):
            return await handler(event, data)

        if getattr(config, 'skip_subscription_check', False):
            return await handler(event, data)

        bot = data["bot"]
        user_id = event.from_user.id
        
        for channel_id in config.channels:
            if not channel_id:
                continue
            try:
                if isinstance(channel_id, str) and not channel_id.startswith('-100') and not channel_id.startswith('@'):
                    chat_id_for_check = f"@{channel_id}"
                else:
                    chat_id_for_check = channel_id
                
                member = await bot.get_chat_member(chat_id_for_check, user_id)
                
                if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                    await event.answer(
                        "<tg-emoji emoji-id='5377782951377379920'>🚫</tg-emoji> <b>Для использования бота подпишитесь на наши каналы:</b>",
                        reply_markup=self.get_sub_keyboard(),
                        parse_mode="HTML"
                    )
                    return 
            except Exception as e:
                logger.error(f"Ошибка проверки подписки в {channel_id}: {e}")
                if "chat not found" in str(e).lower():
                    continue
                return 

        return await handler(event, data)

    def get_sub_keyboard(self):
        buttons = []
        for i, channel in enumerate(config.channels, start=1):
            if channel:
                if channel.startswith('-100'):
                    link_path = f"c/{channel[4:]}"
                else:
                    link_path = channel.lstrip('@')

                buttons.append([
                    types.InlineKeyboardButton(
                        text=f"Подписаться на канал {i}", 
                        url=f"https://t.me/{link_path}",
                        icon_custom_emoji_id='5474359500095890971',
                        style='primary'
                    )
                ])
        return types.InlineKeyboardMarkup(inline_keyboard=buttons)