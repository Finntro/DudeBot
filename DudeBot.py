import telebot
from datetime import datetime
import pymorphy2

bot = telebot.TeleBot('ТУТ ТОКЕН ТВОЕГО БОТА')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я Чювак Бот, и я люблю среды.', parse_mode='html')

@bot.message_handler()
def everyday_text(message): #Всегда возвращает текст, если видит слово "среда".
    morph = pymorphy2.MorphAnalyzer()
    lst = message.text.split()
    results = []
    for i in lst:
      parsed = morph.parse(i)
      norm_form = parsed[0].normal_form
      results.append(norm_form)
    if "среда" in results and datetime.today().weekday() != 2:
      bot.send_message(message.chat.id, "Среда – лучший день недели!\nОчень жду среду.", parse_mode='html')
    if "среда" in results and datetime.today().weekday() == 2:
      bot.send_message(message.chat.id, "Среда – лучший день недели!\nBtw, it's Wednesday, my dudes.", parse_mode='html')

bot.polling(none_stop=True)
