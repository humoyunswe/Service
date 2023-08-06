from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default.formatter import starts
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"<b>Ассалому Алайкум {message.from_user.full_name}! Менга расм юборинг мен PDF килиб бераман.</b>",reply_markup=starts)


