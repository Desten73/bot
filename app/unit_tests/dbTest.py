from unittest import IsolatedAsyncioTestCase
from app.database.requests import (add_new_user, is_gym_bro, add_personal_parameter,
                                       get_personal_parameter)


class DBTest(IsolatedAsyncioTestCase):
    async def test_add_new_user(self):
        self.assertTrue(await add_new_user(3, "Test2"))

    async def test_is_gym_bro(self):
        self.assertTrue(await is_gym_bro(3))

    async def test_add_personal_parameter(self):
        self.assertTrue(await add_personal_parameter(3, True, 1.4, True,
                                                     25, 169, 60))

    async def test_get_personal_parameter(self):
        self.assertTrue(await get_personal_parameter(3))

