from aiogram import Router, F
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from lexicon.lexicon_register import LEXICON
from keyboard.keyboard import create_inline_kb
from services.servis_register import choice_kb, data_kb_category
from database.database import add_user, is_user, add_rating

router: Router = Router()


class FSMRegister(StatesGroup):
    fill_name = State()
    fill_class = State()
    fill_category = State()


@router.callback_query(Text(text=['register']))
async def start_register(callback: CallbackQuery, state: FSMContext):
    if not await  is_user(callback.from_user.id):
        await callback.message.edit_text(text=LEXICON['start_register'])
        await state.set_state(FSMRegister.fill_name)
    else:
        await callback.message.edit_text(
            text=LEXICON['register_again'],
            reply_markup=await create_inline_kb(1, **{'menu': 'Меню', 'start_quest': 'Решать задачки'})
        )


@router.message(StateFilter(FSMRegister.fill_name), F.text.isalpha())
async def process_sent_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        text=LEXICON['sent_class'],
        reply_markup=await create_inline_kb(3, **{"7": "7", "8": "8", "9": "9"}))
    await state.set_state(FSMRegister.fill_category)


@router.message(StateFilter(FSMRegister.fill_name))
async def warning_sent_name(message: Message):
    await message.answer(text=LEXICON['error_name'])


@router.callback_query(StateFilter(FSMRegister.fill_category), Text(text=['7', '8', '9']))
async def process_sent_class(callback: CallbackQuery, state: FSMContext):
    await state.update_data(clas=callback.data)
    await callback.message.edit_text(
        text=LEXICON['sent_category'],
        reply_markup=await choice_kb(int(callback.data)))
    await state.set_state(FSMRegister.fill_category)


@router.message(StateFilter(FSMRegister.fill_class))
async def warning_sent_class(message: Message):
    await message.answer(
        text=LEXICON['error_class'],
        reply_markup=await create_inline_kb(3, **{"7": "7", "8": "8", "9": "9"}))


@router.callback_query(StateFilter(FSMRegister.fill_category), Text(text=data_kb_category()))
async def end_register(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data)
    await add_user(callback.from_user.id, await state.get_data())
    await add_rating(callback.from_user.id)
    await state.clear()
    await callback.message.edit_text(
        text=LEXICON['start_quest'],
        reply_markup=await create_inline_kb(1, **{"start_quest": "Начать решать",
                                                  "update": "Обновить данные"}))


@router.message(StateFilter(FSMRegister.fill_category))
async def warning_sent_category(message: Message, state: FSMContext):
    Dict = await state.get_data()
    await message.edit_text(
        text=LEXICON['error_sent_category'],
        reply_markup=await choice_kb(int(Dict['clas']))
    )



