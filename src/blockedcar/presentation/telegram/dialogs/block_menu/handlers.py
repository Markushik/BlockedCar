from datetime import date, datetime

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, DialogProtocol, ShowMode
from aiogram_dialog.widgets.kbd import Button


async def add_licence_plate_handler(
    message: Message, protocol: DialogProtocol, dialog_manager: DialogManager
) -> None:
    dialog_manager.dialog_data["license_plate"] = message.text
    await dialog_manager.next()


async def on_select_date(
    callback: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager,
    clicked_date: date,
) -> None:
    dialog_manager.dialog_data["departure_date"] = clicked_date.isoformat()
    await dialog_manager.next()


async def add_departure_time_handler(
    message: Message, protocol: DialogProtocol, dialog_manager: DialogManager
) -> None:
    dialog_manager.dialog_data["departure_time"] = message.text
    await dialog_manager.next()


async def add_comment_handler(
    message: Message, protocol: DialogProtocol, dialog_manager: DialogManager
) -> None:
    dialog_manager.dialog_data["comment"] = message.text
    await dialog_manager.next()


async def add_photo_handler(
    message: Message, protocol: DialogProtocol, dialog_manager: DialogManager
) -> None:
    print(message.photo[-1].file_id)
    dialog_manager.dialog_data["photo_id"] = message.photo[-1].file_id
    await dialog_manager.next()
