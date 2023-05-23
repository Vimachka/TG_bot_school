from aiogram import Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, Text

from keyboard.keyboard import create_inline_kb
from keyboard.menu import set_main_menu, set_main_menu_admin
from database.database import is_user,return_rating
from lexicon.lexicon_register import LEXICON
from services.servis_register import is_admin

router: Router = Router()


@router.message(Command(commands=['start']))
async def info(message: Message, bot: Bot):
    if is_admin(message.from_user.id):
        await set_main_menu_admin(bot)
    else:
        await set_main_menu(bot)
    await message.answer(
        text='Давай перейдем к регистрации!',
        reply_markup=await create_inline_kb(1, **{"register": "Регистрация"}))


@router.message(Command(commands=['update']))
async def update(message: Message):
    if await is_user(message.from_user.id):
        await message.answer(
            text='Можно обновить свои данные',
            reply_markup=await create_inline_kb(1, **{'update': 'Обновить'})
        )
    else:
        await message.answer(
            text='Вы не зарегистрированы, хотите пройти регистрацию?',
            reply_markup=await create_inline_kb(1, **{"register": "Регистрация"})
        )


@router.message(Command(commands=['menu']))
async def sent_menu_message(message: Message):
    if await is_user(message.from_user.id):
        await message.answer(
            text=LEXICON['sent_menu'],
            reply_markup=await create_inline_kb(
                1, **{'update': 'Редактировать профиль',
                      'start_quest': 'Решать задачки'}
            )
        )
    else:
        await message.answer(
            text=LEXICON['sent_menu'],
            reply_markup=await create_inline_kb(
                1, **{'register': 'Регистрация'}
            )
        )


@router.callback_query(Text(text=['menu']))
async def sent_menu(callback: CallbackQuery):
    if await is_user(callback.from_user.id):
        await callback.message.edit_text(
            text=LEXICON['sent_menu'],
            reply_markup=await create_inline_kb(
                1, **{'update': 'Редактировать профиль',
                      'start_quest': 'Решать задачки'}
            )
        )
    else:
        await callback.message.edit_text(
            text=LEXICON['sent_menu'],
            reply_markup=await create_inline_kb(
                1, **{'register': 'Регистрация'}
            )
        )


@router.message(Command(commands=['rating']))
async def watching_rating(message: Message):
    rating = await return_rating()
    answer = LEXICON['rating']
    count = 1
    for user in rating:
        answer += f'{count}). {user[1]} - {user[0]} б.\n'
    await message.answer(
        text=answer,
        reply_markup=await create_inline_kb(1, **{'menu': 'Главное меню'})
    )
