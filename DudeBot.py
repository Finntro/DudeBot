from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import *
from aiogram.utils import executor
import asyncio
import aioschedule
from datetime import datetime as dt
import pymorphy2
import re

storage = MemoryStorage()
bot = Bot(token="ТОКЕН ВАШЕГО БОТА")
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup): #Класс состояний пользователя для регистрации шагов игры в WEDNESDAY
    turnE1 = State()
    turnN = State()
    turnS = State()
    turnA = State()
    ggwp = State()
    turnD = State()
    turnE2 = State()
    turnD2 = State()
    turnY = State()

@dp.message_handler(commands=['start']) #Приветствие при запуске бота.
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, "Привет! \nЯ Чювак бот, и я люблю среды.")

@dp.message_handler(commands=['chat']) #Команда получения ID чата для отправки жаю по средам. ID чатов пока что хардкодятся.
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, message.chat.id)

@dp.message_handler()
async def game_ft(message: types.Message):
     if message.text.lower() == "w": # Игра в WEDNESDAY по буквам. Юзер ходит первый.
        await bot.send_message(message.chat.id, "E", parse_mode='html')
        await UserState.turnN.set()
     elif "играть" in message.text.lower(): # Игра в WEDNESDAY по буквам. Бот ходит первый.
        await bot.send_message(message.chat.id, "Сыграем в WEDNESDAY? Я хожу первый.", parse_mode='html')
        await bot.send_message(message.chat.id, "W", parse_mode='html')
        await UserState.turnD.set()
     else:
        await everyday_text(message) # Возвращает текст, если видит слово "среда" в любых формах. В среду и в остальные дни недели тексты отличаются.
#Ниже, в хендлерах со стейтами описаны шаги игры в WEDNESDAY.
@dp.message_handler(state=UserState.turnE1)
async def fturnE1(message: types.Message, state: FSMContext):
        await bot.send_message(message.chat.id, "E", parse_mode='html')
        await UserState.turnN.set()

@dp.message_handler(state=UserState.turnN)
async def fturnN(message: types.Message, state: FSMContext):
    if message.text.lower() == "d":
        await bot.send_message(message.chat.id, "N", parse_mode='html')
        await UserState.turnS.set()
    else:
       await bot.send_message(message.chat.id, "Ты проиграл.", parse_mode='html')
       await state.finish()

@dp.message_handler(state=UserState.turnS)
async def fturnS(message: types.Message, state: FSMContext):
    if message.text.lower() == "e":
        await bot.send_message(message.chat.id, "S", parse_mode='html')
        await UserState.turnA.set()
    elif message.text.lower() == "е":
        await bot.send_message(message.chat.id, "Это кириллица, умник.\n\nТы проиграл.", parse_mode='html')
        await state.finish()
    else:
       await bot.send_message(message.chat.id, "Ты проиграл.", parse_mode='html')
       await state.finish()

@dp.message_handler(state=UserState.turnA)
async def fturnA(message: types.Message, state: FSMContext):
    if message.text.lower() == "d":
        await bot.send_message(message.chat.id, "A", parse_mode='html')
        await UserState.ggwp.set()
    else:
       await bot.send_message(message.chat.id, "Ты проиграл.", parse_mode='html')
       await state.finish()

@dp.message_handler(state=UserState.ggwp)
async def fggwp(message: types.Message, state: FSMContext):
    if message.text.lower() == "y":
       await bot.send_message(message.chat.id, "Good game, well played!", parse_mode='html')
       await state.finish()
    elif message.text.lower() == "у":
        await bot.send_message(message.chat.id, "Это кириллица, умник.\n\nТы проиграл.", parse_mode='html')
        await state.finish()
    else:
       await bot.send_message(message.chat.id, "Ты проиграл.", parse_mode='html')
       await state.finish()

@dp.message_handler(state=UserState.turnD)
async def fturnD(message: types.Message, state: FSMContext):
    if message.text.lower() == "e":
        await bot.send_message(message.chat.id, "D", parse_mode='html')
        await UserState.turnE2.set()
    elif message.text.lower() == "е":
        await bot.send_message(message.chat.id, "Это кириллица, умник.\n\nТы проиграл.", parse_mode='html')
        await state.finish()
    else:
       await bot.send_message(message.chat.id, "Ты проиграл.", parse_mode='html')
       await state.finish()
