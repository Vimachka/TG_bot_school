from aiogram import Bot, types


async def set_main_menu(bot: Bot) -> None:
    main_menu_commands = [
        types.BotCommand(command="/start", description="Начало работы с ботом"),
        types.BotCommand(command="/menu", description="Меню"),
        types.BotCommand(command="/rating", description="Рейтинг")
    ]
    await bot.set_my_commands(main_menu_commands)


async def set_main_menu_admin(bot: Bot) -> None:
    main_menu_commands = [
        types.BotCommand(command="/start", description="Начало работы с ботом"),
        types.BotCommand(command="/menu", description="Меню"),
        types.BotCommand(command="/rating", description="Рейтинг"),
        types.BotCommand(command='/add_quest', description='Добавить задание')
    ]
    await bot.set_my_commands(main_menu_commands)