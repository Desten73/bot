from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq
from app.middlewares import TestMiddleware
from app.fsm import UserPersonalData
import app.functions.another_functions as func

router = Router()

# router.message.middleware(TestMiddleware())


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.add_new_user(message.from_user.id, message.from_user.username)
    await message.answer(f"Добро пожаловать, {message.from_user.username}, "
                         f"я помогу тебе в составлении тренировок и подсчете калорий",
                         reply_markup=kb.start_kb)


# Ответы на пункты основного меню
@router.message(F.text == "Подсчет суточной нормы калорий")
async def calories_per_day(message: Message):
    await message.answer("Выберите один из вариантов", reply_markup=kb.calories_kb)


@router.message(F.text == "Внести свои данные")
async def add_personal_data(message: Message, state: FSMContext):
    # await state.set_state(UserPersonalData.add_personal_data)
    await state.update_data(add_personal_data="True")
    await state.set_state(UserPersonalData.target)
    await message.answer("Выберите вашу цель:", reply_markup=kb.target_kb)


@router.message(F.text == "Составление тренировочного плана")
async def make_personal_workout(message: Message):
    await message.answer("Приносим свои извинения, но данная функция пока не работает. "
                         "Мы сообщим вам об изменении функионала, ждите обновлений!)")


@router.message(F.text == "Питание")
async def add_products(message: Message):
    await message.answer("Приносим свои извинения, но данная функция пока не работает. "
                         "Мы сообщим вам об изменении функионала, ждите обновлений!)")


# Вычисление среднесуточного количества калорий
@router.message(F.text == "Расчет по моим параметрам")
async def start_manual_calories(message: Message):
    person_data = await rq.get_personal_parameter(message.from_user.id)
    if person_data:
        await message.answer(await func.get_answer_calories(person_data), reply_markup=kb.start_kb)
    else:
        await message.answer("Вам необходимо заполнить свои параметры для рассчета калорий")


@router.message(F.text == "Ввести данные для расчета")
async def start_manual_calories(message: Message, state: FSMContext):
    await state.set_state(UserPersonalData.target)
    await state.update_data(add_personal_data="")
    await message.answer("Выберите вашу цель:", reply_markup=kb.target_kb)


@router.message(UserPersonalData.add_personal_data)
async def set_male(message: Message, state: FSMContext):
    await state.update_data(add_personal_data="True")
    await state.set_state(UserPersonalData.target)
    await message.answer("Выберите вашу цель:", reply_markup=kb.target_kb)


@router.message(UserPersonalData.target)
async def set_male(message: Message, state: FSMContext):
    try:
        if message.text == "Набор веса":
            await state.update_data(target="True")
        elif message.text == "Сброс веса":
            await state.update_data(target="")
        else:
            raise ValueError
        await state.set_state(UserPersonalData.male)
        await message.answer("Выберите свой пол:", reply_markup=kb.male_kb)
    except:
        await message.reply("Выберите из предложенного", reply_markup=kb.target_kb)


@router.message(UserPersonalData.male)
async def set_male(message: Message, state: FSMContext):
    try:
        if message.text.lower() in ["мужчина", "муж", "м"]:
            await state.update_data(male="True")
        elif message.text.lower() in ["женщина", "жен", "ж"]:
            await state.update_data(male="")
        else:
            raise ValueError
        await state.set_state(UserPersonalData.activity)
        await message.answer("Выберите свой уровень активности:", reply_markup=kb.activity_kb)
    except:
        await message.reply("Выберите из предложенного", reply_markup=kb.male_kb)


@router.message(UserPersonalData.activity)
async def set_male(message: Message, state: FSMContext):
    try:
        if message.text == "Минимальные нагрузки, сидячая работа":
            await state.update_data(activity="1.2")
        elif message.text == "Средняя активность, работа средней тяжести":
            await state.update_data(activity="1.375")
        elif message.text == "Высокая активность":
            await state.update_data(activity="1.55")
        elif message.text == "Ежедневные тренировки, тяжелая физическая работа":
            await state.update_data(activity="1.7")
        else:
            raise ValueError
        await state.set_state(UserPersonalData.age)
        await message.answer("Введите свой возраст:")
    except:
        await message.reply("Выберите из предложенного", reply_markup=kb.activity_kb)


@router.message(UserPersonalData.age)
async def set_age(message: Message, state: FSMContext):
    try:
        int(message.text)
        await state.update_data(age=message.text)
        await state.set_state(UserPersonalData.growth)
        await message.answer("Введите свой рост:")
    except:
        await message.reply("Необходимо вводить целочисленное число")


@router.message(UserPersonalData.growth)
async def set_growth(message: Message, state: FSMContext):
    try:
        int(message.text)
        await state.update_data(growth=message.text)
        await state.set_state(UserPersonalData.weight)
        await message.answer("Введите свой вес:")
    except:
        await message.reply("Необходимо вводить целочисленное число")


@router.message(UserPersonalData.weight)
async def set_weight(message: Message, state: FSMContext):
    try:
        float(message.text)
        await state.update_data(weight=message.text)
        data = await state.get_data()
        if data["add_personal_data"]:
            await rq.add_personal_parameter(message.from_user.id, data["target"], data["activity"],
                                            data["male"], data["age"], data["growth"], data["weight"])

        await message.answer(await func.get_answer_calories(data), reply_markup=kb.start_kb)
        await state.clear()
    except:
        await message.reply("Пример вводимого числа: 65.4")
