from datetime import date, datetime

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, DialogProtocol, ShowMode
from aiogram_dialog.widgets.kbd import Button
from dishka.integrations.base import wrap_injection
import zstd
import ormsgpack
from dishka.integrations.aiogram import FromDishka
from nats.js.client import JetStreamContext

def inject_getter(func):
    return wrap_injection(
        func=func,
        container_getter=lambda _, p: p["dishka_container"],
        is_async=True,
    )

def inject_handler(func):
    return wrap_injection(
        func=func,
        container_getter=lambda p, _: p[2].middleware_data["dishka_container"],
        is_async=True,
    )

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
    dialog_manager.dialog_data["photo"] = message.photo[-1].file_id
    await dialog_manager.next()


async def on_rewrite(
    message: Message, button: Button, dialog_manager: DialogManager
) -> None:
    ...
 
@inject_handler
async def on_finish(
        message: Message, __, dialog_manager: DialogManager, jetstream: FromDishka[JetStreamContext]
) -> None:
    storage = await jetstream.object_store("store")

    download_photo = await message.bot.download(file=dialog_manager.dialog_data["photo"])
    await storage.put(
        name="some_name",
        data=download_photo,
    )
    await dialog_manager.done()
    
