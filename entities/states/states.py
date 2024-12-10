from aiogram.fsm.state import StatesGroup, State


class UserStates(StatesGroup):
    photos = State()


class AdminStates(StatesGroup):
    ...


class ManageStates(StatesGroup):
    ...
