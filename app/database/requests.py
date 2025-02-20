from sqlalchemy import select, update
from app.database.models import async_session
from app.database.models import User, PersonalParameter


async def add_new_user(tg_id, nickname):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, nickname=nickname))
            await session.commit()
        return True


async def is_gym_bro(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        return True if user else False


async def get_personal_parameter(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            person = await session.scalar(select(PersonalParameter).where(PersonalParameter.user_id == user.id))
            return person
        else:
            return None


async def add_personal_parameter(tg_id, target, activity, male, age, growth, weight):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            raise Exception("Такой user не существует, не прошла команда /start "
                            f"и последующая запись в БД для tg_id == {tg_id}")

        person = await session.scalar(select(PersonalParameter).where(PersonalParameter.user_id == user.id))
        if person:
            await session.execute(update(PersonalParameter).
                                  where(PersonalParameter.user_id == user.id).
                                  values(target=bool(target), activity=float(activity), male=bool(male),
                                         age=int(age), growth=int(growth), weight=float(weight)))
        else:
            session.add(PersonalParameter(user_id=user.id, target=bool(target), activity=float(activity),
                                          male=bool(male), age=int(age), growth=int(growth), weight=float(weight)))
        await session.commit()
        return True
