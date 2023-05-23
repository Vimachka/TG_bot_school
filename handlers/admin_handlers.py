from aiogram import Router, F
from aiogram.filters import Text, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message


from lexicon.lexicon_register import LEXICON
from keyboard.keyboard import create_inline_kb
from services.servis_register import choice_kb, data_kb_category
from database.database import add_solution
from services.servis_register import is_admin

router: Router = Router()

router.message.filter(lambda x: is_admin(x.from_user.id))


class FSMAdd_quest(StatesGroup):
    fill_class = State()
    fill_category = State()
    fill_text = State()
    fill_solution = State()


@router.message(Command(commands=['add_quest']))
async def add_quest(message: Message):
    await message.answer(
        text=LEXICON['start_text_solution'],
        reply_markup=await create_inline_kb(1, **{'add_quest': 'Добавить'})
    )


@router.callback_query(Text(text=['add_quest']))
async def process_add_quest(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=LEXICON['add_quest'],
        reply_markup=await create_inline_kb(3, **{"7": "7", "8": "8", "9": "9"})
    )
    await state.set_state(FSMAdd_quest.fill_class)


@router.callback_query(StateFilter(FSMAdd_quest.fill_class), Text(text=['7', '8', '9']))
async def process_sent_class(callback: CallbackQuery, state: FSMContext):
    await state.update_data(clas=callback.data)
    await callback.message.edit_text(
        text=LEXICON['sent_category'],
        reply_markup=await choice_kb(int(callback.data))
    )
    await state.set_state(FSMAdd_quest.fill_category)


@router.message(StateFilter(FSMAdd_quest.fill_class))
async def process_error_sent_class(message: Message):
    await message.answer(
        text=LEXICON['error_class'],
        reply_markup=await create_inline_kb(3, **{"7": "7", "8": "8", "9": "9"})
    )


@router.callback_query(Text(text=data_kb_category()), StateFilter(FSMAdd_quest.fill_category))
async def process_sent_category(callback: CallbackQuery, state: FSMContext):
    await state.update_data(category=callback.data)
    await callback.message.edit_text(
        text=LEXICON['sent_text']
    )
    await state.set_state(FSMAdd_quest.fill_text)


@router.message(StateFilter(FSMAdd_quest.fill_category))
async def process_error_sent_category(message: Message, state: FSMContext):
    Dict = await state.get_data()
    await message.edit_text(
        text=LEXICON['error_sent_category'],
        reply_markup=await choice_kb(int(Dict['clas']))
    )


@router.message(StateFilter(FSMAdd_quest.fill_text))
async def process_sent_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer(
        text=LEXICON['sent_solution']
    )
    await state.set_state(FSMAdd_quest.fill_solution)


@router.message(StateFilter(FSMAdd_quest.fill_text))
async def process_error_sent_text(message: Message):
    await message.answer(
        text=LEXICON['sent_error_text']
    )


@router.message(StateFilter(FSMAdd_quest.fill_solution))
async def process_sent_solution(message: Message, state: FSMContext):
    await state.update_data(solution=message.text)
    await add_solution(await state.get_data())
    await message.answer(
        text=LEXICON['add_solution'],
        reply_markup=await create_inline_kb(1, **{'add_quest': 'Добавить ещё', 'answer': 'Посмотреть ответы'})
    )
    await state.clear()


@router.message(StateFilter(FSMAdd_quest.fill_solution))
async def process_error_sent_solution(message: Message):
    await message.answer(
        text=LEXICON['error_add_solution']
    )