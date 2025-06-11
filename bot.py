import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from openai import OpenAI

TOKEN = '7978959289:AAFBX-ze9OAZ5xjDJjJEWRGzPhbOIdbp7Oc'

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

# Обробка тексту з урахуванням файлу info.txt
@dp.message(lambda message: message.text)
async def filter_messages(message: Message):
    # Зчитування довідкової інформації з файлу
    try:
        with open("info.txt", "r", encoding="utf-8") as f:
            reference_text = f.read()
    except FileNotFoundError:
        await message.answer("Не знайдено файл info.txt. Додайте файл у папку з ботом.")
        return

    # Підключення до Langdock API
    client = OpenAI(
        base_url="https://api.langdock.com/openai/eu/v1",
        api_key="sk-EFdTuhcTkb69o7ONQ0SAKcs97e53Y_fVuu0_adcbmrHUgUntDx7DXZULBbb-MwKHPg7zj9vXJBRqBEv7BVcblQ"
    )

    # Надсилання запиту з контекстом
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": f"Ти — AI-асистент кафедри комп’ютерних наук. Ось інформація, якою ти можеш користуватись для відповіді:\n\n{reference_text}"
            },
            {
                "role": "user",
                "content": message.text
            }
        ]
    )

    # Відповідь користувачу
    text = completion.choices[0].message.content
    await message.answer(text, parse_mode="Markdown")

# Запуск бота
async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
