# Python telegram bot "Exchange rates".
# Powered by Nikita Rybkin.
import logging

from aiogram import Bot, Dispatcher, executor, types

import config
import parse_sites


# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
bot = Bot(token=config.API_TOKEN, proxy=config.PROXY_URL)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет!\n" +
                        "Я бот курса валют.\n" +
                        "Я показываю текущий курс денежных валют и криптовалют.\n\n" +
                        "Напиши - 'курс' чтобы получить текущий курс.\n" + 
                        "/help чтобы узнать больше команд")


@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    await message.answer(
        "Команды бота:\n" +
        "/help - просмотр команд бота.\n" +
        "/info - информационное сообщение.\n" +
        "Вывести все курсы - курс|курсы|курсы валют|все курсы.\n" +
        "Вывести денежные курсы - денежный курс|курс денег.\n" +
        "Вывести криптовалютные курсы - крипто курс|крипта|\n   курс криптовалют|курс крипты.\n")


@dp.message_handler(commands=['info'])
async def information_message(message: types.Message):
    await message.answer("Я беру курс валют с сайта Центрального Банка России\n" +
                         "(https://www.cbr.ru)\n" +
                         "Обновляется раз в день\n\n" + 
                         "Курс криптоволюты беру с сайта\n" +
                         "(https://www.cryptocompare.com)\n" +
                         "Обновляется каждые 15 секунд\n" +
                         ("-" * 30) + "\n" +
                         "Мой создатель - Никита Рыбкин",
                         disable_web_page_preview=True)


@dp.message_handler()
async def user_message(message: types.Message):
    curse_all = ('курс', 'курсы', 'курсы валют', 'все курсы')
    curse_monetary = ('денежный курс', 'курс денег')
    curse_crypto = ('крипто курс', 'крипта', 'курс криптовалют', 'курс крипты')

    cryptocurrencies = ("BTC", "ETH")
    towards = ("USD", "RUR")

    if message.text in curse_all:
        monetary_rates = parse_sites.parse_monetary_currency()
        crypto_rates = parse_sites.parce_cryptocurrency(cryptocurrencies, towards)
        return_text = "Курс валют:\n" + ("=" * 10) + "\n" + monetary_rates + \
                      "\n\n" + \
                      "Курс криптовалют:\n" + ("=" * 16) + "\n" + crypto_rates
        await message.answer(return_text)
    elif message.text in curse_monetary:
        await message.answer(parse_sites.parse_monetary_currency())
    elif message.text in curse_crypto:
        await message.answer(parse_sites.parce_cryptocurrency(cryptocurrencies, towards))
    else:
        await message.reply("Не знаю данную команду!\n" +
                            "Введите /help для просмотра команд бота.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
