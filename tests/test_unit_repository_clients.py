import datetime
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Client, User
from src.repository.clients import get_clients, get_client_by_id, get_client_by_email, create, update, remove
from src.schemas import ClientModel


class TestClientsRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.client = Client(id=1, email='test@test.com')

    async def test_get_clients(self):
        clients = [Client(), Client(), Client()]
        self.session.query(Client).all.return_value = clients
        result = await get_clients(db=self.session)
        self.assertEqual(result, clients)

    async def test_get_client_by_id(self):
        client = Client()
        self.session.query(Client).filter_by(client_id=1).first.return_value = client
        result = await get_client_by_id(client_id=1, db=self.session)
        self.assertEqual(result, client)

    async def test_get_client_by_email(self):
        client = Client()
        self.session.query(Client).filter_by(email="test@test.com").first.return_value = client
        result = await get_client_by_email(email="test@test.com", db=self.session)
        self.assertEqual(result, client)

    async def test_create(self):
        body = ClientModel(
            first_name="test",
            last_name="TEST",
            email="test@test.com",
            mobile="+380501112233",
            birthday=datetime.date(2020, 1, 1),
            add_info="qwerty"
        )
        user = User(id=1)
        result = await create(body, self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.mobile, body.mobile)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.add_info, body.add_info)
        self.assertTrue(hasattr(result, "id"))

    async def test_update(self):
        body_update = ClientModel(
            first_name="test_update",
            last_name="TEST_update",
            email="test@test.com",
            mobile="+380501112233_update",
            birthday=datetime.date(2020, 1, 1),
            add_info="qwerty_update"
        )
        user = User(id=1)
        result = await update(client_id=1, body=body_update, db=self.session)
        self.assertEqual(result.first_name, body_update.first_name)
        self.assertEqual(result.last_name, body_update.last_name)
        self.assertEqual(result.email, body_update.email)
        self.assertEqual(result.mobile, body_update.mobile)
        self.assertEqual(result.birthday, body_update.birthday)
        self.assertEqual(result.add_info, body_update.add_info)

    async def test_remove(self):
        client = Client()
        self.session.query(Client).filter_by(client_id=1).first.return_value = client
        result = await remove(client_id=1, db=self.session)
        self.assertEqual(result, client)







