from aiogram import Router
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode

from blockedcar.presentation.telegram.dialogs.main_menu.states import MainMenu


async def command_start(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainMenu.START, StartMode.RESET_STACK)


def setup() -> Router:
    router: Router = Router()

    router.message.register(command_start, CommandStart())

    return router
