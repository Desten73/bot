from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import is_gym_bro

# Все клавиатуры

start_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Подсчет суточной нормы калорий"), KeyboardButton(text="Внести свои данные")],
    [KeyboardButton(text="Составление тренировочного плана"), KeyboardButton(text="Питание")]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню...")

calories_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Расчет по моим параметрам"),
     KeyboardButton(text="Ввести данные для расчета")]
], resize_keyboard=True, input_field_placeholder="Выберите пункт меню...")

# Клавиатуры для рассчета среднесуточной нормы калорий
target_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Набор веса"), KeyboardButton(text="Сброс веса")],
], resize_keyboard=True, input_field_placeholder="Выберите вашу цель...")

male_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Мужчина"), KeyboardButton(text="Женщина")],
], resize_keyboard=True, input_field_placeholder="Выберите ваш пол...")

activity_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Минимальные нагрузки, сидячая работа"),
     KeyboardButton(text="Средняя активность, работа средней тяжести")],
    [KeyboardButton(text="Высокая активность"),
     KeyboardButton(text="Ежедневные тренировки, тяжелая физическая работа")],
], resize_keyboard=True, input_field_placeholder="Выберите ваш уровень активности...")


async def get_start_kb(tg_id):
    is_gymbro = await is_gym_bro(tg_id)
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text="test", callback_data="call_data"),
                 InlineKeyboardButton(text="test" if is_gymbro else "test2",
                                      callback_data="call_data" if is_gymbro else "call_data2"),
                 InlineKeyboardButton(text="test", callback_data="call_data"))

    return keyboard.adjust(2).as_markup()
