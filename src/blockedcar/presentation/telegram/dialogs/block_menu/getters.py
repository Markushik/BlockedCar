from aiogram_dialog import DialogManager


async def write_data_getter(dialog_manager: DialogManager, **_kwargs) -> dict:
    return {
        "license_plate": dialog_manager.dialog_data["license_plate"],
        "departure_date": dialog_manager.dialog_data["departure_date"],
        "departure_time": dialog_manager.dialog_data["departure_time"],
        "comment": dialog_manager.dialog_data["comment"],
        "photo": dialog_manager.dialog_data["photo"],
    }
