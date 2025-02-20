from unittest import IsolatedAsyncioTestCase
from app.functions.another_functions import get_answer_calories


class FuncTest(IsolatedAsyncioTestCase):
    async def test_get_answer_calories(self):
        data = dict()
        data["weight"] = 60
        data["growth"] = 169
        data["age"] = 27
        data["male"] = True
        data["activity"] = 1.4
        data["target"] = True

        # class Person:
        #     weight = 50
        #     growth = 169
        #     age = 27
        #     male = True
        #     activity = 1.4
        #     target = True
        # data = Person()
        result = await get_answer_calories(data)
        print(result)
        self.assertIsInstance(result, str)
