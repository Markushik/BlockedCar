from aiogram.types import ContentType, Message
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Calendar, Column, Counter, Group, Row
from aiogram_dialog.widgets.text import Const, Format

from .getters import write_data_getter
from .handlers import (
    add_comment_handler,
    add_departure_time_handler,
    add_licence_plate_handler,
    add_photo_handler,
    on_select_date,
)
from .states import BlockMenu


def block_menu() -> Dialog:
    return Dialog(
        Window(
            Const(
                "Отправите номер(а) которую(ые) перекрыли через запятую\n\nПример: А012АА77, Б123ББ86"
            ),
            MessageInput(add_licence_plate_handler, content_types=[ContentType.TEXT]),
            parse_mode="HTML",
            state=BlockMenu.LICENSE_PLATE,
        ),
        Window(
            Const("Выберите дату отъезда на календаре:"),
            Calendar(id="calendar", on_click=on_select_date),
            state=BlockMenu.DEPARTURE_DATE,
        ),
        Window(
            Const("Во сколько планируете уезжать?"),
            MessageInput(add_departure_time_handler, content_types=[ContentType.TEXT]),
            state=BlockMenu.DEPARTURE_TIME,
        ),
        Window(
            Const("Во сколько планируете уезжать?"),
            MessageInput(add_comment_handler, content_types=[ContentType.TEXT]),
            state=BlockMenu.COMMENT,
        ),
        Window(
            Const("Отправьте фото:"),
            MessageInput(add_photo_handler, content_types=[ContentType.PHOTO]),
            state=BlockMenu.PHOTO,
        ),
        Window(
            Const("Проверьте правильность введеных данных:\n"),
            Format("Перекрытые машины: {license_plate}"),
            state=BlockMenu.CHECK,
            getter=write_data_getter,
        ),
    )
