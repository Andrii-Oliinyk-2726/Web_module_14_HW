import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.repository.users import get_user_by_email, create_user
from src.schemas import UserModel


class TestUsersRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        # self.client = Client(id=1, email='test@test.com')
        self.user = User(id=1, email='user@test.com')

    async def test_get_user_by_email(self):
        user = User()
        self.session.query(User).filter_by(email='user@test.com').first.return_value = user
        result = await get_user_by_email(email='user@test.com', db=self.session)
        self.assertEqual(result, user)

    async def test_create_user(self):
        body = UserModel(
            username="test_user",
            email="test_username@test.com",
            password="12345678"
        )
        result = await create_user(body, self.session)
        self.assertEqual(result.username, body.username)

