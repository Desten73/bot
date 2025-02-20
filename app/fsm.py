from aiogram.filters.state import State, StatesGroup


class UserPersonalData(StatesGroup):
    add_personal_data = State()  # True - отправка данных в БД, False - ввод вручную
    target = State()  # True - набор веса, False - сброс веса
    activity = State()
    male = State()  # True - мужчина, False - женщина
    age = State()
    growth = State()
    weight = State()
