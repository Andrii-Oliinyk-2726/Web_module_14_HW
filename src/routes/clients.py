from datetime import date, timedelta
from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy import extract
from sqlalchemy.orm import Session

from src.schemas import ClientResponse, ClientModel
from src.database.db import get_db
from src.database.models import Client, User, Role
from src.repository import clients as repository_clients
from src.services.auth import auth_service
from src.services.roles import RoleAccess

router = APIRouter(prefix="/clients", tags=['clients'])

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator])
allowed_operation_remove = RoleAccess([Role.admin])


@router.get("/", response_model=List[ClientResponse], name="All clients:",
            dependencies=[Depends(allowed_operation_get), Depends(RateLimiter(times=2, seconds=5))])
async def get_clients(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_clients function returns a list of all clients in the database.
        The function is called by sending a GET request to the /clients endpoint.

    :param db: Session: Access the database
    :param current_user: User: Get the current user
    :return: A list of clients
    :doc-author: Trelent
    """
    clients = await repository_clients.get_clients(db)
    return clients


@router.get("/birthday", response_model=List[ClientResponse], name="Congratulate:",
            dependencies=[Depends(allowed_operation_get)])
async def get_clients_by_birth_date(start_date: date = Query(default=date.today()),
                                    end_date: date = Query(default=(date.today() + timedelta(days=7))),
                                    db: Session = Depends(get_db),
                                    current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_clients_by_birth_date function returns a list of clients whose birthdays fall within the specified date range.
    The start_date and end_date parameters are optional, with default values of today and seven days from today respectively.


    :param start_date: date: Set the start date of the range
    :param end_date: date: Specify the end date of the range
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :return: All clients with birthdays between the start_date and end_date
    :doc-author: Trelent
    """
    clients = db.query(Client).filter(extract('day', Client.birthday) >= start_date.day,
                                      extract('month', Client.birthday) >= start_date.month,
                                      extract('day', Client.birthday) <= end_date.day,
                                      extract('month', Client.birthday) <= end_date.month).all()
    return clients


@router.get("/{client_id}", response_model=ClientResponse, dependencies=[Depends(allowed_operation_get)])
async def get_client(client_id: int = Path(ge=1), db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_client function is a GET request that returns the client with the given ID.
    If no client exists with that ID, it will return a 404 error.

    :param client_id: int: Define the path parameter
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :return: A client object
    :doc-author: Trelent
    """
    client = await repository_clients.get_client_by_id(client_id, db)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return client


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_operation_create)], description='Only moderators and admin')
async def create_client(body: ClientModel, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The create_client function creates a new client in the database.
        It takes an email, password, and full_name as input parameters.
        The function returns the newly created client object.

    :param body: ClientModel: Validate the data that is sent in the request body
    :param db: Session: Pass a database session to the function
    :param current_user: User: Get the current user from the database
    :return: A clientmodel object
    :doc-author: Trelent
    """
    client = await repository_clients.get_client_by_email(body.email, db)
    if client:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email is exists!')
    client = await repository_clients.create(body, db)
    return client


@router.put("/{client_id}", response_model=ClientResponse, dependencies=[Depends(allowed_operation_update)])
async def update_client(body: ClientModel, client_id: int = Path(ge=1), db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    # user = db.query(User).filter_by(id=user_id).first()
    """
    The update_client function updates a client in the database.
        The function takes an id, body and db as parameters.
        It returns a ClientModel object.

    :param body: ClientModel: Get the body of the request
    :param client_id: int: Get the client id from the url
    :param db: Session: Access the database
    :param current_user: User: Get the current user from the database
    :return: A clientmodel object
    :doc-author: Trelent
    """
    client = await repository_clients.update(client_id, body, db)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allowed_operation_remove)])
async def remove_client(client_id: int = Path(ge=1), db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    The remove_client function removes a client from the database.
        The function takes in an integer as a parameter, which is the id of the client to be removed.
        It also takes in two dependencies: db and current_user.
            - db is used to access our database session, so that we can make changes to it (in this case, removing a client).
            - current_user is used for authentication purposes; only users with admin privileges are allowed to remove clients.

    :param client_id: int: Specify the client id that will be used to remove a client
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the user that is currently logged in
    :return: The removed client
    :doc-author: Trelent
    """
    client = await repository_clients.remove(client_id, db)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return client
