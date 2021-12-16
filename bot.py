# Python telegram bot "Exchange rates".
# Powered by Nikita Rybkin.
import logging

from aiogram import Bot, Dispatcher, executor, types

import config


# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=config.API_TOKEN, proxy=config.PROXY_URL)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\n" +
                        "Я бот курса валют.\n" +
                        "Я показываю текущий курс денежных валют и криптовалют.\n" +
                        "Мой создатель - Никита Рыбкин.")


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await message.answer("Команды бота:\n" +
                         "/help - просмотр команд бота\n" +
                         "/info - информационное сообщение\n")


@dp.message_handler(commands=['info'])
async def information_message(message: types.Message):
    await message.answer("Я беру курс валют с сайта Центрального Банка России\n" +
                         "(https://www.cbr.ru)\n" +
                         "Обновляется раз в день\n\n" + 
                         "Курс криптоволюты беру с сайта\n" +
                         "(https://www.cryptocompare.com)\n" +
                         "Обновляется каждые 15 секунд",
                         disable_web_page_preview=True)


@dp.message_handler()
async def unknown_message(message: types.Message):
    await message.reply("Не знаю данную команду!\n" +
                        "Введите /help для просмотра команд бота.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
