from aiogram.fsm.state import State, StatesGroup


class BlockMenu(StatesGroup):
    LICENSE_PLATE = State()
    DEPARTURE_DATE = State()
    DEPARTURE_TIME = State()
    COMMENT = State()
    PHOTO = State()
    CHECK = State()
