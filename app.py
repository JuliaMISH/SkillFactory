import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
        text = 'Чтобы начать работу, введите команду боту в следующем формате (через пробел):\n<имя исходной валюты> \
<в какую валюту перевести> \
<количество валюты для конвертации>\n Доступные валюты: /values'
        bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
        text = 'Доступные валюты: '
        for key in keys.keys():
                text = '\n'.join((text, key, ))
        bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def get_price(message: telebot.types.Message):
        try:
                values = message.text.split(' ')

                if len(values) != 3:
                        raise APIException('Слишком много параметров')

                base, quote, amount = values
                total_quote = CryptoConverter.get_price(base, quote, amount)
        except APIException as e:
                bot.reply_to(message, f'Ошибка пользователя\n{e}')
        except Exception as e:
                bot.reply_to(message, f'Не удалось обработать команду\n{e}')
        else:
                text = f'Стоимость {amount} {base}ов в {quote}ах - {total_quote}'
                bot.send_message(message.chat.id, text)

bot.polling()