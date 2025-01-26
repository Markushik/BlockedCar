from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const

from .states import MainMenu


def main_menu() -> Dialog:
    return Dialog(
        Window(Const("Привет!"), state=MainMenu.START),
    )
