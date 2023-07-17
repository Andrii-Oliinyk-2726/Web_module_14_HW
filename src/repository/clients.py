from sqlalchemy.orm import Session

from src.schemas import ClientModel
from src.database.models import Client


async def get_clients(db: Session):
    """
    The get_clients function returns a list of all clients in the database.


    :param db: Session: Pass the database session into the function
    :return: A list of client objects
    :doc-author: Trelent
    """
    clients = db.query(Client).all()
    return clients


async def get_client_by_id(client_id: int, db: Session):
    """
    The get_client_by_id function takes in a client_id and db Session object,
    and returns the Client object with that id. If no such Client exists, it returns None.

    :param client_id: int: Filter the client by id
    :param db: Session: Pass the database session to the function
    :return: A client by its id
    :doc-author: Trelent
    """
    client = db.query(Client).filter_by(id=client_id).first()
    return client


async def get_client_by_email(email: str, db: Session):
    """
    The get_client_by_email function takes in an email and a database session,
    and returns the client with that email. If no such client exists, it returns None.

    :param email: str: Pass in the email of the client to be found
    :param db: Session: Access the database
    :return: A client object
    :doc-author: Trelent
    """
    client = db.query(Client).filter_by(email=email).first()
    return client


async def create(body: ClientModel, db: Session):
    """
    The create function creates a new client in the database.
        Args:
            body (ClientModel): The client to create.

    :param body: ClientModel: Define the body of the request
    :param db: Session: Access the database and perform operations on it
    :return: The client object, which is the same as the body
    :doc-author: Trelent
    """
    client = Client(**body.dict())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


async def update(client_id: int, body: ClientModel, db: Session):
    """
    The update function updates a client in the database.
        Args:
            client_id (int): The id of the client to update.
            body (ClientModel): The updated information for the specified user.

    :param client_id: int: Identify the client to be deleted
    :param body: ClientModel: Pass the client data to be updated
    :param db: Session: Access the database
    :return: The client object
    :doc-author: Trelent
    """
    client = await get_client_by_id(client_id, db)
    if client:
        client.first_name = body.first_name
        client.last_name = body.last_name
        client.email = body.email
        client.mobile = body.mobile
        client.birthday = body.birthday
        client.add_info = body.add_info
        db.commit()
    return client


async def remove(client_id: int, db: Session):
    """
    The remove function removes a client from the database.
        Args:
            client_id (int): The id of the client to be removed.
            db (Session): A connection to the database.

    :param client_id: int: Specify the client id of the client to be removed
    :param db: Session: Pass the database session into the function
    :return: The client that was removed
    :doc-author: Trelent
    """
    client = await get_client_by_id(client_id, db)
    if client:
        db.delete(client)
        db.commit()
    return client
