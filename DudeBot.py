from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
import asyncio
from datetime import datetime as dt
import re
import shelve
import pymorphy3
from aiogram.utils.exceptions import TelegramAPIError
import random

storage = MemoryStorage()
bot = Bot(token="YOUR BOT TOKEN CODE")
dp = Dispatcher(bot, storage=storage)

class UserState(StatesGroup):
    turnE1 = State()
    turnN = State()
    turnS = State()
    turnA = State()
    ggwp = State()
    turnD = State()
    turnE2 = State()
    turnD2 = State()
    turnY = State()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Сохраняем chat_id в файл по команде /start
    with shelve.open('chat_ids') as db:
        chat_ids = db.get('chat_ids', [])
        if message.chat.id not in chat_ids:
            chat_ids.append(message.chat.id)
            db['chat_ids'] = chat_ids
    await message.answer("Привет! \nЯ Чювак бот, и я люблю среды.")

async def everyday_text(message: types.Message):  # Возвращает текст, если видит слово "среда" в любых формах. В среду и в остальные дни недели тексты отличаются.
    morph = pymorphy3.MorphAnalyzer()
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
        await bot.send_message(message.chat.id, "It's Wednesday, my dudes!", parse_mode='html')
    if "понедельник" in results:
        await bot.send_message(message.chat.id, "Понедельник – это, конечно, хорошо.\nНо среду я люблю больше.",
                               parse_mode='html')
    if "вторник" in results:
        await bot.send_message(message.chat.id, "Вторник – это, конечно, хорошо.\nНо среду я люблю больше.",
                               parse_mode='html')
    if "четверг" in results:
        await bot.send_message(message.chat.id, "Четверг – это, конечно, хорошо.\nНо среду я люблю больше.",
                               parse_mode='html')
    if "пятница" in results:
        await bot.send_message(message.chat.id, "Пятница – это, конечно, хорошо.\nНо среду я люблю больше.",
                               parse_mode='html')
    if "суббота" in results:
        await bot.send_message(message.chat.id, "Суббота – это, конечно, хорошо.\nНо среду я люблю больше.",
                               parse_mode='html')
    if "воскресение" in results:
        await bot.send_message(message.chat.id, "Воскресенье – это, конечно, хорошо.\nНо среду я люблю больше.",
                               parse_mode='html')

@dp.message_handler()
async def game_ft(message: types.Message):# Игра в WEDNESDAY по буквам. Юзер ходит первый.
     if message.text.lower() == "w":
        await bot.send_message(message.chat.id, "E", parse_mode='html')
        await UserState.turnN.set()
     elif "играть" in message.text.lower():
        await bot.send_message(message.chat.id, "Сыграем в WEDNESDAY? Я хожу первый.", parse_mode='html')
        await bot.send_message(message.chat.id, "W", parse_mode='html')
        await UserState.turnD.set()
     else:
        await everyday_text(message) # Возвращает текст, если видит слово "среда" в любых формах. В среду и в остальные дни недели тексты отличаются.

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

# Функция, которая отправляет стикер во все сохранённые чаты
async def send_random_sticker():
    with shelve.open('chat_ids') as db:
        chat_ids = db.get('chat_ids', [])
    sticker_pack = "dudestrasse"
    stickers = await bot.get_sticker_set(sticker_pack)
    for chat_id in chat_ids:
        try:
            sticker_id = random.choice(stickers.stickers).file_id
            await bot.send_sticker(chat_id, sticker_id)
        except TelegramAPIError as e:
            print(f"Sending the message to chat {chat_id} is {e}")
            continue

# Запускаем функцию send_sticker каждую среду в 9:00
async def scheduler():
    while True:
        now = dt.now()
        if now.weekday() == 2 and now.hour == 9 and now.minute == 0:
            await send_random_sticker()
        await asyncio.sleep(60 - now.second)

if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.create_task(scheduler())
        executor.start_polling(dp)
