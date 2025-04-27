from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from random import shuffle
from db_file import OpenTableDB
import asyncio

class AddInfo(StatesGroup):
    theme = State()
    que = State()
    ans = State()

bot = Bot(token="7497685119:AAE_nmJX61P99sV9dqw7myH80Z4fjunC2U8", default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN_V2))
dp = Dispatcher()
db = OpenTableDB()

COMMANDS = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Мои темы", callback_data="my_theme_button")], 
    [InlineKeyboardButton(text="Добавить новую тему", callback_data="add_new_theme")]
])
ADD_THEME_COMMAND = InlineKeyboardMarkup(inline_keyboard=[ 
    [InlineKeyboardButton(text="Добавить новую тему", callback_data="add_new_theme")]
])
ADD_QUE_COMMAND = InlineKeyboardMarkup(inline_keyboard=[ 
    [InlineKeyboardButton(text="Добавить ещё вопрос", callback_data="add_new_que")], 
    [InlineKeyboardButton(text="Завершить изменение темы", callback_data="complete")]
])

async def inline_answers(names, id):
    keyboard = InlineKeyboardBuilder()
    for name in names:
        keyboard.add(InlineKeyboardButton(text=name, callback_data="theme_"+str(id[name])))
    return keyboard.adjust(1).as_markup()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    if db.user_in_db(message.from_user.username):
        await message.answer(f"Привет {message.from_user.first_name}", reply_markup=COMMANDS)
    else:
        await message.answer(f"Привет {message.from_user.first_name}, видно вы тут впервые, используйте комманду /help чтобы понять функции этого бота")
        db.add_user(message.from_user.username)

@dp.message(Command('help'))
async def get_help(message: Message):
    await message.answer("Этот бот сделан для запоминания различных тем введённых пользователем, добавляйте новые темы для запоминания вопросы и ответы к ним, чтобы потом, вы могли проверять себя на знание нужных вам тем, используйте комманду /start чтобы приступить к работе")

@dp.callback_query(F.data.startswith('theme_'))
async def out_mes_about_theme(callback: CallbackQuery):
    await callback.answer()
    card_id = int(str(callback.data)[6:])
    ques = db.select_que(card_id)
    shuffle(ques)
    for i in ques:
        await callback.message.answer(f"""{i[0]}
Ответ:
||{i[1]}||""")
    await callback.message.answer("На данный момент это все вопросы по этой теме", reply_markup=COMMANDS)

@dp.callback_query(F.data == 'my_theme_button')
async def mtb(callback: CallbackQuery):
    await callback.answer()
    user_theme = db.select_user_cards(db.user_id(callback.from_user.username))
    user_theme_names = []
    user_theme_id = {}
    for i in user_theme:
        user_theme_names.append(i[1])
        user_theme_id[i[1]] = i[0]
    if len(user_theme) == 0:
        await callback.message.answer("Здесь пока ничего нет", reply_markup=ADD_THEME_COMMAND)
    else:
        await callback.message.answer("Вот ваши темы для запоминания:", reply_markup=await inline_answers(user_theme_names, user_theme_id))

@dp.callback_query(F.data == 'add_new_theme')
async def ant1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Придумайте название для вашей новой темы")
    await state.set_state(AddInfo.theme)

@dp.callback_query(F.data == 'add_new_que')
async def add_que(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ваш вопрос для самопроверки")
    await state.set_state(AddInfo.que)

@dp.callback_query(F.data == 'complete')
async def complete(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Тема добавлена", reply_markup=COMMANDS)
    await state.clear()

@dp.message(AddInfo.theme)
async def ant2(message: Message, state: FSMContext):
    await state.update_data(theme=message.text)
    await message.answer("""Придумай несколько вопросов для сапроверки по этой теме \n
Введите ваш вопрос для самопроверки""")
    await state.set_state(AddInfo.que)

@dp.message(AddInfo.que)
async def add_new_que(message: Message, state: FSMContext):
    await state.update_data(que=message.text)
    await state.set_state(AddInfo.ans)
    await message.answer("Теперь введите ответ на ваш вопрос")

@dp.message(AddInfo.ans)
async def add_new_ans(message: Message, state: FSMContext):
    await state.update_data(ans=message.text)
    data = await state.get_data()
    if db.theme_in_db(data['theme'], db.user_id(message.from_user.username)):
        db.add_theme_in_base(data['theme'], db.user_id(message.from_user.username))
    if db.que_in_db(data['que'], db.card_id(data['theme'], db.user_id(message.from_user.username))):
        db.add_que_in_base(db.card_id(data['theme'], db.user_id(message.from_user.username)), data['que'], data['ans'])
    else:
        await message.answer("Этот ворос уже есть в этой теме, введите другой вопрос")
        await state.set_state(AddInfo.que)
    await message.answer(f"""Ваш вопрос по теме '{data['theme']}':
{data['que']}
Ваш ответ на этот вопрос:
{data['ans']}
""", reply_markup=ADD_QUE_COMMAND)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
