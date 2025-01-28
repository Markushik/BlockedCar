from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Row, Start
from aiogram_dialog.widgets.text import Const

from blockedcar.presentation.telegram.dialogs.notify_menu.states import NotifyMenu

from .states import MainMenu


def main_menu() -> Dialog:
    return Dialog(
        Window(
            Const(". . ."),
            Start(Const("📳 Уведомить"), id="notify", state=NotifyMenu.OPTIONS),
            Row(
                Button(Const("🗂️ Архив"), id="archive"),
                Button(Const("👤 Профиль"), id="profile"),
            ),
            state=MainMenu.START,
        ),
    )
