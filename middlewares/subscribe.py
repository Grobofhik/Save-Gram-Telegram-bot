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
        # 1. Пропускаем всё, что не является сообщением (на всякий случай)
        if not isinstance(event, types.Message):
            return await handler(event, data)

        # 2. Если в конфиге включен пропуск проверки — идем дальше
        # (Аналог твоего SKIP_SUBSCRIPTION_CHECK)
        if getattr(config, 'skip_subscription_check', False):
            return await handler(event, data)

        # 3. Сама проверка (аналог check_all_subscriptions)
        bot = data["bot"]
        user_id = event.from_user.id
        
        for channel_id in config.channels:
            if not channel_id:
                continue
            try:
                # Определяем chat_id для get_chat_member
                if isinstance(channel_id, str) and not channel_id.startswith('-100') and not channel_id.startswith('@'):
                    chat_id_for_check = f"@{channel_id}"
                else:
                    chat_id_for_check = channel_id
                
                member = await bot.get_chat_member(chat_id_for_check, user_id)
                
                # Если статус "left" или "kicked" — значит не подписан
                if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
                    await event.answer(
                        "<tg-emoji emoji-id='5377782951377379920'>🚫</tg-emoji> <b>Для использования бота подпишитесь на наши каналы:</b>",
                        reply_markup=self.get_sub_keyboard(),
                        parse_mode="HTML"
                    )
                    # ВАЖНО: не вызываем handler, выполнение кода тут остановится
                    return 
            except Exception as e:
                logger.error(f"Ошибка проверки подписки в {channel_id}: {e}")
                # Если канал не найден — пропускаем его, как в твоем коде
                if "chat not found" in str(e).lower():
                    continue
                # В остальных случаях можно либо пустить, либо блокировать. 
                # Твой код в main.py возвращает False (блокирует).
                return 

        # Если цикл прошел и блокировок не было — пускаем в обработчик
        return await handler(event, data)

    def get_sub_keyboard(self):
        """Создает инлайн-кнопки (аналог get_channels_keyboard)"""
        buttons = []
        for i, channel in enumerate(config.channels, start=1):
            if channel:
                # Определяем link_path для инлайн-кнопки
                if channel.startswith('-100'):
                    # Для числовых ID (приватные каналы), удаляем "-100" и используем "c/"
                    link_path = f"c/{channel[4:]}"
                else:
                    # Для публичных каналов (username), убираем '@' если есть
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