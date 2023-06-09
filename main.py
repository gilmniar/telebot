import telebot
from config import tg_bot_token
from extensions import APIException, Exchanger

bot = telebot.TeleBot(tg_bot_token)


@bot.message_handler(commands=['start'])
def command_start(message: telebot.types.Message):
    bot.reply_to(message, 'Здравствуйте! Бот предназначен для удобного перевода курсов валют, для более подробной '
                          'информации введите /help')


@bot.message_handler(commands=['help'])
def command_help(message: telebot.types.Message):
    bot.reply_to(message, 'Введите сообщение в формате(ВАЖНО!Вводите имя валюты в именительном падеже)'
                          '<имя валюты, цену которой вы желаете узнать> '
                          '<имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>.'
                          'Чтобы узнать валюты, которые доступны для перевода введите /values')


@bot.message_handler(commands=['values'])
def command_values(message: telebot.types.Message):
    bot.reply_to(message, 'Валюты доступные для перевода: Доллар, Евро, Юань, Рубль')


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) > 3:
            raise APIException("Слишком много значений")

        quote, base, amount = values
        total_base = Exchanger.exchange(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n {e}')
    else:
        text = f"Цена {amount} {quote} в {base} - {total_base['result']}"
        bot.send_message(message.chat.id, text)


bot.polling()
