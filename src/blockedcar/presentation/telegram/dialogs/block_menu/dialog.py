from aiogram.types import ContentType, Message
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Calendar,
    Column,
    Counter,
    Group,
    Next,
    Row,
)
from aiogram_dialog.widgets.text import Const, Format

from .getters import write_data_getter
from .handlers import (
    add_comment_handler,
    add_departure_time_handler,
    add_licence_plate_handler,
    add_photo_handler,
    on_finish,
    on_rewrite,
    on_select_date,
)
from .states import BlockMenu


def block_menu() -> Dialog:
    return Dialog(
        Window(
            Const(
                "<b>🚗 Введите номера машин</b>, которые <b>перекрыли:</b>\n\n"
                "<b>Пример: </b> <code>А123АА45, Б678ББ91</code>"
            ),
            MessageInput(add_licence_plate_handler, content_types=[ContentType.TEXT]),
            parse_mode="HTML",
            state=BlockMenu.LICENSE_PLATE,
        ),
        Window(
            Const("<b>🗓️ Выберите дату</b> своего <b>отдъезда:</b>"),
            Calendar(id="calendar", on_click=on_select_date),
            parse_mode="HTML",
            state=BlockMenu.DEPARTURE_DATE,
        ),
        Window(
            Const(
                "<b>🕓 Введите время</b> планируемого <b>выезда:</b>\n\n"
                "<b>Пример: </b> <code>8:15</code>"
            ),
            MessageInput(add_departure_time_handler, content_types=[ContentType.TEXT]),
            parse_mode="HTML",
            state=BlockMenu.DEPARTURE_TIME,
        ),
        Window(
            Const("<b>💬 Введите комментарий:</b>"),
            Next(Const("Пропустить"), id="next_to_photo"),
            MessageInput(add_comment_handler, content_types=[ContentType.TEXT]),
            parse_mode="HTML",
            state=BlockMenu.COMMENT,
        ),
        # todo: Кнопка: Доска
        Window(
            Const(
                "<b>📎 Прикрепите фото:</b>\n\n"
                "<b>Можно прикрепить</b> только <b>одно</b> фото"
            ),
            Next(Const("Пропустить"), id="next_to_check"),
            MessageInput(add_photo_handler, content_types=[ContentType.PHOTO]),
            parse_mode="HTML",
            state=BlockMenu.PHOTO,
        ),
        Window(
            Const("<b>Проверьте корректность</b> введеных данных:\n"),
            Format(
                "<b>Перекрытые машины: </b><code>{license_plate}</code>\n"
                "<b>Дата отъезда: </b><code>{departure_date}</code>\n"
                "<b>Время отъезда: </b><code>{departure_time}</code>\n"
                "<b>Комментарий: </b><code>{comment}</code>\n"
                "<b>Прикрепленные фото: </b><code>(1)</code>\n\n"
            ),
            Const("Верны ли введенные данные?"),
            Row(
                Button(Const("Да"), id="yes", on_click=on_finish),
                Button(Const("Нет"), id="no", on_click=on_rewrite),
            ),
            state=BlockMenu.CHECK,
            parse_mode="HTML",
            getter=write_data_getter,
        ),
    )
