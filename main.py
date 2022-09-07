import telebot
from config import keys, TOKEN
from extensions import ValueConverter, APIException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_message(message: telebot.types.Message):
    text = 'Для начала работы введите команду в следующем формате: \n <название валюты из которой переводим> \
<в какую валюту перевести>\
<количество переводимой валюты>\nСписок валют доступен по команде /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values_message(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise APIException('Слишком много параметров')
        elif len(values) < 3:
            raise APIException('Недостаточно параметров для конвертации')
        quote, base, amount = values
        total_base = ValueConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
