from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.loader import bot, db
from bot.config import Config
from bot.services.time_convert import convert_time
from bot.services.layout_fix import looks_like_wrong_layout, en_to_ru_layout

router = Router()


# 📌 Клавиатура для админа
def get_auth_keyboard(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="✅ Авторизовать", callback_data=f"auth:{user_id}"),
        InlineKeyboardButton(text="❌ Послать на хуй", callback_data=f"deny:{user_id}")
    )
    return builder.as_markup()


# 📎 Автор пересланного сообщения
def get_forward_author(msg: Message) -> str | None:
    if msg.forward_from:
        return msg.forward_from.full_name
    if msg.forward_sender_name:
        return msg.forward_sender_name
    return None


# 📌 Обработка сообщений от пользователей
@router.message()
async def handle_user(msg: Message):
    user_id = msg.from_user.id
    text = msg.text

    if not text:
        return

    text = text.strip()

    # 🔐 Проверка авторизации
    is_authorized = await db.is_user_authorized(user_id)

    if not is_authorized:
        await msg.answer("⛔ Вы не авторизованы. Ожидайте подтверждения от администратора.")
        await bot.send_message(
            Config.ADMIN_ID,
            f"❗ Новый пользователь:\n"
            f"<b>{msg.from_user.full_name}</b> (ID: <code>{user_id}</code>)",
            reply_markup=get_auth_keyboard(user_id)
        )
        return

    # ⌨️ FIX: неправильная раскладка (ТОЛЬКО для пересланных)
    if msg.forward_from or msg.forward_sender_name:
        if looks_like_wrong_layout(text):
            fixed_text = en_to_ru_layout(text)

            if fixed_text != text:
                author = get_forward_author(msg)

                if author:
                    reply_text = (
                        f"⌨️ Кажется, {author} писал:\n\n"
                        f"{fixed_text}"
                    )
                else:
                    reply_text = (
                        "⌨️ Похоже, сообщение набрано не в той раскладке:\n\n"
                        f"{fixed_text}"
                    )

                await msg.answer(reply_text)
                return

        # ⛔ Переслано, но это не раскладка и не время
        await msg.answer(
            "Я не понял запрос. Напиши время в формате HH или HH:MM."
        )
        return

    # ⏰ Основная логика (таймзоны) — обычные сообщения
    result = convert_time(text)
    await msg.answer(result)



# 📌 Админ: авторизовать пользователя
@router.callback_query(F.data.startswith("auth:"))
async def approve_user(callback: CallbackQuery):
    if callback.from_user.id != Config.ADMIN_ID:
        await callback.answer("⛔ Ты не админ.")
        return

    user_id = int(callback.data.split(":")[1])
    await db.authorize_user(user_id)

    await callback.message.edit_text(f"✅ Пользователь {user_id} авторизован.")
    await bot.send_message(
        user_id,
        "✅ Вы были авторизованы. Теперь можете пользоваться ботом!"
    )


# 📌 Админ: отказать пользователю
@router.callback_query(F.data.startswith("deny:"))
async def deny_user(callback: CallbackQuery):
    if callback.from_user.id != Config.ADMIN_ID:
        await callback.answer("⛔ Ты не админ.")
        return

    user_id = int(callback.data.split(":")[1])

    await callback.message.edit_text(f"❌ Пользователю {user_id} отказано.")
    await bot.send_message(
        user_id,
        "🚫 Вам отказано в доступе к боту."
    )
