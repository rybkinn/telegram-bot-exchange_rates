# Python telegram bot "Exchange rates".
# Powered by Nikita Rybkin.
import logging
import datetime
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ParseMode

import config
import parse_sites
import keyboards


# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
if os.getenv('TELEGRAM_BOT_EXCHANGE_RATES') is None:
    bot = Bot(token=config.API_TOKEN, proxy=config.PROXY_URL)
else:
    bot = Bot(token=os.getenv('TELEGRAM_BOT_EXCHANGE_RATES'))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("📌Выберете действие:\n",
                        reply_markup=keyboards.menu_keyboard)


@dp.callback_query_handler(text = 'course_btn')
async def course_callback_handler(callback_query: types.CallbackQuery):

    date = datetime.datetime.now().date().strftime("%d.%m.%Y")

    cryptocurrencies = ("BTC", "ETH")
    towards = ("USD", "RUR")

    monetary_rates = parse_sites.parse_monetary_currency()
    crypto_rates = parse_sites.parce_cryptocurrency(cryptocurrencies, towards)
    return_text = f"{date}\n\n" + \
                  "Курс валют (к рублю):\n" + ("=" * 20) + "\n" + monetary_rates + \
                  "\n\n" + \
                  "Курс криптовалют:\n" + ("=" * 17) + "\n" + crypto_rates

    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(text=return_text,
                                chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                parse_mode=ParseMode.HTML,
                                reply_markup=keyboards.back_keyboard)

@dp.callback_query_handler(text = 'info_btn')
async def info_callback_handler(callback_query: types.CallbackQuery):

    return_text = "Я беру курс валют с сайта Центрального Банка России\n" + \
                  "(https://www.cbr.ru)\n" + \
                  "Обновляется раз в день\n\n" + \
                  "Курс криптоволюты беру с сайта\n" + \
                  "(https://www.cryptocompare.com)\n" + \
                  "Обновляется каждые 15 секунд\n" + \
                  ("-" * 50) + "\n" + \
                  "Мой создатель - Никита Рыбкин"

    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(text=return_text,
                                chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                disable_web_page_preview=True,
                                reply_markup=keyboards.back_keyboard)

@dp.callback_query_handler(text = 'back_btn')
async def back_callback_handler(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.edit_message_text(text="📌Выберете действие:\n",
                                chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                reply_markup=keyboards.menu_keyboard)


@dp.message_handler()
async def user_message(message: types.Message):
    await message.reply("❌Я вас не понимаю!\n")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
