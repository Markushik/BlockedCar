from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.text import Const

from blockedcar.presentation.telegram.dialogs.block_menu.states import BlockMenu

from .states import NotifyMenu


def notify_menu() -> Dialog:
    return Dialog(
        Window(
            Const("О чём вы хотите уведомить?"),
            Start(
                Const("Перекрыл машину"),
                id="blocked_car",
                state=BlockMenu.LICENSE_PLATE,
            ),
            state=NotifyMenu.OPTIONS,
        ),
    )
