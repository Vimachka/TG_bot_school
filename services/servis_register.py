from aiogram.types import Message

from keyboard.keyboard import create_inline_kb
from config.config import Config, load_config
from database.database import return_attempts, update_rating

config: Config = load_config('.env')


async def choice_kb(clas: int):
    if clas == 7:
        return await create_inline_kb(
            1, **{"begin": "Введение физику", "pressure": "Давление", "interaction": "Взаимодействие тел",
                  "work": "Работа,мощность,энергия"}
        )
    elif clas == 8:
        return await create_inline_kb(
            1, **{"thermal": "Тепловые явления", "electrical": "Электричество",
                  "electromagnetic": "Электромагнитные явления", "light": "Световые явления"}
        )
    elif clas == 9:
        return await create_inline_kb(
            1, **{"oge": "ОГЭ", "mechanics": "Механика", "electromag": "Электромагнитные явления",
                  "lightreact": "Световые явления", "quantum": "Квантовые явления"}
        )


def data_kb_category() -> list:
    return ['begin', 'pressure', 'interaction', 'work',
            'thermal', 'electrical', 'electromagnetic', 'light',
            'oge', 'mechanics', 'electromag', 'lightreact', 'quantum']


def is_admin(id_user: int) -> bool:
    print(id_user)
    if id_user in config.tg_bot.id_admin:
        return True
    else:
        return False


async def add_rating_score(message: Message, id_solution: int):
    attempts = await return_attempts(message.from_user.id, id_solution)
    score = 10 if attempts == 1 else 5 if 1 < attempts < 5 else 3
    await update_rating(message.from_user.id, score)
