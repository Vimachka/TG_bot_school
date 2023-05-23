from aiogram import Router
from aiogram.filters import Text, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.database import id_solution, update_id_solution, is_test, add_test, answer_test, update_test
from lexicon.lexicon_register import LEXICON
from keyboard.keyboard import create_inline_kb, create_url_marcup
from services.servis_register import add_rating_score

router: Router = Router()


class FSMSolution(StatesGroup):
    fill_answer = State()


@router.callback_query(Text(text=['start_quest']))
async def start_solution(callback: CallbackQuery, state: FSMContext):
    solution = await id_solution(callback.from_user.id)
    if solution:
        await update_id_solution(callback.from_user.id, solution[0])
        await state.set_state(FSMSolution.fill_answer)
        await state.update_data(id_solution=solution)
        await callback.message.edit_text(
            text=solution[1],
            reply_markup=await create_url_marcup(834670735)
        )
    else:
        await callback.message.edit_text(
            text=LEXICON['no_solution'],
            reply_markup=await create_inline_kb(
                1, **{'menu': 'Меню'}
            )
        )


@router.message(StateFilter(FSMSolution.fill_answer))
async def process_answer_solution(message: Message, state: FSMContext):
    await state.update_data(solution=message.text)
    id_sol = (await state.get_data())['id_solution'][0]
    text_solution = (await state.get_data())['id_solution'][1]
    true_answ = (await answer_test((await state.get_data())['id_solution'][0]))
    success = true_answ == message.text
    answer = message.text
    if not await is_test(message.from_user.id):
        await add_test(message.from_user.id, id_sol, answer, success)
    else:
        await update_test(message.from_user.id, id_sol, success, answer)

    if success:
        await state.clear()
        await message.answer(
            text=LEXICON['true_answer'],
            reply_markup=await create_inline_kb(
                2, **{'start_quest': 'Продолжить',
                      'menu': 'Меню'}
            )
        )
        await add_rating_score(message, id_sol)
    else:
        await message.answer(
            text=LEXICON['false_answer'] + text_solution,
            reply_markup=await create_url_marcup(834670735)
        )

