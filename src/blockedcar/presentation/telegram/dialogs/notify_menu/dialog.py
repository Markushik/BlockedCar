from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from .states import NotifyMenu


def notify_menu() -> Dialog:
    return Dialog(
        Window(
            Const("О чём вы хотите уведомить?"),
            Button(Const("Перекрыл машину"), id="blocked_car"),
            state=NotifyMenu.OPTIONS,
        ),
    )