@dp.message_handler(state=UserState.turnE2)
async def fturnE2(message: types.Message, state: FSMContext):
    if message.text.lower() == "n":
        await bot.send_message(message.chat.id, "E", parse_mode='html')
        await UserState.turnD2.set()
    else:
       await bot.send_message(message.chat.id, "Ты проиграл.", parse_mode='html')
       await state.finish()

@dp.message_handler(state=UserState.turnD2)
async def fturnD2(message: types.Message, state: FSMContext):
    if message.text.lower() == "s":
        await bot.send_message(message.chat.id, "D", parse_mode='html')
        await UserState.turnY.set()
    else:
       await bot.send_message(message.chat.id, "Ты проиграл.", parse_mode='html')
       await state.finish()

@dp.message_handler(state=UserState.turnY)
async def fturnY(message: types.Message, state: FSMContext):
    if message.text.lower() == "a":
        await bot.send_message(message.chat.id, "Y", parse_mode='html')
        await bot.send_message(message.chat.id, "Good game, well played!", parse_mode='html')
        await state.finish()
    elif message.text.lower() == "а":
        await bot.send_message(message.chat.id, "Это кириллица, умник.\n\nТы проиграл.", parse_mode='html')
        await state.finish()
    else:
       await bot.send_message(message.chat.id, "Ты проиграл.", parse_mode='html')
       await state.finish()

async def everyday_text(message: types.Message): # Возвращает текст, если видит слово "среда" в любых формах. В среду и в остальные дни недели тексты отличаются.
     morph = pymorphy2.MorphAnalyzer()
     opt = re.sub(r'[^\w\s]', '', message.text)
     lst = opt.split()
     results = []
     for i in lst:
       parsed = morph.parse(i)
       norm_form = parsed[0].normal_form
       results.append(norm_form)
     if "среда" in results and dt.today().weekday() != 2:
       await bot.send_message(message.chat.id, "Среда – лучший день недели!\nОчень жду среду.", parse_mode='html')
     if "среда" in results and dt.today().weekday() == 2:
       await bot.send_message(message.chat.id, "Среда – лучший день недели!", parse_mode='html')
     if "понедельник" in results:
       await bot.send_message(message.chat.id, "Понедельник – это, конечно, хорошо.\nНо среду я люблю больше.", parse_mode='html')
     if "вторник" in results:
       await bot.send_message(message.chat.id, "Вторник – это, конечно, хорошо.\nНо среду я люблю больше.", parse_mode='html')
     if "четверг" in results:
       await bot.send_message(message.chat.id, "Четверг – это, конечно, хорошо.\nНо среду я люблю больше.", parse_mode='html')
     if "пятница" in results:
       await bot.send_message(message.chat.id, "Пятница – это, конечно, хорошо.\nНо среду я люблю больше.", parse_mode='html')
     if "суббота" in results:
       await bot.send_message(message.chat.id, "Суббота – это, конечно, хорошо.\nНо среду я люблю больше.", parse_mode='html')
     if "воскресение" in results:
       await bot.send_message(message.chat.id, "Воскресенье – это, конечно, хорошо.\nНо среду я люблю больше.", parse_mode='html')

async def wed_pic(): #Функция отправки жаб в разные чаты. ID чатов пока что хардкодятся.
     await bot.send_sticker(ТУТ ЧАТ АЙДИ, r'CAACAgIAAxkBAAEFfvNi8Anx-hCR7AMEed1TG5g1zRP7uAACPgQAArBhXgMBlldWjYQJMikE')
     await bot.send_sticker(ТУТ ЧАТ АЙДИ 2, r'CAACAgIAAxkBAAEFfvNi8Anx-hCR7AMEed1TG5g1zRP7uAACPgQAArBhXgMBlldWjYQJMikE')
     await bot.send_sticker(ТУТ ЧАТ АЙДИ N, r'CAACAgIAAxkBAAEFfvNi8Anx-hCR7AMEed1TG5g1zRP7uAACPgQAArBhXgMBlldWjYQJMikE')

async def scheduler(): #Расписание отправки жаб с циклом для постоянного выполнения.
    aioschedule.every().wednesday.at("00:00").do(wed_pic)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.create_task(scheduler())
        executor.start_polling(dp)