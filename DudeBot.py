import telebot
from datetime import datetime
import pymorphy2

bot = telebot.TeleBot('5365438885:AAEgTY3EQHx4wzM8J6ChnyMOB-BFnBXV0Hc')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я Чювак Бот, и я люблю среды.', parse_mode='html')
@bot.message_handler()
def game(message):
    if message.text.lower() == "играть":
       bot.send_message(message.chat.id, "Сыграем в WEDNESDAY? Я хожу первый.", parse_mode='html')
       msg = bot.send_message(message.chat.id, "W", parse_mode='html')
       bot.register_next_step_handler(msg,turn1)
def turn1(message):
    if message.text == "E":
       msg = bot.send_message(message.chat.id, "D", parse_mode='html')
       bot.register_next_step_handler(msg, turn2)
    elif message.text == "Е":
       bot.send_message(message.chat.id, "Это кириллица, умник. \n\nТы проиграл.", parse_mode='html')
    else:
        bot.send_message(message.chat.id, 'Ты проиграл.', parse_mode='html')
def turn2(message):
    if message.text == "N":
       msg = bot.send_message(message.chat.id, 'E', parse_mode='html')
       bot.register_next_step_handler(msg, turn3)
    else:
       bot.send_message(message.chat.id, 'Ты проиграл.', parse_mode='html')
def turn3(message):
    if message.text == "S":
       msg = bot.send_message(message.chat.id, 'D', parse_mode='html')
       bot.register_next_step_handler(msg, turn4)
    else:
       bot.send_message(message.chat.id, 'Ты проиграл.', parse_mode='html')
def turn4(message):
    if message.text == "A":
       bot.send_message(message.chat.id, 'Y \n\nGood game, well played!', parse_mode='html')
    elif message.text == "А":
       bot.send_message(message.chat.id, "Это кириллица, умник. \n\nТы проиграл.", parse_mode='html')
    else:
       bot.send_message(message.chat.id, 'Ты проиграл.', parse_mode='html')

@bot.message_handler()
def everyday_text(message): #Возвращает текст, если видит слово "среда" в любых формах. В среду и в остальные дни недели тексты отличаются.
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
    if "понедельник" in results:
      bot.send_message(message.chat.id, "Понедельник – это, конечно, хорошо.\nНо среду я люблю больше.", parse_mode='html')
    if "вторник" in results:
      bot.send_message(message.chat.id, "Вторник – это, конечно, хорошо.\nНо среду я люблю больше.", parse_mode='html')
    if "четверг" in results:
      bot.send_message(message.chat.id, "Четверг – это, конечно, хорошо.\nНо среду я люблю больше.", parse_mode='html')
    if "пятница" in results:
      bot.send_message(message.chat.id, "Пятница – это, конечно, хорошо.\nНо среду я люблю больше.", parse_mode='html')
    if "суббота" in results:
      bot.send_message(message.chat.id, "Суббота – это, конечно, хорошо.\nНо среду я люблю больше.", parse_mode='html')
    if "воскресение" in results:
      bot.send_message(message.chat.id, "Воскресенье – это, конечно, хорошо.\nНо среду я люблю больше.", parse_mode='html')

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling(none_stop=True)
