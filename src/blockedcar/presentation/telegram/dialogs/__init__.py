from .block_menu.dialog import block_menu
from .main_menu.dialog import main_menu
from .notify_menu.dialog import notify_menu


def get_dialogs() -> list:
    return [
        main_menu(),
        notify_menu(),
        block_menu(),
    ]
