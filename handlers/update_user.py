from aiogram import Router, F
from aiogram.filters import Text, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from lexicon.lexicon_register import LEXICON
from keyboard.keyboard import create_inline_kb
from services.servis_register import choice_kb, data_kb_category
from database.database import update_user_bd

router: Router = Router()


class FSMUdate_user(StatesGroup):
    fill_class = State()
    fill_category = State()


@router.callback_query(Text(text=['update']))
async def update_user(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON['update'], reply_markup=await create_inline_kb(3, **{"7": "7", "8": "8", "9": "9"})
    )
    await state.set_state(FSMUdate_user.fill_class)


@router.callback_query(StateFilter(FSMUdate_user.fill_class), Text(text=['7', '8', '9']))
async def process_sent_class(callback: CallbackQuery, state: FSMContext):
    await state.update_data(clas=callback.data)
    await callback.message.edit_text(
        text=LEXICON['sent_category'], reply_markup=await choice_kb(int(callback.data))
    )
    await state.set_state(FSMUdate_user.fill_category)


@router.message(StateFilter(FSMUdate_user.fill_class))
async def process_error_sent(message: Message):
    await message.answer(
        text=LEXICON['error_class'],
        reply_markup=await create_inline_kb(3, **{"7": "7", "8": "8", "9": "9"})
    )


@router.callback_query(StateFilter(FSMUdate_user.fill_category), Text(text=data_kb_category()))
async def process_sent_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data)
    await update_user_bd(callback.from_user.id, await state.get_data())
    await state.clear()
    await callback.message.edit_text(
        text=LEXICON['update_now'],
        reply_markup=await create_inline_kb(1, **{"start_quest": "Начать решать"}))


@router.message(StateFilter(FSMUdate_user.fill_category))
async def process_error_sent_category(message: Message, state: FSMContext):
    Dict = await state.get_data()
    await message.answer(
        text=LEXICON['error_sent_category'],
        reply_markup=await choice_kb(int(Dict['clas']))
    )
