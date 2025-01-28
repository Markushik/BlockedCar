from aiogram.fsm.state import State, StatesGroup


class MenuBlock(StatesGroup):
    LICENSE_PLATE = State()
    DEPARTURE_DATE = State()
    DEPARTURE_TIME = State()
    COMMENT = State()
    PHOTO = State()
