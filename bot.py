import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from openai import OpenAI

# Токени з середовища Railway
TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

# Ініціалізація бота
logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        'Привіт! Я — AI-асистент кафедри комп’ютерних наук.\nМожеш запитати мене про вступ, спеціальність, предмети чи інше.', 
        parse_mode='HTML'
    )

# Обробка тексту
@dp.message(lambda message: message.text)
async def filter_messages(message: Message):
    try:
        with open("info.txt", "r", encoding="utf-8") as f:
            reference_text = f.read()
    except FileNotFoundError:
        await message.answer("Не знайдено файл info.txt. Додайте файл у проєкт.")
        return

    client = OpenAI(
        base_url="https://api.langdock.com/openai/eu/v1",
        api_key=OPENAI_KEY
    )

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"Ти — AI-асистент кафедри комп’ютерних наук. Ось інформація, якою ти можеш користуватись:\n\n{reference_text}"
            },
            {
                "role": "user",
                "content": message.text
            }
        ]
    )

    response = completion.choices[0].message.content
    await message.answer(response, parse_mode="Markdown")

# Запуск
async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
