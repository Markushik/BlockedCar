from aiogram.fsm.state import State, StatesGroup


class VacateMenu(StatesGroup):
    DEPARTURE_DATE = State()
    DEPARTURE_TIME = State()
    GEOLOCATION = State()
